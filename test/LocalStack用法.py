from werkzeug.local import LocalStack


# 要创建一个栈对象, 要实现push, pop, top方法
# 1. 实例化LocalStack

s = LocalStack()
s.push(1)  # 压栈
print(s.top)  # 取栈顶, top不是方法是属性, 调用的时候不需要括号
print(s.top)  # 栈顶元素不会被删除
print(s.pop())  # 弹出栈顶元素
print(s.top)  # 元素已经被删除

s.push(1)
s.push(2)
print(s.top)
print(s.top)  # 两次取的都是同一个元素
s.pop()  # 后进先出
print(s.top)
