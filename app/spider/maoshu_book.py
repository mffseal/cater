from app.libs.httper import HTTP
from flask import current_app


# 原始数据模型, 数据通过外部API获取
class MaoShuBook:
    # 模型层 MVC M层
    # 外部API调用url
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    # 实例变量, 用于保存原始数据
    def __init__(self):
        self.total = 0
        self.books = []

    # 通过isbn搜索
    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    # 通过关键字搜索
    def search_by_keyword(self, keyword, page=1):
        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'], self.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    # 计算页数
    @staticmethod
    def calculate_start(page):
        return (page - 1) * current_app.config['PER_PAGE']

    # 保存isbn搜索获取的信息到实例对象
    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    # 保存关键字搜索获取的信息到实例对象
    def __fill_collection(self, data):
        if data:
            self.total = data['total']
            self.books = data['books']

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None
