from enum import Flag
import json, jsonschema
from http.server import HTTPServer, BaseHTTPRequestHandler

USERS_LIST = [
]


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def _set_response(self, status_code=200, body=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body if body else {}).encode('utf-8'))

    def _pars_body(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        return json.loads(self.rfile.read(content_length).decode('utf-8'))  # <--- Gets the data itself

    def do_GET(self):
        global USERS_LIST
        if self.path == '/reset':
            USERS_LIST = [   {
                        "id": 1,
                        "username": "theUser",
                        "firstName": "John",
                        "lastName": "James",
                        "email": "john@email.com",
                        "password": "12345",}]
            self._set_response(status_code=200, body=USERS_LIST)
        elif self.path == '/users':
            self._set_response(status_code=200, body=USERS_LIST)
        elif '/user/' in self.path:
            for element in USERS_LIST:
                if self.path[6:] == element['username']:
                    self._set_response(status_code=200, body=element)
                    return
            self._set_response(status_code=400, body={"error": "User not found"})

    def do_POST(self):
        global USERS_LIST
        if '/user/' in self.path:
            data = self._pars_body()
            if not self.validateJSON(data=data):
                self._set_response(status_code=400, body={})
                return
            for element in USERS_LIST:
                if element['id'] == data['id']:
                    self._set_response(status_code=400, body={})
            USERS_LIST.append(data)
            self._set_response(status_code=201, body=USERS_LIST)
            
    def do_PUT(self):
        self._set_response(418)

    def do_DELETE(self):
        if '/user/' in self.path:
            for element in USERS_LIST:
                if int(self.path[6:]) == element['id']:
                    self._set_response(status_code=200, body={})
                    return
            self._set_response(status_code=404, body={"error": "User not found"})

    def validateJSON(self, data):
        schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "username": {"type": "string"},
            "firstName": {"type": "string"},
            "lastName": {"type": "string"},
            "email": {"type": "string"},
            "password": {"type": "string"}
        },
        "required": ["name", "username", "firstName", "lastName", "email", "password"],
                }
        try:
            jsonschema.validate(data, schema=schema)
            return True
        except:
            return False


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, host='localhost', port=8000):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
