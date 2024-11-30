import requests
import time
import random
import config  # 导入配置文件

# 从配置文件中获取数据
dataLogin = config.dataLogin
dataCheck = config.dataCheck
loginUrl = config.loginUrl
checkStatusUrl = config.checkStatusUrl
header = config.header  # 请求头信息


def get_current_time():
    """返回当前时间的字符串"""
    return time.asctime(time.localtime(time.time()))


def is_internet_connected():
    """使用 HTTP 请求检测网络连接"""
    try:
        # 请求百度以判断网络连接状态
        response = requests.get("https://www.baidu.com", timeout=3, proxies={"http": None, "https": None})
        print(get_current_time(), "网络连接成功")
        time.sleep(5)  # 等待5秒后重试
        return response.status_code == 200
    except requests.RequestException:
        print(get_current_time(), "网络连接失败")
        return False


def check_login_status():
    """检查是否登录状态"""
    try:
        response = requests.post(url=checkStatusUrl, headers=header, data=dataCheck, timeout=5)
        response.encoding = 'utf-8'
        content = response.text.encode().decode("unicode_escape").encode('raw_unicode_escape').decode()
        status_index = content.find('"result":"')

        # 根据状态判断是否在线
        return content[status_index + 10:status_index + 14] in ['wait', 'success']
    except requests.RequestException as e:
        print(get_current_time(), "网络请求失败:", str(e))
        return False


def login():
    """执行登录操作"""
    try:
        login_response = requests.post(url=loginUrl, headers=header, data=dataLogin, timeout=5)
        login_response.encoding = 'utf-8'
        login_content = login_response.text.encode().decode("unicode_escape").encode('raw_unicode_escape').decode()
        result_index = login_content.find('"result":"')

        if login_content[result_index + 10:result_index + 17] == 'success':
            print(get_current_time(), "登录成功！")
            return True  # 登录成功
        else:
            print(get_current_time(), "登录失败！")
            return False  # 登录失败
    except requests.RequestException as e:
        print(get_current_time(), "网络请求失败:", str(e))
        return False
    except Exception as e:
        print(get_current_time(), "发生异常:", str(e))
        return False


def main():
    """主逻辑，持续判断网络状态并处理登录逻辑"""
    while True:
        # 检查网络连接状态
        if not is_internet_connected():
            print(get_current_time(), "当前无网络连接，请检查网络。")
            retry_count = 0
            while retry_count < 10:
                if login():
                    break  # 登录成功，退出重试循环
                retry_count += 1
                print(get_current_time(), f"登录失败，重试第 {retry_count} 次...")
                time.sleep(5)  # 等待5秒后重试

            if retry_count >= 10:
                print(get_current_time(), "连续10次尝试登录失败，休眠1小时后重试。")
                time.sleep(3600)  # 休眠1小时

if __name__ == "__main__":
    main()
