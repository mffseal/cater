

# 单本数据结构
# 修饰原始数据
class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.pages = book['pages']
        self.author = '、'.join(book['author'])
        self.price = book['price']
        self.summary = book['summary']
        self.image = book['image']
        self.isbn = book['isbn']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    # 用/来分割三个字段，并且兼容字段空的情况
    # 用属性的方法访问函数
    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        # python3中filter()返回的是迭代器对象
        # join()接收的是可迭代对象，比如列表和迭代器
        return ' / '.join(intros)


# 最终需要的多本书的数据结构
# 将单本数据整合为最终的统一数据结构
class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    # 通过单本书的类裁剪数据后填充进来
    def fill(self, maoshu_book, keyword):
        self.total = maoshu_book.total
        self.keyword = keyword
        # 利用列表生成式
        self.books = [BookViewModel(book) for book in maoshu_book.books]

# class BookViewModel:
#     # 单本结果
#     @classmethod
#     def package_single(cls, data, keyword):
#         returned = {
#             'books': [],
#             'total': 0,
#             'keyword': keyword
#         }
#         if data:
#             returned['total'] = 1
#             returned['books'] = [cls.__cut_book_data(data)]
#         return returned
#
#     # 集合结果
#     @classmethod
#     def package_collection(cls, data, keyword):
#         # 一致的数据结构
#         returned = {
#             'books': [],
#             'total': 0,
#             'keyword': keyword
#         }
#         if data:
#             returned['total'] = data['total']
#             returned['books'] = [cls.__cut_book_data(book) for book in data['books']]
#         return returned
#
#     # 裁剪原始数据
#     @classmethod
#     def __cut_book_data(cls, data):
#         book = {
#             'title': data['title'],
#             'publisher': data['publisher'],
#             'pages': data['pages'] or '',  # None转为空字符
#             'author': '、'.join(data['author']),
#             'price': data['price'],
#             'summary': data['summary'] or '',  # None转为空字符
#             'image': data['image']
#         }
#         return book
