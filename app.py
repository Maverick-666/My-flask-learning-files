from flask import Flask
from markupsafe import escape # 防止用户恶意输入
from flask import url_for # 生成动态的URL
from flask import request
from flask import redirect
from flask import render_template
from faker import Faker

app = Flask(__name__)

# 创建book类
class books:

    def __init__(self,name,price):
        self.name = name
        self.price = price

@app.route('/')
def index():
    return render_template('index.html',name=name,movies=movies)

# 第一种传参，查询字符串/blog?blog_id=10&username=Alice
@app.route("/blog")
def blog_detail():
     blog_id = request.args.get("blog_id",default=1,type=int)
     my_name = request.args.get("username",default="Maverick",type=str)
     return render_template("blog_detail.html",blog_id = blog_id, my_name = my_name,another_information = '今天是2025年6月12日')

#查询字符串的方式传参 2
@app.route("/book/list",methods=['GET','POST'])
def hello():
    # arguements: 参数
    # request.args: 类字典类型
    page = request.args.get("page", default=1,type=int) # request能够获取输入的信息，默认值是1
    return f'<h1>您获取的是第{page}页的图书列表</h1><img src="http://helloflask.com/totoro.gif">'

# 第二种传参，使用动态路由
@app.route("/secret_page/<password>", methods = ['GET','POST'])
def secret(password):
    book = books('secrets of the world','999$')
    return render_template("secret_page.html",password = password, book = book)

# jinja的条件控制
@app.route("/control")
def age_control():
    age = request.args.get("age", default= 17, type=int)
    return render_template("control.html",age = age,movies = movies)

# jinja的模板继承
@app.route("/child1")
def child1():
    return render_template("child_1.html")

# jinja的模板继承2
@app.route("/child2")
def child2():
    return render_template("child_2.html")    

# jinja的静态文件
@app.route("/static")
def static_demo():
    return render_template("static.html")
     

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    return f'Hello, {username}!'

@app.route("/user/<name>")
def user_page(name):
    return f'<h1>User:{escape(name)}</h1>'

@app.route("/test")
def test_url_for():
    # 下面是一些调用示例（请访问 http://localhost:5000/test 后在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 生成 hello 视图函数对应的 URL，将会输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for("user_page", name="greyli"))# 输出：/user/greyli
    print(url_for("user_page", name="peter"))# 输出：/user/peter
    print(url_for("test_url_for")) # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面
    print(url_for("test_url_for", num=2)) # 输出：/test?num=2
    return "test page"

@app.route('/goback/<int:year>')
def go_back(year):
    return f'<p>Welcome to {2025-year}</p>'

@app.route('/anotherweb')
def another_website():
    return '', 302 , {'Location': 'https://www.runoob.com/flask/flask-tutorial.html'}

@app.route('/redirect')
def redirect_to_another_website():
    return redirect(url_for('another_website'))

@app.route('/redirect2')
def redirect_to_another_website2():
    return redirect("https://github.com/")

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