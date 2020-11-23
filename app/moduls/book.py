from sqlalchemy import Column, String, Integer, Float

from app.moduls.base import db


# 数据库book表模型
class Book(db.Model):
    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    author = Column(String(30), default='未名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(Float)
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(50))
    summary = Column(String(1000))
    image = Column(String(50))
