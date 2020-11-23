from flask import render_template

from app.moduls.gift import Gift
from app.view_models.book import BookViewModel
from . import web


@web.route('/index')
def index():
    recent_gifts = Gift.recent()
    # 把gift转化为book的view_models
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('index.html', recent=books)
