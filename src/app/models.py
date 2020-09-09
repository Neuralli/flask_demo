import enum
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""

    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


class gender_choice(enum.Enum):
    male = 1
    female = 2


class login_method(enum.Enum):
    EMAIL = 0
    FACEBOOK = 1
    GOOGLE = 3


class User(BaseModel, db.Model):
    """用户基本信息表"""

    __tablename__ = "user_baseinfo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用户编号
    real_name = db.Column(db.String(32))  # 用户姓名，用于用户的真实姓名
    nick_name = db.Column(db.String(32), nullable=False)  # 用户昵称
    avatar = db.Column(db.String(255))  # 用户头像
    gender = db.Column(db.String(20))  # 性别
    birthday = db.Column(db.Date)  # 生日
    mobile = db.Column(db.String(11))  # 手机号
    email = db.Column(db.String(32), unique=True, nullable=False)  # 邮箱
    is_master = db.Column(db.Boolean, default=False)  # 是否是风水大师
    interest = db.Column(db.JSON)  # 用户兴趣
    focus = db.Column(db.JSON)  # 用户兴趣
    description = db.Column(db.String(255))  # 简介
    images = db.Column(db.JSON())  # images
    details = db.Column(db.Text)  # 详情

    def to_dict(self):
        """将对象转换为字典
        article_
        """
        d = {
            "id": self.id,
            "real_name": self.real_name,
            "nick_name": self.nick_name,
            "avatar": self.avatar,
            "gender": self.gender,
            "birthday": self.birthday,
            "mobile": self.mobile,
            "email": self.email,
            "description": self.description,
        }
        return d


class UserAuth(BaseModel, db.Model):
    """用户权限表"""
    __tablename__ = "user_auths"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    identity_type = db.Column(db.Enum(login_method))  # 0:EMAIL，1:FACEBOOK，2:GOOGLE
    identifier = db.Column(db.String(32))  # 登录唯一标识
    credential = db.Column(db.String(100))  # 密码凭证（站内的保存密码，站外的不保存，保存TOKEN）
    verified = db.Column(db.SmallInteger)  # 判断是否通过验证（默认为0未通过验证，通过验证后为1)
    create_ip = db.Column(db.String(32))  # 注册IP
    last_login_ip = db.Column(db.String(32))  # 最后登录IP

    def check_password(self, password):
        check_password_hash(self.credential, password)