from flask import flash, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.moduls.wish import Wish
from . import web


@web.route('/my/wish')
def my_wish():
    pass


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.uid = current_user.id
            wish.isbn = isbn
            db.session.add(wish)
    else:
        flash('这本书已经添加至你的赠送清单或已存在与你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))
