from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.libs.helper import is_isbn_or_key
from app.moduls.base import Base

# UserMixin实现了flask-login需要的一些函数
from app.moduls.gift import Gift
from app.moduls.wish import Wish
from app.spider.maoshu_book import MaoShuBook


class User(UserMixin, Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(24), nullable=False)
    photo_number = Column(String(18), unique=True)
    # 密码，改变数据库表字段
    _password = Column('password', String(256), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    # 属性函数
    @property
    def password(self):
        return self._password

    # 写入属性的函数
    # 在写入前做预处理
    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    # 判断用户传入isbn是否规范
    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        else:
            maoshu_book = MaoShuBook()
            maoshu_book.search_by_isbn(isbn)
        if not maoshu_book.first:
            return False
        # 不允许一个用户同时赠送多本相同的书
        # 一个用户不可能同时成为赠送和索要者
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False


# 给flask-login读取用户状态用
@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
