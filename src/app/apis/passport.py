"""
用户注册资源
"""
import re
import uuid

from flask import request, jsonify, session, current_app
from flask_restplus import Namespace, Resource, fields
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app import db
from app.models import User, UserAuth
from utils import commons
from utils.NameGenerator import gen_two_words
from utils.response_code import Code

api = Namespace('user', description='用户')

resource_fields = api.model('Resource', dict(nick_name=fields.String, email=fields.String, password=fields.String,
                                             password2=fields.String, interest=fields.String, focus=fields.String))


# url =/api/v1.0/user
@api.route('/')
class UserResource(Resource):
    @api.doc(
        params={'nick_name': '用户昵称(非必须)',
                'email': "邮箱(必须)",
                "password": "第1次输入密码(必须)",
                "password2": "第2次输入密码(必须)",
                "focus": "关注(Json)",
                "interest": "兴趣(Json)"
                })
    @api.doc(
        responses={
            200: 'Success',
            400: 'Validation Error',
            4103: 'Incomplete Parameters'
        })
    @api.expect(resource_fields)
    # url =/api/v1.0/user
    def post(self):
        """
        使用邮箱完成用户账号的注册
        """
        # 接收参数
        request_dict = request.get_json()
        nick_name = request_dict.get('nick_name')
        email = request_dict.get('email')
        password = request_dict.get('password')
        password2 = request_dict.get('password2')
        focus = request_dict.get('focus')
        interest = request_dict.get('interest')

        # 校验参数
        # 校验邮箱或者密码参数是否输入完整
        if not all([email, password, password2]):
            return jsonify(errno=Code.PARAMERR, errmsg="请输入完整的邮箱和密码")

        # 生成昵称
        if not nick_name:
            nick_name = gen_two_words(split=' ', lowercase=False)

        # 校验邮箱是否符合格式
        if not re.match(
                r'^[\.A-Za-z0-9_-]+@[A-Za-z0-9_-]+(\.[A-Za-z0-9_-]+)+$', email):
            return jsonify(errno=Code.PARAMERR, errmsg="请输入正确的邮箱")

        # 验证两次输入的密码是否一致
        if password != password2:
            return jsonify(errno=Code.PARAMERR, errmsg="两次输入的密码不一致")

        # 逻辑处理
        create_ip = request.remote_addr
        # 生成唯一的登录标识
        user_uuid = uuid.uuid1().hex
        # 加密用户密码
        credential = generate_password_hash(password)

        # 保存用户的注册数据到数据库
        user = User(nick_name=nick_name, email=email, focus=focus, interest=interest)

        try:
            # user = db.session.query(User).
            db.session.add(user)

            db.session.flush()
            db.session.commit()
            user_id = user.id
            user_auth = UserAuth(id=user.id,
                                 identity_type="EMAIL",
                                 identifier=user_uuid,
                                 credential=credential,
                                 create_ip=create_ip)
            db.session.add(user_auth)
            db.session.commit()
            db.session.close()

        except IntegrityError as e:
            # 数据库操作错误后的回滚
            db.session.rollback()
            # 表示该邮箱已经注册过账号,返回直接登陆
            current_app.logger.error(e)

            return jsonify(commons.falseReturn(
                code=Code.DATAEXIST, errmsg="该邮箱已经注册过账号，请直接登录"))

        except Exception as e:
            db.session.rollback()
            # 表示邮箱账号出现了重复值，即邮箱已注册过
            current_app.logger.error(e)
            return jsonify(commons.falseReturn(
                code=Code.DATAEXIST, errmsg="查询数据异常"))

        # # 保存登录状态到session中
        session["name"] = nick_name
        session["email"] = email
        session["user_id"] = user_id
        # 返回结果
        return jsonify(commons.trueReturn(code=Code.OK, errmsg="注册成功"))
