import unittest
from kvstore.cache.cache import LRUCache

class TestLRUCache(unittest.TestCase):
  def test_get_and_put(self):
    cache = LRUCache(2)
    cache.put('key1', 'value1')
    cache.put('key2', 'value2')
    self.assertEqual(cache.get('key1'), 'value1')
    self.assertEqual(cache.get('key2'), 'value2')
    cache.put('key3', 'value3')

if __name__ == '__main__':
    unittest.main() 