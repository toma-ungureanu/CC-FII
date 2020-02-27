from http.server import HTTPServer, BaseHTTPRequestHandler
import os


class Serv(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.path = None

    def do_GET(self):
        curent_path = fr'{os.path.curdir}'
        if self.path == '/':
            self.path = os.path.abspath(curent_path + r'/html/index.html')
        elif self.path == "/css/indexStyle.css":
            self.path = os.path.abspath(curent_path + r'/css/indexStyle.css')
        elif self.path == "/metrics":
            self.path = os.path.abspath(curent_path + r'/html/metrics.html')
        elif self.path == "/css/metricsStyle.css":
            self.path = os.path.abspath(curent_path + r'/css/metricsStyle.css')
        elif self.path == "/python/get_service_info.py":
            self.path = os.path.abspath(curent_path + r'/python/get_service_info.py')
        try:
            file_to_open = open(self.path).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))


httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()
