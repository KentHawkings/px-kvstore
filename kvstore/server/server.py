import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import wraps
from kvstore.store import KeyValueStore

def _validate_request(func):
    """Decorator to validate the request path and extract the key."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        key = self._get_key_from_path()
        if key is None:
            self._send_error_response(404, 'Not Found')
            return
        if not key:
            self._send_error_response(400, 'Key is missing')
            return
            
        return func(self, key, *args, **kwargs)
    return wrapper

class StoreHTTPRequestHandler(BaseHTTPRequestHandler):
    _store = KeyValueStore()
    API_BASE_PATH = '/store/'

    @_validate_request
    def do_GET(self, key):
        value = self._store[key]
        if value is not None:
            self._send_json_response(200, {'key': key, 'value': value})
        else:
            self._send_error_response(404, 'Key not found')

    @_validate_request
    def do_POST(self, key):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            value = data['value']
        except (TypeError, json.JSONDecodeError, KeyError):
            self._send_error_response(400, 'Invalid JSON or missing "value" field')
            return

        self._store[key] = value
        self._send_json_response(201, {'key': key, 'value': value})

    @_validate_request
    def do_DELETE(self, key):
        if self._store.pop(key) is not None:
            self.send_response(204)
            self.end_headers()
        else:
            self._send_error_response(404, 'Key not found')
    
    def _get_key_from_path(self):
        """Extracts the key from the request path if it's a valid API path."""
        if self.path.startswith(self.API_BASE_PATH):
            return self.path[len(self.API_BASE_PATH):]
        return None

    def _send_error_response(self, status, message):
        self._send_json_response(status, {'error': message})

    def _send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def run_server(server_class=HTTPServer, handler_class=StoreHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever() 