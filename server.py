import socket
import threading
import time
from webbrowser import get

from myThread import myThread, sema, tasks, working_thread

max_connection = 5
port = 8989

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('0.0.0.0', port))
socket.listen(port)


class thread_pool(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.log_name = self.get_log_name()
        self.start()
        

    def get_log_name(self):
        now_time = time.localtime()
        log_name = "log/" + str(now_time.tm_year) + "-" + str(
            now_time.tm_mon) + "-" + str(now_time.tm_mday) + "-" + str(
                now_time.tm_hour) + "-" + str(now_time.tm_min) + "-" + str(
                    now_time.tm_sec) + ".txt"
        return log_name

    def run(self):
        for i in range(max_connection):
            myThread(self.log_name)
        while True:
            for i in range(10):
                if (len(working_thread) >= max_connection
                        and max_connection != 0 and (not tasks.empty())):
                    print("shutdown")
                    working_thread[0].restart()
            sema.acquire(timeout=1)

            working_thread_cnt = len(working_thread)
            print("now working thread: " + str(working_thread_cnt) +
                  " ; free thread: " +
                  str(max_connection - working_thread_cnt) +
                  " ; now waiting request: " + str(tasks.qsize()))


def SendToClient(client):
    print(client.recv(1024).decode().splitlines()[0].split())
    filename = "index.html"  ##这里暂时先写死不管client发过来任何请求，都给他返回POST index.html
    ## filename = "/cgi-bin/calculator.html"
    filedata = open(filename, "rb").read()
    message = b"HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n"
    message += b"Content-Length: " + str(len(filedata)).encode() + b"\r\n\r\n"
    message += filedata
    client.send(message)
    client.close()


#实例化线程库
thread_pool()
#打开监听
while True:
    try:
        client, address = socket.accept()
        print('Connected to', address)
        ## there connect has been set up

        #加入线程池：
        tasks.put(client)
        
        #SendToClient(client)

    except KeyboardInterrupt:
        print('Server closed')
        break
