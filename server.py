import socket
import threading
import time

from myThread import myThread, tasks, timer, working_thread


class thread_pool(threading.Thread):
    def __init__(self,max_connection):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.log_name = self.get_log_name()
        self.max_connection=max_connection
        self.start()

    def get_log_name(self):
        now_time = time.localtime()
        log_name = "log/" + str(now_time.tm_year) + "-" + str(
            now_time.tm_mon) + "-" + str(now_time.tm_mday) + "-" + str(
                now_time.tm_hour) + "-" + str(now_time.tm_min) + "-" + str(
                    now_time.tm_sec) + ".txt"
        return log_name

    def run(self):
        #创建线程
        for i in range(self.max_connection):
            myThread(self.log_name)
        while True:
            #每隔1s打印
            timer.acquire(timeout=1)
            working_thread_cnt = len(working_thread)
            print("\n")
            print("Working thread: " + str(working_thread_cnt) +
                  " ; Free thread: " + str(self.max_connection - working_thread_cnt) +
                  " ; Waiting request: " + str(tasks.qsize()))
            print("working_thread list: ",working_thread,"\n")



def main():
    max_connection = int(input("输入最大线程数："))
    #max_connection = 10
    port = 8989

    Server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Server_Socket.bind(('0.0.0.0', port))
    Server_Socket.listen(port)

    #实例化线程库
    thread_pool(max_connection)
    #打开监听
    while True:
        try:
            client, address = Server_Socket.accept()
            print("\n")
            print('Connected to: ', address)
            print(tasks.qsize(),working_thread)
            #加入任务列表：
            tasks.put(client)
            print(tasks.qsize(),working_thread)


        except KeyboardInterrupt:
            print('Server closed')
            break


if __name__=="__main__":
    main()
