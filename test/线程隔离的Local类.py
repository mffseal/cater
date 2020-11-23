import threading
import time

from werkzeug.local import LocalStack, Local


s = LocalStack()
s.push(1)


def worker():
    print("子线程第一次取local: "+str(s.top))
    s.push(2)  # 子线程
    print("子线程在push后取栈顶: "+str(s.top))


t = threading.Thread(target=worker, name="子线程")
t.start()
time.sleep(1)
print("子线程结束后主线程栈顶值: "+str(s.top))  # 主线程栈顶还是1
