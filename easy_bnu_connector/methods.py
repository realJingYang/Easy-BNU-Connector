# -*- coding: UTF-8 -*-
# Easy-BNU-Connector v0.2.4
# File: easy_bnu_connector\methods.py
# Author: GasinAn
# License: GNU General Public License v3.0

import os
import re
try:
    import _thread
except:
    import thread as _thread
try:
    import tkinter
except:
    import Tkinter as tkinter

from requests import request

import binascii
import hashlib
import hmac

__all__ = ('os', 're', '_thread', 'tkinter', 'request',
           'ZH_CN', 'md5', 'sha1', 'base64_encode', 'x_encode', 'DEVICE')

_ALPHA = 'LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA'
ALPHA = r'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
ZH_CN = {'ACIDIsEmpty': '缺少ACID',
         'ACIDIsRequired': '缺少ACID',
         'AuthInfoError': '刷新页面后再次登录',
         'AuthResaultTimeoutErr': 'Portal服务请求超时',
         'BSSIDIsEmpty': '缺少BSSID',
         'BrowserVersionError': '请使用 Chrome 浏览器或 360 浏览器极速模式',
         'BxAddUserErr': '添加用户失败，请联系管理员',
         'BxResaultTimeoutErr': '北向接口服务器异常，请查看日志或检查北向接口服务',
         'CHALLENGE failed, BAS respond timeout.': '网络连接超时，请稍后重试',
         'CasUsernameIsEmpty': '获取CAS用户名失败',
         'ChallengeExpireError': 'Challenge时间戳错误',
         'CheckServerTimestamp': '检查服务器时间',
         'CreateVisitorError': '创建访客失败',
         'E0000': '登录成功',
         'E2401': 'User-Request',
         'E2402': 'Lost-Carrier',
         'E2404': 'Idle-Timeout',
         'E2405': 'Session-Timeout',
         'E2406': 'Admin-Reset',
         'E2407': 'Admin-Reboot',
         'E2408': 'Port-Error',
         'E2409': 'NAS-Error',
         'E2410': 'NAS-Request',
         'E2411': 'NAS-Reboot',
         'E2412': 'Port-Unneeded',
         'E2413': 'Port-Preempted',
         'E2414': 'Port-Suspended',
         'E2415': 'Service-Unavailable',
         'E2416': 'Callback',
         'E2417': 'User-Error',
         'E2531': '用户不存在',
         'E2532': '您的两次认证的间隔太短,请稍候10秒后再重试登录',
         'E2533': '密码错误次数超过限制，请5分钟后再重试登录',
         'E2534': '有代理行为被暂时禁用',
         'E2535': '认证系统已经被禁用',
         'E2536': '授权已过期',
         'E2553': '帐号或密码错误',
         'E2601': '您使用的不是专用客户端,IPOE-PPPoE混杂模式请联系管理员重新打包客户端程序',
         'E2602': '您还没有绑定手机号或绑定的非联通手机号码',
         'E2606': '用户被禁用',
         'E2607': '接口被禁用',
         'E2611': '您当前使用的设备非该账号绑定设备 请绑定或使用绑定的设备登入',
         'E2613': 'NAS PORT绑定错误',
         'E2614': 'MAC地址绑定错误',
         'E2615': 'IP地址绑定错误',
         'E2616': '账户余额不足',
         'E2620': '已经在线了',
         'E2621': '已经达到授权人数',
         'E2806': '找不到符合条件的产品',
         'E2807': '找不到符合条件的计费策略',
         'E2808': '找不到符合条件的控制策略',
         'E2833': 'IP不在DHCP表中，需要重新拿地址。',
         'E2840': '校内地址不允许访问外网',
         'E2841': 'IP地址绑定错误',
         'E2842': 'IP地址无需认证可直接上网',
         'E2843': 'IP地址不在IP表中',
         'E2844': 'IP地址在黑名单中',
         'E2901': '第三方认证接口返回的错误信息',
         'E2901: (Third party 1)bind_user2: ldap_bind error': '账号或密码错误',
         'E2901: (Third party 1)ldap_first_entry error': '账号或密码错误',
         'E6500': '认证程序未启动',
         'E6501': '用户名输入错误',
         'E6502': '注销时发生错误，或没有帐号在线',
         'E6503': '您的账号不在线上',
         'E6504': '注销成功，请等1分钟后登录',
         'E6505': '您的MAC地址不正确',
         'E6506': '用户名或密码错误，请重新输入',
         'E6507': '您无须认证，可直接上网',
         'E6508': '您已欠费，请尽快充值',
         'E6509': '您的资料已被修改正在等待同步，请2钟分后再试。如果您的帐号允许多个用户上线，请到WEB登录页面注销',
         'E6510': '您的帐号已经被删除',
         'E6511': 'IP已存在，请稍后再试',
         'E6512': '在线用户已满，请稍后再试',
         'E6513': '正在注销在线账号，请重新连接',
         'E6514': '你的IP地址和认证地址不附，可能是经过小路由器登录的',
         'E6515': '系统已禁止客户端登录，请使用WEB方式登录',
         'E6516': '您的流量已用尽',
         'E6517': '您的时长已用尽',
         'E6518': '您的IP地址不合法，可能是：一、与绑的IP地址附；二、IP不允许在当前区域登录',
         'E6519': '当前时段不允许连接',
         'E6520': '抱歉，您的帐号已禁用',
         'E6521': '您的IPv6地址不正确，请重新配置IPv6地址',
         'E6522': '客户端时间不正确，请先同步时间（或者是调用方传送的时间格式不正确，不是时间戳；客户端和服务器之间时差超过2小时，括号里面内容不要提示给客户）',
         'E6523': '认证服务无响应',
         'E6524': '计费系统尚未授权，目前还不能使用',
         'E6525': '后台服务器无响应;请联系管理员检查后台服务运行状态',
         'E6526': '您的IP已经在线;可以直接上网;或者先注销再重新认证',
         'E6527': '当前设备不在线',
         'E6528': '您已经被服务器强制下线',
         'E6529': '身份验证失败，但不返回错误消息',
         'GetVerifyCode': '获取验证码',
         'INFO Error锛宔rr_code=2': '设备不在认证范围内',
         'INFOFailedBASRespondTimeout': 'BAS无响应',
         'IPHasBeenOnlinePleaseLogout': '您的设备已经在线，不可重复提交',
         'Info': '信息',
         'IpAlreadyOnlineError': '本机IP已经使用其他账号登陆在线了',
         'IsEvokingWeChat': '正在唤起微信...',
         'LimitDomainErr': '请使用中科院允许的邮箱进行登录',
         'LogoutOK': 'DM下线成功',
         'MACIsEmpty': '缺少MAC',
         'MemoryDbError': 'SRun认证服务(srun_portal_server)无响应',
         'MissingRequiredParametersError': '登录失败，请联系网络管理员',
         'NasTypeNotFound': 'NAS设备不存在',
         'NoAcidError': '网络设备出问题，请稍候',
         'NoResponseDataError': '无响应数据',
         'NotOnlineError': '当前设备不在线',
         'OK': '确认',
         'OtpCodeCheckError': '口令验证失败',
         'OtpCodeHasBeenUsed': '动态码已被使用',
         'OtpServerError': '身份验证器服务故障',
         'PhoneNumberError': '手机号错误',
         'ProvisionalReleaseFail': '临时放行失败',
         'S': '秒',
         'SendVerifyCodeOK': '验证码发送成功',
         'SignError': '签名错误',
         'SpeedLimitError': '认证请求太频繁，请稍后10s重试',
         'SrunPortalServerError': 'Portal服务请求错误',
         'SsoServerError': '单点登陆服务异常，请检查服务',
         'TheServerIsNotResponding': 'The service waits for a timeout, please try again later',
         'TimestampError': '时间戳错误',
         'TokenError': '验证码发送失败',
         'TokenIsEmpty': '缺少Token',
         'TypeError': '加密类型错误',
         'TypeIsEmptyOrError': '微信请求类型为空或错误',
         'UserMustModifyPassword': '您的密码比较简单或已长时间未修改，存在安全隐患，请登录自服务重置您的密码',
         'VcodeError': '验证码错误',
         'VcodeTooOftenError': '两次间隔时间太短',
         'VerifyCodeError': '验证码错误',
         'Wait': '请稍等...',
         'WeChatOptionNotFound': '未找到微信配置',
         'YouAreNotOnline': '该设备不在线',
         'ZkNetworkError': '科技云服务异常',
         'ZkUserError': '登录中国科技云通行证的账号无效，请检查账号是否正确'}

