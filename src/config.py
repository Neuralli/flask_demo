import redis


class Config(object):
    """配置信息"""

    # 随机加密盐值,随机即可
    # SECRET_KEY = "gXDWCGzm$AW0zfWgR@k2SYa33U6sTVPjs0ai8oqHkqS7XM"
    SECRET_KEY = ""
    AUTH_SALT = "sYjLRzKQG4vra"
    EXPIRES_IN = 3600

    # 文件保存路径
    UPLOAD_FOLDER = '/static'

    # 数据库
    # SQLALCHEMY_DATABASE_URI = "mysql://root:sa123@192.168.126.131:3307/metaphysics"
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis
    REDIS_HOST = "192.168.126.131"
    REDIS_PORT = "6379"
    #
    # # flask_session
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True  # 对cookie中的session_id是否隐藏
    PERMANENT_SESSION_LIFETIME = 86400  # 设置session过期的时间，单位s


class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置信息"""
    DEBUG = False


config_map = {
    'develop': DevelopmentConfig,
    'product': ProductionConfig
}
