from flask import Flask, current_app

app = Flask(__name__)

# ctx = app.app_context()
# ctx.push()
# a = current_app()
# b = a.config['DEBUG']
# ctx.pop()

with app.app_context():
    a = current_app()
    b = a.config['DEBUG']
    print(b)


# 上下文管理器类
class MyResource:
    def __init__(self):
        my_value = "上下文为函数提供的'全局'变量"

    def __enter__(self):
        print("连接资源")
        return self  # 给as后的变量传递对象

    """
    exc_type, exc_val, exc_tb 用于接收异常信息
    没有发生异常则三个参数为None
    发生异常则接收异常信息
    """

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("回收资源, 处理异常")
        if exc_tb:
            print("发生异常, 需要处理")
        else:
            print("没有异常, 无需处理")
        return True  # 内部处理异常
        return False  # 将异常抛到外部, 等同于不写return

    def query(self):
        print("查询数据")

def worker():
    print("访问上下文中的'全局'变量:")
with MyResource() as resource:
    resource.query()
