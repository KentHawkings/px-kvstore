import unittest
from kvstore.store import KeyValueStore

class TestKeyValueStore(unittest.TestCase):

    def setUp(self):
        self.store = KeyValueStore()

    def test_set_and_get(self):
        self.store['key1'] = 'value1'
        self.assertEqual(self.store['key1'], 'value1')

    def test_get_nonexistent_key(self):
        self.assertIsNone(self.store['nonexistent'])

    def test_pop(self):
        self.store['key1'] = 'value1'
        self.assertEqual(self.store.pop('key1'), 'value1')
        self.assertIsNone(self.store['key1'])

    def test_pop_nonexistent_key(self):
        self.assertIsNone(self.store.pop('nonexistent'))

if __name__ == '__main__':
    unittest.main() 