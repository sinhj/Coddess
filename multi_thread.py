#coding=utf-8
import threading
import os
from time import ctime, sleep



def play_music(func):
    for i in range(3):
        print "I was listening to %s.mp3         %s" %(func, ctime())
        os.system(r'start "C:\Program Files (x86)\Windows Media Player"\wmplayer.exe C:\Users\Public\Music\"Sample Music"\Kalimba.mp3')
        sleep(7)



def play_film(func):
    sleep(0.01)
    print "I was seeing %s                %s" %(func, ctime())
    # 不加 /close 会一直卡在这里，除非在其他线程结束此进程
    os.system(r'C:\"Program Files"\MPC-HC\mpc-hc64 C:\Users\swx614709\Videos\config.mp4')
    # 在播放结束之後关闭 mpc
    print "I was seeing %s                %s" %(func, ctime())
    os.system(r'C:\"Program Files"\MPC-HC\mpc-hc64 C:\Users\swx614709\Videos\config.mp4 /close')



def kill_mpc():
    sleep(15)
    os.system(r'taskkill /IM mpc-hc64.exe')
    sleep(15)



# 逗号 单个元素转换为元组 tuple
t1 = threading.Thread(target = play_music, args = (u'Kalimba', ))
t2 = threading.Thread(target = play_film, args = (u'config.mp4', ))
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

    for t in threads:
        t.setDaemon(True)
        t.start()
    t3.join()

    sleep(3)
    os.system(r'taskkill /IM wmplayer.exe')
    os.system(r'taskkill /IM mpc-hc64.exe')
    print "Playback over.                         %s" % ctime()
