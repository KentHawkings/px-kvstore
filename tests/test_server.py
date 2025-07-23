import unittest
import json
import http.client
import threading
from kvstore.server import run_server
from kvstore.server.server import StoreHTTPRequestHandler

import os
import sys

class TestStoreHTTPServer(unittest.TestCase):
    _server_thread = None

    @classmethod
    def setUpClass(cls):
        cls.stderr_original = sys.stderr
        sys.stderr = open(os.devnull, 'w')

        cls._server_thread = threading.Thread(target=run_server, kwargs={'port': 8001})
        cls._server_thread.daemon = True
        cls._server_thread.start()

        import time
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        sys.stderr.close()
        sys.stderr = cls.stderr_original

    def setUp(self):
        StoreHTTPRequestHandler.store._data.clear()
        self.client = http.client.HTTPConnection('localhost', 8001)

    def tearDown(self):
        self.client.close()

    def test_invalid_path(self):
        self.client.request('GET', '/invalid/path')
        response = self.client.getresponse()
        self.assertEqual(response.status, 404)

    def test_get_nonexistent_key(self):
        self.client.request('GET', '/store/nonexistent')
        response = self.client.getresponse()
        self.assertEqual(response.status, 404)
        data = json.loads(response.read())
        self.assertEqual(data, {'error': 'Key not found'})

    def test_post_and_get(self):
        headers = {'Content-Type': 'application/json'}
        body = json.dumps({'value': 'value1'})
        self.client.request('POST', '/store/key1', body=body, headers=headers)
        response = self.client.getresponse()
        self.assertEqual(response.status, 201)
        data = json.loads(response.read())
        self.assertEqual(data, {'key': 'key1', 'value': 'value1'})

        self.client.request('GET', '/store/key1')
        response = self.client.getresponse()
        self.assertEqual(response.status, 200)
        data = json.loads(response.read())
        self.assertEqual(data, {'key': 'key1', 'value': 'value1'})

    def test_delete_key(self):
        StoreHTTPRequestHandler.store['key_to_delete'] = 'some_value'

        self.client.request('DELETE', '/store/key_to_delete')
        response = self.client.getresponse()
        self.assertEqual(response.status, 204)

        self.client.request('GET', '/store/key_to_delete')
        response = self.client.getresponse()
        self.assertEqual(response.status, 404)

if __name__ == '__main__':
    unittest.main() 