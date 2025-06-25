# -*- coding: utf-8 -*-

# ==============================================================================
# 1. 模块导入
# 导入所有需要的库和模块
# ==============================================================================
import datetime
from flask import Flask, url_for, request, redirect, render_template
from markupsafe import escape
from faker import Faker
from flask_sqlalchemy import SQLAlchemy

# ==============================================================================
# 2. 应用初始化和配置
# 创建Flask应用实例并进行相关配置，包括数据库连接
# ==============================================================================
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# MySQL数据库配置
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "Maverick"  # 请替换为你自己的用户名
PASSWORD = "root"  # 请替换为你自己的密码
DATABASE = "database_learn"  # 请替换为你自己的数据库名
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 推荐关闭，以减少性能开销

# 初始化SQLAlchemy
db = SQLAlchemy(app)


# ==============================================================================
# 3. 数据库模型定义 (Models)
# 定义所有与数据库表对应的ORM类
# ==============================================================================
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", backref="articles")


# ==============================================================================
# 4. 辅助类和模拟数据
# 定义一些非数据库模型的类，并创建用于测试的模拟数据
# ==============================================================================
class Books:
    """一个简单的书籍类，用于演示"""

    def __init__(self, name, price):
        self.name = name
        self.price = price


# 使用Faker库生成模拟数据
fake = Faker()
name = fake.name()
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]


# ==============================================================================
# 5. 自定义模板过滤器 (Template Filters)
# 定义所有Jinja2模板中使用的自定义过滤器
# ==============================================================================
@app.template_filter("my_cut")
def cut(value):
    """自定义过滤器，替换字符串中的'world'"""
    value = value.replace("world", "ybx")
    return value


@app.template_filter("handle_time")
def handle_time(time):
    """
    一个处理时间的过滤器，根据时间差显示不同的格式。
    - 小于1分钟: "刚刚"
    - 小于1小时: "xx分钟前"
    - 小于1天: "xx小时前"
    - 小于30天: "xx天前"
    - 超过30天: 显示具体日期
    """
    if isinstance(time, datetime.datetime):
        now = datetime.datetime.now()
        timestamp = (now - time).total_seconds()
        if timestamp < 60:
            return "刚刚"
        elif 60 <= timestamp < 3600:
            minutes = int(timestamp / 60)
            return f"{minutes}分钟前"
        elif 3600 <= timestamp < 86400:
            hours = int(timestamp / 3600)
            return f"{hours}小时前"
        elif 86400 <= timestamp < 2592000:
            days = int(timestamp / 86400)
            return f"{days}天前"
        else:
            return time.strftime("%Y-%m-%d, %H:%M:%S")
    return time


@app.template_filter("dateformat")
def dateformat(value, format="%Y-%m-%d %H:%M"):
    """格式化日期的过滤器"""
    if isinstance(value, datetime.datetime):
        return value.strftime(format)
    return value


# ==============================================================================
# 6. 视图函数 (Routes / Views)
# 定义应用的URL路由和对应的处理函数
# ==============================================================================

# --- 主页和基础功能 ---
@app.route('/')
def index():
    signature1 = '<script>alert("Hello")</script>'
    persons = ['ybx', 'hh']
    hello1 = list('hello')  # 将字符串转换为列表
    str1 = 'hello world'
    # 修正: 使用 datetime.datetime 创建对象
    create_time = datetime.datetime(2025, 6, 20, 16, 0, 0)

    context = {
        'name': name,
        'movies': movies,
        'signature1': signature1,
        'persons': persons,
        'hello1': hello1,
        'str1': str1,
        'create_time': create_time,
        'person' : {
            'username': 'ybx',
            'age' : 18,
            'country': 'china',
        }
    }
    # keys() -> iterkeys
    # values() -> itervalues
    # items -> iteritems
    return render_template('index.html', **context)


@app.get('/variables')
def variables():
    context = {
        "hobby": "玩游戏",
        "my_book": Books(name="good luck", price=2000),
        "people": {"name": "龙逍遥", "height": "185cm"},
    }
    return render_template("variables.html", **context)


# --- 数据库操作 (CRUD) ---
@app.route("/user/add")
def add_user():
    user = User(username="Maverick", password="root")
    db.session.add(user)
    db.session.commit()
    return "用户添加成功"


