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
      id integer PRIMARY KEY,
      command_line text NOT NULL,
      start_time timestamp NOT NULL,
      duration integer NOT NULL,
      stdout text NOT NULL,
      stderr text NOT NULL,
      exit_code integer NOT NULL
    )
  ''')

  db.execute('''
    CREATE INDEX IF NOT EXISTS cronjobs_start_time ON cronjobs(start_time)
  ''')
  return db

def spawn():
  db = sqlite3.connect(database_name(), detect_types=sqlite3.PARSE_DECLTYPES)
  db.row_factory = sqlite3.Row
  return db
