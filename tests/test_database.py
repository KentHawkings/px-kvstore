import unittest
from kvstore.database.database import Database

class TestDatabase(unittest.TestCase):
  def setUp(self):
    self.db = Database(db=':memory:')

  def tearDown(self):
    self.db.close()

  def test_get_and_set(self):
    self.db.set('key1', 'value1')
    self.assertEqual(self.db.get('key1'), 'value1')

  def test_delete(self):
    self.db.set('key1', 'value1')
    self.db.delete('key1')
    self.assertIsNone(self.db.get('key1'))

  def test_get_nonexistent_key(self):
    self.assertIsNone(self.db.get('nonexistent'))

if __name__ == '__main__':
  unittest.main() 