from flask import Flask,session,g
import config
from exts import db,mail
from models import UserModel
from blueprints.func import bp as func_bp
from blueprints.user import bp as user_bp
from blueprints.display import bp as display_bp
from blueprints.forecast import bp as forecast_bp
from flask_migrate import Migrate
from flask import Markup


app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)


db.init_app(app)
mail.init_app(app)

migrate = Migrate(app,db)

app.register_blueprint(func_bp)
app.register_blueprint(user_bp)
app.register_blueprint(display_bp)
app.register_blueprint(forecast_bp)

# blueprint：用来做模块化

# flask db init:只需要执行一次
# flask db migrate:将orm模型生成迁移脚本
# flask db upgrade:将迁移脚本映射到数据库中
# before_request/before_first_request/ after_request :钩子函数
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g,"user",user)
    else:
        setattr(g,"user",None)

@app.context_processor
def my_context_processor():
    return {"user":g.user}



if __name__ == '__main__':
    app.run()
