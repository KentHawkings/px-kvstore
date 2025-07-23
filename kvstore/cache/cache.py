from collections import OrderedDict

class LRUCache:
  def __init__(self, maxsize):
    self._cache = OrderedDict()
    self._maxsize = maxsize

  def get(self, key):
    if key not in self._cache:
        return None
    else:
        self._cache.move_to_end(key)
        return self._cache[key]

  def put(self, key, value):
    self._cache[key] = value
    self._cache.move_to_end(key)
    if len(self._cache) > self._maxsize:
        self._cache.popitem(last=False)

  def delete(self, key):
    self._cache.pop(key)

  def clear(self):
    self._cache.clear()