# coding:utf-8
import json
from decimal import Decimal
from random import Random
from werkzeug.routing import BaseConverter


# 定义正则转换器
class ReConverter(BaseConverter):
    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super(ReConverter, self).__init__(url_map)
        # 保存正则表达式
        self.regex = regex


def trueReturn(code, errmsg, data=None, *args):
    for arg in args:
        print(arg)
    return {
        "status": True,
        "code": code,
        "data": data,
        "msg": errmsg,
    }


def falseReturn(code, errmsg, data=None):
    return {
        "status": False,
        "errno": code,
        "data": data,
        "errmsg": errmsg
    }


# 生成随机salt
def create_salt(length=4):
    """
    生成随机盐值
    :param length:  默认盐值长度为4
    :return: 返回生成的盐值
    """
    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'

    # 获取chars 的最大下标
    len_chars = len(chars) - 1
    random = Random()
    for i in range(length):
        # 每次从chars中抽取一位拼接成一个salt值
        salt += chars[random.randint(0, len_chars)]
    return salt


def tuple_to_dict(tuple_list):
    """ 传入元组"""
    result_dict = list()
    for i in tuple_list:
        # 对l 进行字典化
        # [(1,name),(2,name)] --> [{'id': 3, 'name': '改名'}, {'id': 4, 'name': '擇日'}]
        __dict = dict(zip(("index", "type"), i))
        result_dict.append(__dict)
    return result_dict


# 重写jsonJSONEncoder 方法

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)
