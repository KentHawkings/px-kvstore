import sqlite3

class Database:
  def __init__(self, db='kvstore.db'):
    self._conn = sqlite3.connect(db, check_same_thread=False)
    self._create_table()

  def _create_table(self):
    cursor = self._conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS kv (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
    self._conn.commit()

  def get(self, key: str):
    cursor = self._conn.cursor()
    cursor.execute('SELECT value FROM kv WHERE key = ?', (key,))
    row = cursor.fetchone()
    return row[0] if row else None

  def set(self, key: str, value: str):
    cursor = self._conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO kv (key, value) VALUES (?, ?)', (key, str(value)))
    self._conn.commit()

  def delete(self, key: str):
    cursor = self._conn.cursor()
    cursor.execute('DELETE FROM kv WHERE key = ?', (key,))
    self._conn.commit()

  def close(self):
    self._conn.close()