from flask import Flask
from markupsafe import escape # 防止用户恶意输入
from flask import url_for # 生成动态的URL
from flask import request
from flask import redirect
from flask import render_template
from faker import Faker

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',name=name,movies=movies)

@app.route("/hello",methods=['GET','POST'])
def hello():
    name = request.args.get("name", "Flask")
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'


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