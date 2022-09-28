import os
import subprocess
import time
from argparse import FileType
from socket import socket


class HTTPRequest():
    def __init__(self,socket,log_name):
        print('@@@enter init')
        self.response_body = ''             #响应主题
        self.socket = socket
        self.proc = None
        self.method = None
        self.msg = None
        self.log_name = log_name
        self.filesize = 0
        self.status_code = 200

    # 日志书写（文件大小）
    def write_log(self):
        content = self.msg[1].split(":")[1].replace(" ", "")
        content = content + "--"
        content = content + "[" + str(time.localtime().tm_year) + "-" + str(
            time.localtime().tm_mon) + "-" + str(
                time.localtime().tm_mday) + "-" + str(
                    time.localtime().tm_hour) + "-" + str(
                        time.localtime().tm_min) + "-" + str(
                            time.localtime().tm_sec) + "]"
        content = content + " \"" + self.msg[0].split("/")[0].replace(" ",
                                                                    "") + " "
        content = content + " " + self.msg[0].split(" ")[1].replace(" ",
                                                                    "") + "\" "
        content = content + str(self.filesize) + " "
        content = content + str(self.status_code) + " "
        for i in self.msg:
            if (i.split(" ")[0] == "Referer:"):
                content = content + i.split(" ")[1].replace(" ", "")

        content = content + "\n"
        with open(self.log_name, "a") as f:
            f.write(content)
    
    # 解析请求，得到请求的信息
    def passRequest(self,request):
        ## print("@@enter passrequest")
        request = request
        request_line = request[0].split()
        method = request_line[0]
        filename = "index.html"
        if(request_line[1] != '/'):
            filename = request_line[1][1:]
        self.msg = request

        self.filesize = os.path.getsize(filename)
        if method == 'POST':
            args = request[-1]

            if(os.path.isfile(filename)):
                ## print('$$$'+filename)
                
                ## print(filename)
                cmd = 'python3 ' + filename + ' "' + args + '" "' + self.socket.getsockname()[0] + '" "' + str(self.socket.getsockname()[1]) + '"'
                
                self.proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
                self.proc.wait()

                content = b"HTTP/1.1 200 OK\r\nContent-Type: text/html;charset=utf-8\r\n"
                file1 = open('res.html', 'rb').read()
                content += b"Content-Length: " + str(len(file1)).encode('utf-8') + b"\r\n\r\n"
                content += file1
                self.status_code = 200

            else:
                content = b"HTTP/1.1 403 Forbidden\r\nContent-Type: text/html;charset=utf-8\r\n"
                page = b''
                self.file_handle = open("403.html", "rb")
                for line in self.file_handle:
                    page += line
                content += b'\r\n'
                content += page
                self.status_code = 403
            
            content += b"\r\n"
            self.response_body = content
              ## filesize = os.path.getsize(filename)

        if method == 'GET':
            ## print('@@'+filename)
            if(os.path.isfile(filename)):
                print('@'+filename)
                file = open(filename, 'rb').read()
                FileType = filename.split('.')[-1]
                content = b"HTTP/1.1 200 OK\r\nContent-Type: text/"+ FileType.encode() + b";charset=utf-8\r\n"
                content += b"Content-Length: " + str(len(file)).encode('utf-8') + b"\r\n\r\n"
                content += file
                self.status_code = 200
            else:
                content = b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html;charset=utf-8\r\n"
                filename = "404.html"
                self.status_code = 403
            content += b"\r\n"
            self.response_body = content

        if method == 'HEAD':
            ## print('@@'+filename)
            if(os.path.isfile(filename)):
                print('@'+filename)
                file = open(filename, 'rb').read()
                FileType = filename.split('.')[-1]
                content = b"HTTP/1.1 200 OK\r\nContent-Type: text/"+ FileType.encode() + b";charset=utf-8\r\n"
                content += b"Content-Length: " + str(len(file)).encode('utf-8') + b"\r\n\r\n"
                self.status_code = 200
            else:
                content = b"HTTP/1.1 404 Not Found\r\nContent-Type: text/html;charset=utf-8\r\n"
                filename = "404.html"
                self.status_code = 403
            content += b"\r\n"
            self.response_body = content

        self.write_log()
    
   
    