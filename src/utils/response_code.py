# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author         :  Nova
@Version        :  v1.o
------------------------------------
@File           :  response_code.py
@Description    :  返回码枚举类
@CreateTime     :  2020/7/2 14:00
------------------------------------
@ModifyTime     :
"""


class Code:
    OK = "200"
    DBERR = "4001"
    NODATA = "4002"
    DATAEXIST = "4003"
    DATAERR = "4004"
    SESSIONERR = "4101"
    LOGINERR = "4102"
    PARAMERR = "4103"
    USERERR = "4104"
    ROLEERR = "4105"
    PWDERR = "4106"
    REQERR = "4201"
    IPERR = "4202"
    THIRDERR = "4301"
    IOERR = "4302"
    SERVERERR = "4500"
    UNKOWNERR = "4501"
    ERROR_TOKEN = "50001"
    NO_PARAMETER = "50002"
    ERR_PERMISSOM = "5003"
    LOGIN_TIMEOUT = "50004"


error_map = {
    Code.OK: u"成功",
    Code.DBERR: u"数据库查询错误",
    Code.NODATA: u"无数据",
    Code.DATAEXIST: u"数据已存在",
    Code.DATAERR: u"数据错误",
    Code.SESSIONERR: u"用户未登录",
    Code.LOGINERR: u"用户登录失败",
    Code.PARAMERR: u"参数错误",
    Code.USERERR: u"用户不存在或未激活",
    Code.ROLEERR: u"用户身份错误",
    Code.PWDERR: u"密码错误",
    Code.REQERR: u"非法请求或请求次数受限",
    Code.IPERR: u"IP受限",
    Code.THIRDERR: u"第三方系统错误",
    Code.IOERR: u"文件读写错误",
    Code.SERVERERR: u"内部错误",
    Code.UNKOWNERR: u"未知错误",
    Code.ERROR_TOKEN: "无效token",
    Code.NO_PARAMETER: "缺少参数token",
    Code.ERR_PERMISSOM: "权限不够",
    Code.LOGIN_TIMEOUT: "登录已过期",
}
