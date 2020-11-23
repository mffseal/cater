from contextlib import contextmanager
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import SmallInteger, Column, Integer


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield  # with不用as，就不用返回值
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


# 继承后重写filter_by函数
# 默认查询status=1也就是没被标记删除的条目
class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1  # 加上默认的删除状态，查询时不用再写
        # 调用父类被覆盖的方法
        return super(Query, self).filter_by(**kwargs)


# 指定Query对象，使得改写的filter_by生效
db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    # 让SQLAlchemy识别为基类
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        # 给创建时间字段赋值
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        # 遍历字典
        for key, value in attrs_dict.items():
            # 判断某个对象是否包含某个属性
            if hasattr(self, key) and key != 'id':
                # 动态赋值
                setattr(self, key, value)

    # 将时间字段由整数转为时间对象
    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None
