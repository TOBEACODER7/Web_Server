import os
import subprocess
import threading
import time
from queue import Queue

tasks = Queue()  #socket队列
working_thread = list()  #线程列表
sema = threading.Semaphore()  #信号量


class myThread(threading.Thread):

    def __init__(self, log_name):
        threading.Thread.__init__(self)
        self.file_handle = None
        self.proc = None
        self.socket = None
        self.msg = None
        self.log_name = log_name
        self.setDaemon(True)
        self.start()

    def run(self):
        while True:
            self.socket = tasks.get()  #取socket赋值
            working_thread.append(self)  #放到线程列表
            sema.release()  #线程可用

            message = self.socket.recv(8000).decode("utf-8").splitlines()
            self.msg = message

            filename = "index.html"
            ## filename = "/cgi-bin/calculator.html"
            if (message):
                method = message[0].split()[0]
                if (message[0].split()[1] != "/"):
                    filename = message[0].split()[1][1:]
                print(method,filename)
            else:
                self.restart()
                continue
            if (len(method) <= 1):
                self.restart()
                continue
            #加入线程进行操作：
            working_thread.append(self)
            try:
                print(method)
                if (method == 'GET'):
                    self.get()
                elif (method == 'POST'):
                    pass
                else:
                    content = b"HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n"
                    self.socket.sendall(content)
            except Exception as e:
                print("reason:", e)  # read a closed file
            
            self.restart()#清空操作
            working_thread.remove(self)
            sema.release()

    def get(self):
        
        filename = "index"  ##这里暂时先写死不管client发过来任何请求，都给他返回POST index.html
        ## filename = "/cgi-bin/calculator.html"

        filedata = open(filename+".html", "rb").read()
        message = b"HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n"
        message += b"Content-Length: " + str(
            len(filedata)).encode() + b"\r\n\r\n"
        message += filedata
        self.socket.send(message)
        #self.scoket.close()

    #用于清空操作后所赋的值
    def restart(self):
        if (self.file_handle != None):
            self.file_handle.close()
            self.file_handle = None
        if (self.socket != None):
            try:
                self.socket.shutdown(2)  #2表示禁止下次的数据读取和写入
                self.socket.close()
            except Exception as e:
                print("socket error:", e)
            self.socket = None
        if (self.proc != None and self.proc.poll() != None):
            self.proc.kill()
            self.proc = None
