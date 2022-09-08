########################
##########yjy###########
########################

import os


class HTTPRequest():
    RootDir = '...'
    NotFoundHtml = RootDir+'/404.html'

    def __init__(self):
        self.method = None
        self.url = None
        self.protocol = None
        self.head = dict()
        self.request_data = dict()
        self.response_line = ''
        self.response_head = dict()
        self.response_body = ''
        self.session = None
        

    def passRequestLine(self, request_line):
        header_list = request_line.split(' ')
        self.method = header_list[0].upper()
        self.url = header_list[1]
        #对于/的请求，自动添加'index.html
        if self.url == '/':
            self.url = '/index.html'
        self.protocol = header_list[2]


    # 解析请求，得到请求的信息
    def passRequest(self, request):
        request = request.decode('utf-8')
        if len(request.split('\r\n', 1)) != 2:
            return
        request_line, body = request.split('\r\n', 1)
        request_head = body.split('\r\n\r\n', 1)[0]     # 头部信息
        self.passRequestLine(request_line)
        self.passRequestHead(request_head)

        # 所有post视为动态请求
        # get如果带参数也视为动态请求
        # 解析请求的数据，然后发送到对应的处理文件上
        if self.method == 'POST':
            self.request_data = {}
            request_body = body.split('\r\n\r\n', 1)[1]
            parameters = request_body.split('&')   # 每一行是一个字段
            for i in parameters:
                if i=='':
                    continue
                key, val = i.split('=', 1)
                self.request_data[key] = val
            self.dynamicRequest(HTTPRequest.RootDir + self.url)
        if self.method == 'GET':
            if self.url.find('?') != -1:        # 含有参数的get
                self.request_data = {}
                req = self.url.split('?', 1)[1]
                s_url = self.url.split('?', 1)[0]
                parameters = req.split('&')
                for i in parameters:
                    key, val = i.split('=', 1)
                    self.request_data[key] = val
                self.dynamicRequest(HTTPRequest.RootDir + s_url)
            else:
                self.staticRequest(HTTPRequest.RootDir + self.url)

    
    # 静态请求
    def staticRequest(self, path):
        # print path
        if not os.path.isfile(path):
            f = open(HTTPRequest.NotFoundHtml, 'r')
            self.response_line = "HTTP/1.1 404 Not Found\r\n"
            self.response_head['Content-Type'] = 'text/html'
            self.response_body = f.read()
        else:
            extension_name = os.path.splitext(path)[1]  # 扩展名
            extension_set = {'.css', '.html', '.js'}
            if extension_name == '.png':
                f = open(path, 'rb')
                self.response_line = "HTTP/1.1 200 OK\r\n"
                self.response_head['Content-Type'] = 'text/png'
                self.response_body = f.read()
            elif extension_name in extension_set:
                f = open(path, 'r')
                self.response_line = "HTTP/1.1 200 OK\r\n"
                self.response_head['Content-Type'] = 'text/html'
                self.response_body = f.read()
            elif extension_name == '.py':
                self.dynamicRequest(path)
            # 其他文件不返回
            else:
                f = open(HTTPRequest.NotFoundHtml, 'r')
                self.response_line = "HTTP/1.1 404 Not Found\r\n"
                self.response_head['Content-Type'] = 'text/html'
                self.response_body = f.read()
    
    
    def dynamicRequest(self, path):
        # 区分动态和静态请求仅根据是否是.py结尾
        # 如果找不到或者后缀名不是py则输出404
        if not os.path.isfile(path) or os.path.splitext(path)[1] != '.py':
            f = open(HTTPRequest.NotFoundHtml, 'r')
            self.response_line = "HTTP/1.1 404 Not Found\r\n"
            self.response_head['Content-Type'] = 'text/html'
            self.response_body = f.read()
        else:
            # 获取文件名，并且将/替换成.
            file_path = path.split('.', 1)[0].replace('/', '.')
            self.response_line = "HTTP/1.1 200 OK\r\n"
            m = __import__(file_path)
            m.main.SESSION = self.processSession()            
            if self.method == 'POST':
                m.main.POST = self.request_data
                m.main.GET = None
            else:
                m.main.POST = None
                m.main.GET = self.request_data
            self.response_body = m.main.app()            
            self.response_head['Content-Type'] = 'text/html'
            self.response_head['Set-Cookie'] = self.Cookie