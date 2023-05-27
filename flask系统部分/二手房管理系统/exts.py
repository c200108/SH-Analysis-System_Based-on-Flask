#exts.py:为了解决循环引用问题
# 第三方插件
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()