try:
    int_ = long
except:
    int_ = int

try:
    chr_ = unichr
except:
    chr_ = chr

def md5(n, t):
    return hmac.new(t.encode(), n.encode(), hashlib.md5).hexdigest()

def sha1(s):
    return hashlib.sha1(s.encode()).hexdigest()

def base64_encode(s):
    _base64_encode = binascii.b2a_base64(s.encode('UTF-8'), newline=False).decode()
    for k in range(64):
        _base64_encode = _base64_encode.replace(ALPHA[k], chr_(k+256))
    for k in range(64):
        _base64_encode = _base64_encode.replace(chr_(k+256), _ALPHA[k])
    return _base64_encode

def char_code_at(a, i):
    try:
        return ord(a[i])
    except:
        return 0

def int32(num):
    return (int_(num)+2147483648)%4294967296-2147483648

def uint32(num):
    return int_(num)%4294967296

def s(a, b):
    c = len(a)
    v = []
    for i in range(0, c, 4):
        ord_0 = char_code_at(a, i)
        ord_1 = char_code_at(a, i+1)
        ord_2 = char_code_at(a, i+2)
        ord_3 = char_code_at(a, i+3)
        v.append(ord_0|ord_1<<8|ord_2<<16|ord_3<<24)
    if b:
        v.append(c)
    return v

def x_encode(str_, key):
    if str_ == '':
        return ''
    v = s(str_, True)
    k = s(key, False)
    if len(k) < 4:
        k += (4-len(k))*[0]
    n = len(v)-1
    z = v[n]
    c = -1640531527
    q = int_(6+52/(n+1))
    d = 0
    for _ in range(q):
        d = int32(d+c)
        e = int32(uint32(d)>>2)&3
        for p in range(n):
            y = v[p+1]
            m = int32(uint32(z)>>5)^int32(y<<2)
            m += (int32(uint32(y)>>3)^int32(z<<4))^(d^y)
            try:
                m += int32(k[(int32(p)&3)^e])^z
            except:
                m += z
            v[p] = int32(v[p]+m)
            z = v[p]
        y = v[0]
        m = int32(uint32(z)>>5)^int32(y<<2)
        m += (int32(uint32(y)>>3)^int32(z<<4))^(d^y)
        try:
            m += int32(k[(int32(n)&3)^e])^z
        except:
            m += z
        v[n] = int32(v[n]+m)
        z = v[n]
    a = ''
    for v_i in v:
        chr_0 = chr_(v_i&255)
        chr_1 = chr_(int32(uint32(v_i)>>8)&255)
        chr_2 = chr_(int32(uint32(v_i)>>16)&255)
        chr_3 = chr_(int32(uint32(v_i)>>24)&255)
        a += chr_0+chr_1+chr_2+chr_3
    return a