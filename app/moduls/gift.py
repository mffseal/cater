from flask import current_app
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship

from app.moduls.base import Base, db
from app.moduls.wish import Wish
from app.spider.maoshu_book import MaoShuBook


class Gift(Base):
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

    # 取出用户送出书的清单
    @classmethod
    def get_user_gifts(cls, uid):
        # 根据用户uid查询出该用户所有礼物
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time).all())
        return gifts

    # 根据isbn查询该书心愿单人数
    @classmethod
    def get_wish_counts(cls, isbn_list):
        # 根据传入的一组isbn，到with表中计算出某个礼物
        # 并且计算出某个礼物的wish心愿数量
        # 最后要的是每一个isbn对应的数量，要分组
        # 使用mysql的in查询
        # filter接受的不是参数，而是条件表达式
        # 使用func.count()来计数
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(Wish.launched is False, Wish.status == 1,
                                                                Wish.isbn.in_(isbn_list)).group_by(Wish.isbn).all()
        return count_list

    # 根据isbn取得图书数据
    @property
    def book(self):
        # 调用api查询isbn
        maoshu_book = MaoShuBook()
        maoshu_book.search_by_isbn(self.isbn)
        return maoshu_book.first

    # 读取最近赠送的书籍，提供结果数量限制和去重
    @classmethod
    def recent(cls):
        # 链式调用
        # limit()限制返回结果数
        # distinct前要先group_by
        # desc倒序
        recent_gift = Gift.query.filter_by(launched=False).group_by(
            Gift.isbn).order_by(desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift
