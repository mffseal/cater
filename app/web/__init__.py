from flask import Blueprint


# 实例化蓝图对象, 在每个视图函数文件里导入
web = Blueprint('web', __name__)


# 在app中注册此蓝图是, 自动导入并执行视图函数
from app.web import book, auth, drift, gift, main, wish
