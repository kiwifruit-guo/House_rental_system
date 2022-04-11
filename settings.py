# 盛放所有的配置信息
from flask_sqlalchemy import SQLAlchemy

# 创建flask-sqlalchemy的实例对象
db = SQLAlchemy()


class Config:
    # 开启调试模式
    DEBUG = True

    # 配饰flask-sqlalchemy数据库的链接地址
    # '数据库的类型://用户名:密码@数据库的地址:端口号/数据库的名字'   注意点  这里使用的标点符号都是英文的
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/beijing_house_data'

    # 压制警告信息
    SQLALCHEMY_TRACK_MODIFICATIONS = True