@app.route("/user/query")
def query_user():
    users = User.query.filter_by(username="Maverick").all()
    for user in users:
        print(f"查询到用户: {user.username}")
    return "数据查找成功 (请查看控制台)"


@app.route("/user/update")
def update_user():
    user = User.query.filter_by(username="Maverick").first()
    if user:
        user.password = "root_updated"
        db.session.commit()
        return "数据修改成功"
    return "未找到要修改的用户"


@app.route("/user/delete")
def delete_user():
    user = User.query.filter_by(password="root").first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return "数据已删除"
    return "未找到要删除的用户"


@app.route("/article/add")
def add_article():
    user = User.query.get(1)
    if user:
        article1 = Article(title="Flask 学习", content="我喜欢学Flask", author=user)
        article2 = Article(title="Django 学习", content="我喜欢学Django", author=user)
        db.session.add_all([article1, article2])
        db.session.commit()
        return "文章添加成功"
    return "未找到ID为1的用户，无法添加文章"


@app.route("/article/query")
def query_article():
    user = User.query.get(1)
    if user:
        for article in user.articles:
            print(f"用户 '{user.username}' 的文章: {article.title}")
        return "文章查找成功 (请查看控制台)"
    return "未找到ID为1的用户"


# --- 模板功能演示 ---
@app.route("/control")
def age_control():
    age = request.args.get("age", default=17, type=int)
    return render_template("control.html", age=age, movies=movies)


@app.route("/child1")
def child1():
    return render_template("child_1.html")


@app.route("/child2")
def child2():
    return render_template("child_2.html")


@app.route("/static")
def static_demo():
    return render_template("static.html")


# --- 路由和请求处理演示 ---
@app.route("/blog")
def blog_detail():
    blog_id = request.args.get("blog_id", default=1, type=int)
    my_name = request.args.get("username", default="Maverick", type=str)
    return render_template("blog_detail.html", blog_id=blog_id, my_name=my_name)


@app.route("/book/list")
def book_list():
    page = request.args.get("page", default=1, type=int)
    return f'<h1>您获取的是第{page}页的图书列表</h1><img src="http://helloflask.com/totoro.gif">'


@app.route("/secret_page/", methods=['GET', 'POST'])
def secret_page():
    if request.method == "GET":
        book = Books('Secrets of the World', price='999')
        context = {
            'book': book,
            'signature': request.args.get("signature"),
        }
        return render_template("secret_page.html", **context)
    else:
        username = request.form.get('username')
        return f'Success, {escape(username)}!'


@app.route('/<any(yellow, green):url_path>/<id>/')
def same_url(url_path, id):
    return f'<h1 style="color:{url_path};">这是{url_path}界面的第{id}页</h1>'


@app.route("/user/<name>")
def user_page(name):
    return f'<h1>User: {escape(name)}</h1>'


@app.route("/test_url")
def test_url_for():
    print(url_for('index'))
    print(url_for("user_page", name="greyli"))
    print(url_for("test_url_for", next='/'))
    return "URL生成测试 (请查看控制台)"


@app.route('/goback/<int:year>')
def go_back(year):
    # 修正: 动态获取当前年份
    current_year = datetime.datetime.now().year
    return f'<p>Welcome to {current_year - year}</p>'


# --- 重定向功能演示 ---
@app.route('/anotherweb')
def another_website():
    return '这是一个外部网站的模拟页面。'


@app.route('/redirect')
def redirect_to_another_website():
    return redirect(url_for('another_website'))


@app.route('/github')
def redirect_to_github():
    return redirect("https://github.com/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 实际项目中这里会有登录验证逻辑
        return redirect(url_for('profile', name=request.form.get('username', 'Guest')))
    return render_template('login.html')


@app.route('/profile')
def profile():
    name = request.args.get("name")
    if not name:
        return redirect(url_for('login'))
    return f"<h1>欢迎, {escape(name)}!</h1>"

@app.route('/index_2')
def index_2():
    return render_template("index_2.html")



# ==============================================================================
# 7. 应用启动
# 作为脚本直接运行时，创建数据库表并启动开发服务器
# ==============================================================================
if __name__ == '__main__':
    # 使用应用上下文来确保db操作有正确的环境
    with app.app_context():
        # 创建所有定义的数据库表（如果它们尚不存在）
        db.create_all()
    # 启动Flask的开发服务器
    # debug=True会在代码修改后自动重载，并提供详细的错误页面
    app.run(debug=True, port=5000)