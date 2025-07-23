import threading
from kvstore.cache.cache import LRUCache
from kvstore.database.database import Database

class KeyValueStore:
  def __init__(self, db: Database, cache: LRUCache):
    self._database = db
    self._cache = cache
    self._lock = threading.RLock()

  def __getitem__(self, key):
    with self._lock:
      value = self._cache.get(key)
      if value is None:
        value = self._database.get(key)
        if value is not None:
          self._cache.put(key, value)
      return value

  def __setitem__(self, key, value):
    with self._lock:
      self._database.set(key, value)
      self._cache.put(key, value)

  def pop(self, key, default=None):
    with self._lock:
      value = self._database.get(key)
      if value is None:
          return default
      
      self._database.delete(key)
      self._cache.delete(key)
      return value

  def close(self):
    self._database.close()