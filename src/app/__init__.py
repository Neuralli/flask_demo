#!-*- coding:utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler

import pymysql
import redis
from flask import Flask, request
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import config_map
from utils.commons import ReConverter

pymysql.version_info = (1, 3, 13, 'final', 0)
pymysql.install_as_MySQLdb()
# 数据库
db = SQLAlchemy()

# 创建redis连接对象
redis_store = None

# 为flask补充csrf 防护
csrf = CSRFProtect()

# 配置日志信息
# 设置日志的记录等级
logging.basicConfig(level=logging.INFO)
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日记录器
logging.getLogger().addHandler(file_log_handler)


# 工厂模式
def create_app(config_name):
    """
    初始化Flask的应用对象，并初始化数据库等内容
    :param config_name: str  配置模式的模式的名字 （"develop",  "product"）
    :return:
    """
    # 创建app
    app = Flask(__name__)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 使用app 初始化db
    db.init_app(app)

    # 创建redis连接对象
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # 利用flask_session，将session数据保存在redis中
    Session(app)

    # 为flask 补充csrf防护
    # CSRFProtect(app)

    # 为flask 添加自定义的转换器
    app.url_map.converters["re"] = ReConverter

    # 注册蓝图
    # from .apis import blueprint as api
    from .apiv1 import blueprint as api1
    app.register_blueprint(api1, url_prefix="/api/v1.0")

    # from .apiv2 import blueprint as api2
    # app.register_blueprint(api2, url_prefix="/api/v2.0")

    # 使用swagger
    # Swagger(app)

    return app
