import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from functools import wraps
from kvstore.cache.cache import LRUCache
from kvstore.store import KeyValueStore
from kvstore.database.database import Database

def _validate_request(func):
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

def _handle_internal_server_error(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            self.handle_exception(e)
            self._send_error_response(500, 'Internal Server Error')
            return
    return wrapper

class StoreHTTPRequestHandler(BaseHTTPRequestHandler):
    _store = KeyValueStore(db=Database(), cache=LRUCache(1000))
    API_BASE_PATH = '/store/'

    def handle_exception(self, e):
        import sys
        import traceback
        traceback.print_exc(file=sys.stderr)

    @_handle_internal_server_error
    @_validate_request
    def do_GET(self, key):
        value = self._store[key]
        if value is not None:
            self._send_json_response(200, {'key': key, 'value': value})
        else:
            self._send_error_response(404, 'Key not found')

    @_handle_internal_server_error
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

    @_handle_internal_server_error
    @_validate_request
    def do_DELETE(self, key):
        self._store.pop(key)
        self.send_response(204)
        self.end_headers()
    
    def _get_key_from_path(self):
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

def run_server(server_class=ThreadingHTTPServer, host='', port=8000):
    server_address = (host, port)
    webserver = server_class(server_address, StoreHTTPRequestHandler)
    print(f'Starting webserver on port {port}...')
    webserver.serve_forever() 