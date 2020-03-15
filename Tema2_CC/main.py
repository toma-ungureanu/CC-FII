from http.server import HTTPServer, BaseHTTPRequestHandler
import json

# open json file and give it to data variable as a dictionary
with open("db.json") as data_file:
    data = json.load(data_file)


# Defining a HTTP request Handler class
class ServiceHandler(BaseHTTPRequestHandler):
    # sets basic headers for the server
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        length = int(self.headers['Content-Length'])
        content = self.rfile.read(length)
        temp = str(content).strip('b\'')
        self.end_headers()
        return temp

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            response = json.dumps(data).replace("\"", "").encode()
        else:
            resource = str(self.path).replace("/", "")
            if resource in data:
                self.send_response(200)
                response = json.dumps(data[resource]).replace("\"", "").encode()
            else:
                self.send_response(404)
                response = "Resource not found!".encode()

        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(response)

    def do_VIEW(self):
        display = {}
        temp = self._set_headers()
        if temp in data:
            display[temp] = data[temp]
            self.wfile.write(json.dumps(display).encode())
        else:
            error = "NOT FOUND!"
            self.wfile.write(bytes(error, 'utf-8'))
            self.send_response(404)

    def do_POST(self):
        temp = self._set_headers()
        key = 0
        for key, value in data.items():
            pass
        index = int(key) + 1
        data[str(index)] = str(temp)
        with open("db.json", 'w+') as file_data:
            json.dump(data, file_data)

    # self.wfile.write(json.dumps(data[str(index)]).encode())

    def do_PUT(self):
        temp = self._set_headers()
        x = temp[:1]
        y = temp[2:]
        if x in data:
            data[x] = y
            with open("db.json", 'w+') as file_data:
                json.dump(data, file_data)
        # self.wfile.write(json.dumps(data[str(x)]).encode())
        else:
            error = "NOT FOUND!"
            self.wfile.write(bytes(error, 'utf-8'))
            self.send_response(404)

    def do_DELETE(self):
        temp = self._set_headers()
        if temp in data:
            del data[temp]
            with open("db.json", 'w+') as file_data:
                json.dump(data, file_data)
        else:
            error = "NOT FOUND!"
            self.wfile.write(bytes(error, 'utf-8'))
            self.send_response(404)


# Server Initialization
server = HTTPServer(('127.0.0.1', 8080), ServiceHandler)
server.serve_forever()
