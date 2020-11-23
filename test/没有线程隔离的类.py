import threading
from datetime import time


class A:
    b = 1


my_obj = A()  # 实例化一个对象


def worker():
    my_obj.b = 2


# 创建一个线程, 在线程中修改对象属性值
new_t = threading.Thread(target=worker, name="test")
new_t.start()

# 在主线程中查看对象属性值是否隔离(被修改)
time.sleep(1)  # 休眠1秒, 使新线程在主线程执行前完成
print(my_obj.b)
