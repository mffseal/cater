from flask import current_app, flash, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.moduls.gift import Gift
from . import web


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]

    return 'My Gitfs'


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    # 判断操作合法性
    if current_user.can_save_to_list(isbn):
        # try:
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            # 获取用户id
            # current_user就是实例化后User的模型对象
            gift.uid = current_user.id
            # 读取豆子的增加量配置
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            # 这样写体现了事务操作，对user表和gift表要么同时操作要么不操作
            # 所有对数据库的操作直到这里才开始提交
            db.session.add(gift)
            # db.session.commit()
        # except Exception as e:
        #     db.session.rollback()
        #     raise e
    else:
        flash('这本书已经添加至你的赠送清单或已存在与你的心愿清单，请不要重复添加')
    # 赠送后返回之前书本的详情页面
    # TODO: Ajax
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
def redraw_from_gifts(gid):
    pass
