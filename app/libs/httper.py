import requests


# http请求类, 用于获取外部API数据
class HTTP:
    # 默认返回json格式的数据
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        # 不是200则返回空字符
        if r.status_code != 200:
            return {} if return_json else ''
        else:
            return r.json() if return_json else r.text
