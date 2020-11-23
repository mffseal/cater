import json

from flask import jsonify, request, flash, render_template
from flask_login import current_user

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.moduls.gift import Gift
from app.moduls.wish import Wish
from app.spider.maoshu_book import MaoShuBook
from app.view_models.book import BookViewModel, BookCollection
from app.view_models.trade import TradeInfo
from . import web


@web.route('/book/search')
def search():
    # 校验层, 接受request参数列表
    form = SearchForm(request.args)
    # 实例化视图模型
    books = BookCollection()

    if form.validate():
        # strip()兼容前后空格
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        # 实例化原始数据模型
        maoshu_book = MaoShuBook()

        if isbn_or_key == 'isbn':
            maoshu_book.search_by_isbn(q)
        else:
            maoshu_book.search_by_keyword(q, page)

        # 将原始数据对象传递给视图模型对象
        books.fill(maoshu_book, q)
        # 递归得将不可序列化的类转化为字典
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html', books=books, form=form)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    # 设置书本的默认状态
    # 根据这两个变量进行显示控制
    # 表示这本书是否被人索要或送出
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍详情
    maoshu_book = MaoShuBook()
    maoshu_book.search_by_isbn(isbn)
    book = BookViewModel(maoshu_book.first)

    # 判断用户是否登录
    if current_user.is_authenticated:
        # 判断当前用户是否是这本书的赠送者
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
        # 判断当前用户是否索要此书籍
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True
    # 取送出和想要的书
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    # 处理原始数据
    # 使用视图模型处理书籍库查出的数据
    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)

    return render_template('book_detail.html', book=book, wishes=trade_wishes_model, gifts=trade_gifts_model,
                           has_in_wishes=has_in_wishes, has_in_gifts=has_in_gifts)

