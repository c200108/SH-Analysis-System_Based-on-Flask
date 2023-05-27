# 模型文件
from datetime import datetime
from exts import db

# 数据库设置信息
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    jointime = db.Column(db.DateTime, default=datetime.now)
    phone = db.Column(db.String(200) )
    address = db.Column(db.String(200))
    sex = db.Column(db.String(200))
    age = db.Column(db.String(200))

class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    captcha = db.Column(db.String(50), nullable=False)
    # used = db.Column(db.Boolean, default=False)

class FindPasswordModel(db.Model):
    __tablename__ = "findpassword_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    captcha = db.Column(db.String(50), nullable=False)

class Quotes(db.Model):
    __tablename__ = "sh_data"
    id = db.Column(db.Integer, primary_key=True,)
    title = db.Column(db.String(255), nullable=False)#简介
    total_price = db.Column(db.Float, nullable=False)#总价
    unit_price = db.Column(db.Integer, nullable=False)#单价
    square = db.Column(db.Float, nullable=False)#面积
    size = db.Column(db.String(255), nullable=False)#户型
    floor = db.Column(db.String(255), nullable=False)#楼层
    direction = db.Column(db.String(255), nullable=False)#朝向
    type = db.Column(db.String(255), nullable=False)#楼型
    district = db.Column(db.String(255), nullable=False)#地区
    nearby = db.Column(db.String(255), nullable=False)#区域
    community = db.Column(db.String(255), nullable=False)#小区
    decoration = db.Column(db.String(255), nullable=False)#装修
    elevator = db.Column(db.String(255), nullable=False)#电梯
    elevatorNum = db.Column(db.String(255), nullable=False)#梯户比例
    ownership = db.Column(db.String(255), nullable=False)#房屋性质