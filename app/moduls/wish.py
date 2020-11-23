from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship

from app.moduls.base import Base


class Wish(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 模型关系
    user = relationship('User')
    # 外键
    uid = Column(Integer, ForeignKey('user.id'))
    # 书籍没有表，所以与isbn关联
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)
    # 软删除
