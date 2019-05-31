# -*- encoding: utf-8 -*-

# for Windows

import paramiko
import os
from stat import S_ISDIR



# 表示一个远程 Linux server
class Linux_Server(object):
    def __init__(self, ipaddr, usrname, passwd, timeout=30):
        self.ipaddr = ipaddr
        self.usrname = usrname
        self.passwd = passwd
        self.timeout = timeout

        self.transport = ""
        # self.channel = ""
        # 连接失败的重试次数
        self.try_times = 3

    # 能不能连接 Windows host
    # 连接远程 Linux server
    def connect(self):
        pass

    # 断开连接
    def close(self):
        pass

    # 发送要执行的命令
    def send(self, cmd):
        pass

    # get 单个文件
    def sftp_get(self, remote_file, local_file):
        transport = paramiko.Transport(sock = (self.ipaddr, 22))
        transport.connect(username = self.usrname, password = self.passwd)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(remote_file, local_file)
        transport.close()

    # put 单个文件
    def sftp_put(self, local_file, remote_file):
        transport = paramiko.Transport(sock = (self.ipaddr, 22))
        transport.connect(username = self.usrname, password = self.passwd)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(local_file, remote_file)
        transport.close()

    # 扫描远程 Linux server 指定目录
    def scan_remote_dir(self, sftp, remote_dir):
        # 文件列表
        found_files = list()

        # 去掉路径末尾的 '/'
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        # 获取远程 Linux 指定目录的属性，遍历所有目录及文件
        dir_detl = sftp.listdir_attr(remote_dir)
        for elem in dir_detl:
            # 每一个文件或目录的路径
            _path = remote_dir + '/' + elem.filename
            # 如果是目录，则递归处理，这里用到了 stat.S_ISDIR 方法，与 Linux 中的宏的名字一致
            if S_ISDIR(elem.st_mode):
                found_files.extend(self.scan_remote_dir(sftp, _path))
            else:
                found_files.append(_path)
        return found_files
    # listdir_attr() 会列出指定目录下的所有文件或目录，并且还会列出其属性，比如 st_size, st_uid, st_gid, st_mode, st_atime, st_mtime
    # 这些属性与 linux 中的 stat 函数返回的属性类似，根据其中的 st_mode 属性来判断是一个目录还是文件，并且处理 st_mode 的方法也是与 Linux 中定义的宏一致的

    # 获取到指定目录下的所有文件之后，传输就比较简单了，依次遍历 get 即可
    def sftp_get_dir(self, remote_dir, local_dir):
        transport = paramiko.Transport(sock = (self.ipaddr, 22))
        transport.connect(username = self.usrname, password = self.passwd)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # 获取远程 Linux server 指定目录及其子目录下的所有文件
        found_files = self.scan_remote_dir(sftp, remote_dir)
        # 依次 get 每个文件
        print "get %s ..." %remote_dir
        for f_path in found_files:
            filename = f_path.split('/')[-1]
            local_f_path = os.path.join(local_dir, filename)
            print filename
            sftp.get(f_path, local_f_path)

    # 扫描本地 Windows host 指定目录
    def scan_local_dir(self, local_dir):
        # 保存所有文件的列表
        found_files = list()

        # 获取本地 Windows 指定目录属性，遍历所有目录及文件
        dir_detl = os.listdir(local_dir)
        for elem in dir_detl:
            # 每一个文件或目录的路径
            filename = os.path.join(local_dir, elem)
            # 如果是目录，则递归处理
            if os.path.isdir(elem):
                found_files.extend(self.scan_local_dir(filename))
            else:
                found_files.append(filename)
        return found_files

    def sftp_put_dir(self, local_dir, remote_dir):
        transport = paramiko.Transport(sock = (self.ipaddr, 22))
        transport.connect(username = self.usrname, password = self.passwd)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # 去掉路径末尾的 '/'
        if remote_dir[-1] == '/':
            remote_dir = remote_dir[0:-1]

        # 获取本地 Windows host 指定目录及其子目录下的所有文件
        found_files = self.scan_local_dir(local_dir)

        # 依次 put 每个文件
        print "put %s ..." %local_dir
        for f_path in found_files:
            filename = os.path.split(f_path)[-1]
            remote_f_path = remote_dir + '/' + filename
            print filename
            sftp.put(f_path, remote_f_path)



if __name__ == "__main__":
    ipaddr = "10.120.211.73"
    usrname = "root"
    passwd = "Mima2013!"

    # remote_file = "/opt/foo.txt"
    remote_path = "/root"           # 不能用 "~"
    # local_file = r"E:\Field\tmp.txt"
    local_path = r".\testsftp"      # 需要手动建目录

    remote_host = Linux_Server(ipaddr, usrname, passwd)

    # 将远端的 foo.txt get 到本地
    # remote_host.sftp_get(remote_file, local_file)

    # for line in open(r"E:\Field\tmp.txt"): print line,

    # 将本地的 tmp.txt put 到远端
    # remote_host.sftp_put(local_file, remote_file)

    # 将 Linux remote_path 目录 get 到 Windows local_path 目录
    remote_host.sftp_get_dir(remote_path, local_path)

    # 将 Windows local_path 目录 put 到 Linux remote_path 目录
    # remote_host.sftp_put_dir(remote_path, local_path)

    # 如果要保持与远端的目录结构一致，就需要在 local_dir 中创建子目录
    # 只测试了 get

    # 考虑目录、文件同一个方法处理
