from flask import Blueprint
from flask_restplus import Api

# 导入api 应用
# from .apis.namespaceX import api as nsX

from .apis.passport import api as user

# from .apis.article_all import api as article_all

# 创建蓝图
blueprint = Blueprint('api', __name__)
api = Api(blueprint,
          title='FS_app_api',
          version='1.0',
          description='风水师App接口 V1.0',
          )

# 添加api应用到蓝图
# api.add_namespace(nsX)
# 用户
api.add_namespace(user)