# 登陆注册提交验证表单功能
import wtforms
from wtforms.validators import Email,Length,EqualTo
from models import UserModel,EmailCaptchaModel,FindPasswordModel
from exts import db

#Form：主要就是用来验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="邮箱验证码格式错误!")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误!")])
    password = wtforms.StringField(validators=[Length(min=6, max=15, message="密码格式错误!")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password",message="密码与确认密码不一致！")])

    # 自定义验证：
    # 1、邮箱是否被注册
    def validate_email(self,field):
        print("邮箱存在性验证测试")
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已被注册！")
    # 2、验证码是否正确
    def validate_captcha(self,field):
        print("验证码对应验证测试")
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码有误！")
        # else:
        #     # todo:可以删除掉已经使用的captcha
        #     db.session.delete(captcha_model)
        #     db.session.commit()

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=15, message="密码格式错误!")])

class FindPasswordForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="邮箱验证码格式错误!")])
    newpassword = wtforms.StringField(validators=[Length(min=6, max=15, message="密码格式错误!")])
    password_again = wtforms.StringField(validators=[EqualTo("newpassword", message="密码与确认密码不一致！")])
    def validate_captcha(self,field):
        print("验证码对应验证测试")
        captcha = field.data
        email = self.email.data
        captcha_model = FindPasswordModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码有误！")