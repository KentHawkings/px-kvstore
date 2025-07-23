import unittest
from kvstore.cache.cache import LRUCache
from kvstore.database.database import Database
from kvstore.store import KeyValueStore

class TestKeyValueStore(unittest.TestCase):
  def setUp(self):
    db = Database(db=':memory:')
    cache = LRUCache(2)
    self.store = KeyValueStore(db=db, cache=cache)

  def tearDown(self):
    self.store.close()

  def test_set_and_get(self):
    self.store['key1'] = 'value1'
    self.assertEqual(self.store['key1'], 'value1')
    self.store['key1'] = 'value2'
    self.assertEqual(self.store['key1'], 'value2')

  def test_get_nonexistent_key(self):
    self.assertIsNone(self.store['nonexistent'])

  def test_pop(self):
    self.store['key1'] = 'value1'
    self.assertEqual(self.store.pop('key1'), 'value1')
    self.assertIsNone(self.store['key1'])

  def test_pop_nonexistent_key(self):
    self.assertIsNone(self.store.pop('nonexistent'))
    self.assertIsNone(self.store.pop('nonexistent', None))

  def test_cache_behavior(self):
    self.store['key1'] = 'value1'
    self.assertEqual(self.store._cache.get('key1'), 'value1')
    
    self.store.pop('key1')
    self.assertIsNone(self.store._cache.get('key1'))

    self.store['key2'] = 'value2'
    self.store._cache.delete('key2')
    self.assertIsNone(self.store._cache.get('key2'))
    self.assertEqual(self.store['key2'], 'value2')
    self.assertEqual(self.store._cache.get('key2'), 'value2')

if __name__ == '__main__':
    unittest.main()