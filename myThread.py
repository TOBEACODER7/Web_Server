import os
import subprocess
import threading
import time
from queue import Queue
from shlex import split
from urllib import request

from request import HTTPRequest

tasks = Queue()  #socket队列
working_thread = list()  #线程列表
timer = threading.Semaphore()  #信号量


class myThread(threading.Thread):

    def __init__(self, log_name):
        threading.Thread.__init__(self)
        self.socket = None
        self.msg = None
        self.log_name = log_name
        self.setDaemon(True)
        self.start()          

    def run(self):
        while True:
            #先打印已建立的线程：
            print("now blocking: ",self)
            
            #在此阻塞：
            self.socket = tasks.get()
            print("now running: ",self)
            #打印工作线程
            working_thread.append(self)
            timer.release()
            #解析消息
            message = self.socket.recv(8000).decode("utf-8").splitlines()
            print(message)
            print("\n")
            self.msg = message
            #确定收到消息
            if (message):
                line1 = message[0].split()
            else:
                #self.restart()
                working_thread.remove(self)
                continue
            if (len(line1) <= 1):
                #self.restart()
                working_thread.remove(self)
                continue
            
            #处理
            request = HTTPRequest(self.socket,self.log_name)
            request.passRequest(message)
            self.socket.sendall(request.response_body)

            try:
                self.socket.shutdown(2)
                self.socket.close()
            except Exception as e:
                print("socket error:", e)
            self.socket = None
            
            print("before:",working_thread)
            working_thread.remove(self)
            print("\n")
            print("after:",working_thread)
            timer.release()

            
