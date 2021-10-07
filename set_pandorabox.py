import os

import paramiko
import requests
import time

HOST = '192.168.1.1'
USER = 'root'
PASSWORD = '09272021'
URL = 'http://192.168.1.1/'
PORT = 22
CMD_NK4C = "ash --login -c 'sh nk4conf.sh'"


class AutoSetPandoraBox:
    def __init__(self):
        self.url = URL
        self.hostname = HOST
        self.username = USER
        self.password = PASSWORD
        self.port = PORT
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
            print("出错了：", e)
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
            # print("出错了：", e)
            return 500
        else:
            result = stdout.read()
            if not result:
                result = stderr.read()
            time.sleep(15)
            return result

    def access_web(self):
        """
        判断路由器是否重启成功
        :return:
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
        try:
            r = requests.get(url=self.url, headers=headers, timeout=5)
        except Exception as e:
            # print("出错了:", e)
            return 500
        return r.status_code

    @staticmethod
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

    def __del__(self):
        self.ssh.close()


def main():
    instance = AutoSetPandoraBox()
    if instance.connect_ssh() == 500:
        return 500
    else:
        instance.exec_sh(CMD_NK4C)
        while True:
            if instance.access_web() != 403:
                print("路由器正在重启...")
                time.sleep(10)
            else:
                print("启动【创翼客户端】拨号...")
                instance.start_nk()
                break


if __name__ == '__main__':
    main()
