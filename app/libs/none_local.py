class NoneLocal:
    def __init__(self, v):
        self.v = v


n = NoneLocal(1)  # 不是线程隔离的一个对象
