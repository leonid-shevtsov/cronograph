import os
import sys
import sqlite3

_database_name = None

def database_name():
  global _database_name
  _database_name = _database_name or (sys.argv.pop(1) if len(sys.argv)>1 and sys.argv[1].endswith('.sqlite3') else os.path.expanduser('~/.cronograph.sqlite3'))
  return _database_name

def ensure_structure(db):
  db.execute('''
    CREATE TABLE IF NOT EXISTS cronjobs (
      start_time INTEGER NOT NULL,
      end_time INTEGER NOT NULL,
      command_line TEXT NOT NULL,
      stdout TEXT NOT NULL,
      stderr TEXT NOT NULL,
      exit_code INTEGER NOT NULL
    )
  ''')
  return db

def spawn():
  db = sqlite3.connect(database_name())
  db.row_factory = sqlite3.Row
  return db
