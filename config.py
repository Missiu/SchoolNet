header = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Length': '120',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 非必要请勿启用
    # 'Cookie': '',
    'Host': '172.16.3.19',
    'Origin': 'http://172.16.3.19',
    # 以下数据填写Post请求中的内容
    'Referer': 'http://172.16.3.19/eportal/success.jsp?userIndex=37653134356561663565633665383538656237393565623830396161613063385f31302e31362e3133322e3230335f3231303530323130xx&keepaliveInterval=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
}

dataLogin = {
    # 以下内容从Post请求中获取，密码填写加密后的密码
    # todo 你的账号密码
    'userId': '210xxxxxx',
    'password': 'Aa123456',
    'service': 'dianxin',    # 例如`dianxin` `yidong`
    'queryString': 'wlanacname=SuShe-HeXin&wlanuserip=10.16.132.89&wlanparameter=fc3497954236&nasip=172.16.10.252',
    # 不用填写以下内容
    'operatorPwd': '',
    'operatorUserId': '',
    'validcode': '',
    # 填写的是否为加密密码
    'passwordEncrypt': 'false', # 如果密码未加密，更改为'false'
    # 填写Post内容
    'userIndex': '37653134356561663565633665383538656237393565623830396161613063385f31302e31362e3133322e3230335f3231303530323130xx'
}

dataCheck = {
    # 填写Post内容
    'userIndex': '37653134356561663565633665383538656237393565623830396161613063385f31302e31362e3133322e3230335f3231303530323130xx'
}

# 填写登录界面URL，以下默认是宜宾学院登录地址。如需修改，建议用批量字符串替换功能替换项目所有IP
loginUrl = 'http://172.16.3.19/eportal/InterFace.do?method=login'
checkStatusUrl = 'http://172.16.3.19/eportal/InterFace.do?method=getOnlineUserInfo'
