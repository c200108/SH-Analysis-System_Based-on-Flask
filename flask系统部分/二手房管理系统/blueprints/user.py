# 用户登陆注册
from flask import  Blueprint,render_template,jsonify,redirect,url_for,session,g
from exts import mail,db
from flask_mail import Message
from random import randint
from flask import request
from models import EmailCaptchaModel,UserModel,FindPasswordModel
from .forms import RegisterForm,LoginForm,FindPasswordForm
from werkzeug.security import generate_password_hash,check_password_hash

bp = Blueprint('user',__name__,url_prefix='/user')

#用户登录
@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                str_email = "邮箱不存在或未注册！"
                print(str_email)
                return render_template('login.html',str = str_email)
            if check_password_hash(user.password, password):
                # cookie：
                # cookie中不适合存储太多的数据，只适合存储少量的数据
                # cookie一般用来存放登录授权的东西
                # flask中的session，是经过加密后存储在cookie中的
                session['user_id'] = user.id
                return redirect("/")
            else:
                str_password = "密码错误！"
                print(str_password)
                return render_template('login.html',str = str_password)
        else:
            str = form.errors
            print(str)
            return render_template('login.html', str=str)

#用户注册
# GET：从服务器上获取数据
# POST：将客户端的数据提交给服务器
@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证：flask-wtf: wtforms
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            print(user)
            return redirect(url_for("user.login"))
        else:
            print(form.errors)
            return render_template('register.html',message = form.errors)
            # return redirect(url_for("user.register"))

#忘记密码
@bp.route('/forgetPassword',methods=['GET','POST'])
def forgetPassword():
    if request.method == 'GET':
        return render_template('forgetPassword.html')
    else:
        form = FindPasswordForm(request.form)
        if form.validate():
            email = form.email.data
            user_find = UserModel.query.filter_by(email=email).first()
            if not user_find:
                str_email = "邮箱不存在或未注册！"
                print(str_email)
                return render_template('forgetPassword.html',message = str_email)
            else:
                new_password = request.form.get('newpassword')
                user_find.password = generate_password_hash(new_password)
                db.session.commit()
                message = "密码修改成功"
                return render_template('forgetPassword.html',message=message)
        else:
            print(form.errors)
            return render_template('forgetPassword.html', message=form.errors)

#退出登录
@bp.route('/logout')
def logout():
    session.clear()
    return redirect("/")

#发送邮箱注册验证码
@bp.route('/captcha/email')
def get_email_captcha():
    # /captcha/email/<email>
    # /captcha/email?email=xxx@qq.com
    email = request.args.get("email")
    captcha = randint(1000, 9999)
    # I/O操作 邮件发送与页面变化有延迟
    message = Message(subject='二手房数据网站注册申请', recipients=[email],
                      body=f'很荣幸您在本网站注册账户，您的邮箱验证码为{captcha},请不要告诉他人。\n此信息来自SH-Analysis网站')
    mail.send(message)
    #1、验证码暂存缓存方式 memcached/redis
    #2、用数据库表的方式存储
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # RESTful API
    # {code: 200/400/500 message: "" data: None}
    return jsonify({'code':200, 'message':'', 'data':None})

#找回密码发送邮箱验证码
@bp.route('/find/email')
def find_captcha():
    # /captcha/email/<email>
    # /captcha/email?email=xxx@qq.com
    email = request.args.get("email")
    captcha = randint(1000, 9999)
    # I/O操作 邮件发送与页面变化有延迟
    message = Message(subject='二手房数据网站找回密码', recipients=[email],
                      body=f'你正在修改用户密码，请确认是否为本人操作，您的邮箱验证码为{captcha},请不要告诉他人。\n此信息来自SH-Analysis网站')
    mail.send(message)
    #1、验证码暂存缓存方式 memcached/redis
    #2、用数据库表的方式存储
    findpassword_captcha = FindPasswordModel(email=email, captcha=captcha)
    db.session.add(findpassword_captcha)
    db.session.commit()
    # RESTful API
    # {code: 200/400/500 message: "" data: None}
    return jsonify({'code':200, 'message':'', 'data':None})

#用户个人中心
@bp.route('/message',methods=['GET','POST'])
def message():
    if request.method == 'GET':
        return render_template("message.html")
    else:
        global new_username, new_phone, new_address, new_sex, new_age
        # 从POST请求中获取表单数据
        new_username = request.form.get('username')
        new_phone = request.form.get('phone')
        new_address = request.form.get('address')
        new_sex = request.form.get('sex')
        new_age = request.form.get('age')
        #对输入内容判断
        if new_username == "":
            new_username = g.user.username
        if new_phone == "":
            new_phone = g.user.phone
        if new_address == "":
            new_address = g.user.address
        if new_sex == "":
            new_sex = g.user.sex
        if new_age == "":
            new_age = g.user.age
        # 更新用户数据
        hhh = UserModel.query.filter(UserModel.username == g.user.username).first()
        hhh.username = new_username
        hhh.phone = new_phone
        hhh.address = new_address
        hhh.sex = new_sex
        hhh.age = new_age
        db.session.commit()
        # 返回更新后的个人资料页面
        return render_template('message.html')




