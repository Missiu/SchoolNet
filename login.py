import platform
import subprocess
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
    """使用 ping 命令检测网络连接"""
    system = platform.system()
    if system == "Windows":
        cmd = ["ping", "-n", "1", "www.baidu.com"]
    else:
        cmd = ["ping", "-c", "1", "www.baidu.com"]

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0  # 返回码为 0 表示网络连接正常
    except Exception as e:
        print("Ping 检测失败:", str(e))
        return False


def parse_response(response):
    """解析并返回响应内容中的 result 状态"""
    response.encoding = 'utf-8'
    content = response.text.encode().decode("unicode_escape").encode('raw_unicode_escape').decode()
    status_index = content.find('"result":"')
    if status_index == -1:
        return None  # 如果未找到 result 字段，返回 None
    return content[status_index + 10:status_index + 17]


def check_and_login(session):
    """
    检查当前在线状态，并根据状态执行相应的操作。
    如果当前处于离线状态，尝试登录。
    """
    try:
        # 检查在线状态
        response = session.post(url=checkStatusUrl, headers=header, data=dataCheck)
        status = parse_response(response)

        if status in ['wait', 'success']:
            print(get_current_time(), "当前处于在线状态。")
            return True  # 在线状态
        else:
            print(get_current_time(), "当前已经下线，正在尝试登录！")
            # 尝试登录
            login_response = session.post(url=loginUrl, headers=header, data=dataLogin)
            login_status = parse_response(login_response)

            if login_status == 'success':
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


def monitor_online_status(session):
    """
    持续监测在线状态，如果掉线则尝试重新登录。
    """
    while True:
        # 检查网络连接状态
        if not is_internet_connected():
            print(get_current_time(), "当前无网络连接，请检查网络。")
            time.sleep(5)
            continue

        # 检查在线状态
        response = session.post(url=checkStatusUrl, headers=header, data=dataCheck)
        status = parse_response(response)

        if status in ['wait', 'success']:
            print(get_current_time(), "仍处于在线状态。")
        else:
            print(get_current_time(), "检测到下线，正在重新登录...")
            if not check_and_login(session):
                print(get_current_time(), "重新登录失败，稍后重试。")

        # 隔一段时间再次检查状态
        time.sleep(5)


def main():
    with requests.Session() as session:
        while True:
            # 检查网络状态
            if not is_internet_connected():
                print(get_current_time(), "当前无网络连接，请检查网络。")
                # 登录尝试
                for attempt in range(1, 11):  # 重试10次
                    if check_and_login(session):
                        # 登录成功后，开始监测在线状态
                        monitor_online_status(session)
                        break  # 跳出重试循环
                    else:
                        print(get_current_time(), f"登录失败，重试第 {attempt} 次...")
                        time.sleep(5)  # 等待5秒后重试
                else:
                    # 连续10次登录失败
                    print(get_current_time(), "连续10次尝试登录失败，休眠1小时后重试。")
                    time.sleep(3600)  # 休眠1小时


if __name__ == "__main__":
    main()
