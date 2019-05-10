#! /usr/bin/python
# encoding= utf-8

import threading
import os		# os.system(), os.popen()
from time import ctime, sleep



def play_music(func, f_n):
    for i in range(3):
        print "I was listening to %s.mp3" %func
        os.system(r'start "C:\Program Files (x86)\Windows Media Player"\wmplayer.exe E:\sinhj\"%s".mp3' %f_n)
        sleep(7)



def play_film(func, f_n):
    sleep(0.01)
    print "I was seeing %s sway." %func
    # 不加 /close 会一直卡在这里，除非在其他线程结束此进程
    os.system(r'C:\"Program Files"\MPC-HC\mpc-hc64 "E:\sinhj\%s.mp4"' %f_n)
    # 在播放结束之後关闭 mpc
    print "I was seeing %s sway." %func
    os.system(r'C:\"Program Files"\MPC-HC\mpc-hc64 "E:\sinhj\%s.mp4" /close' %f_n)



def kill_mpc():
    sleep(15)
    os.system(r'taskkill /IM mpc-hc64.exe')
    sleep(15)



def ingbk(str):
    return str.decode("utf-8").encode("gbk")



str0 = '坏脾気 - 吳汶芳'
# str1 = 'Jiyeon - 1 分 1 秒'
str1 = '自転车 - オレスカバンド'

# 逗号 单个元素转换为元组 tuple
t1 = threading.Thread(target = play_music, args = (u'坏脾気', ingbk(str0)))
t2 = threading.Thread(target = play_film, args = (u'Jiyeon', ingbk(str1)))
t3 = threading.Thread(target = kill_mpc, args = ())

threads = []
threads.append(t1)
threads.append(t2)
threads.append(t3)

if __name__ == '__main__':
    print 1,    # , 换行变成空格
    print 2,
    print 3,
    a = '...'
    print a

    print type(t1)
    print isinstance(a, str)

    op = ctime()
    for t in threads:
        t.setDaemon(True)
        t.start()
    t3.join()

    sleep(3)
    os.system(r'taskkill /IM wmplayer.exe')
    os.system(r'taskkill /IM mpc-hc64.exe')
    print "Playback over.   %s ~ %s" %(op, ctime())
