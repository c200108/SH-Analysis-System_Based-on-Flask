# 配置文件

SECRET_KEY = 'afwfiofiaidha'
# 数据库配置信息
#MySQL所在的主机名
HOSTNAME = '127.0.0.1'
# MySQL监听的端口号，默认3306
PORT = 3306
# 连接MySQL的用户名
USERNAME = 'root'
# 连接MySQL的密码
PASSWORD = '12345678'
# MySQL上的创建数据库的名称
DATABASE = 'secondhouse1'
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮箱配置信息
MAIL_SERVER = "smtp.163.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "sh_analysis2023@163.com"
MAIL_PASSWORD = "UEORUEMNVGZDOMJS"
MAIL_DEFAULT_SENDER = "sh_analysis2023@163.com"
# gbkmnnqblxafechc
# sh_analysis2023@163.com  UEORUEMNVGZDOMJS