from flask import Flask
from flask_login import LoginManager
from app.moduls.book import db

login_manager = LoginManager()


# Flask核心对象实例化函数
def create_app():
    app = Flask(__name__)
    # 加载配置文件
    app.config.from_object('app.setting')
    app.config.from_object('app.secure')
    # 注册蓝图
    app = register_blueprint(app)

    # 绑定模型
    db.init_app(app)
    # app.app_context()
    # 数据库
    with app.app_context():
        db.create_all()

    # 初始化登录管理器
    login_manager.init_app(app)
    # 未授权页面重定向到登录页
    login_manager.login_view = 'web.login'
    # 指定重定向同时flash的消息
    login_manager.login_message = '请先登录或注册'
    return app


# 蓝图注册函数
def register_blueprint(app):
    # 导入蓝图
    from app.web import web
    # 调用app自带函数注册蓝图
    app.register_blueprint(web)
    return app
