import os

import paramiko
import requests
import time

HOST = '192.168.1.1'
USER = 'root'
PASSWORD = '09272021'

ROUTE_URL = 'http://' + HOST
BAIDU_URL = 'https://www.baidu.com/'
# 路由器内部命令
CMD_NK4C = "ash --login -c 'sh nk4conf.sh'"


class AutoPandoraBox:
    def __init__(self, host, user, password, port=22):
        """
        初始化参数
        :param host:
        :param user:
        :param password:
        :param port:
        """
        self.hostname = host
        self.username = user
        self.password = password
        self.port = port
        self.ssh = paramiko.SSHClient()

    def connect_ssh(self):
        """
        ssh 连接路由器
        :return:
        """
        print("正在登录路由器...")
        try:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.load_system_host_keys()
            self.ssh.connect(hostname=self.hostname, username=self.username, password=self.password, port=self.port)
        except Exception as e:
            # print("登录路由器错误：", e)
            # print("路由器未连接...")
            time.sleep(5)
            return 500

    def exec_sh(self, cmd):
        """
        执行 ssh 命令
        :return:
        """
        print("正在启动自动程序...")
        try:
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
        except Exception as e:
            print("执行路由器命令错误：", e)
            return 500
        else:
            result = stdout.read()
            if not result:
                result = stderr.read()
            time.sleep(15)
            return result

    def __del__(self):
        self.ssh.close()


def start_nk():
    """
    启动 NetKeeper
    :return:
    """
    app = "C:\\Program Files\\NetKeeper\\NetKeeper.exe"
    if os.path.exists(app):
        os.startfile(app)
    else:
        print("没有找到创翼客户端")


def access_internet(url):
    """
    判断路由器是否重启成功
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    }

    try:
        r = requests.get(url=url, headers=headers, timeout=5)
    except Exception as e:
        # print("访问网络错误:", e)
        return 500
    return r.status_code


def dial_net():
    """
    路由器拨号模块
    :return:
    """
    instance = AutoPandoraBox(HOST, USER, PASSWORD)
    if instance.connect_ssh() == 500:
        # 连接路由器出错
        print("未连接到路由器...")
        print("请检查路由器...")
        print("正在退出...")
        time.sleep(3)
        return 500
    else:
        # 执行路由器内部命令
        instance.exec_sh(CMD_NK4C)
        while True:
            # 等待路由器重启
            if access_internet(ROUTE_URL) != 403:
                print("路由器正在重启...")
                time.sleep(10)
            else:
                # 启动创翼客户端
                print("启动【创翼客户端】...")
                start_nk()
                break


def main():
    net_code = access_internet(BAIDU_URL)
    if net_code == 200:
        print("外网已连接，不需要拨号，正在退出...")
        time.sleep(3)
        return
    else:
        dial_net()
        return


if __name__ == '__main__':
    main()
