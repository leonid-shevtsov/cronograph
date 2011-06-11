import os
import sys
import sqlite3

def get_database_name():
  return sys.argv.pop(1) if len(sys.argv)>1 and sys.argv[1].endswith('.sqlite3') else os.path.expanduser('~/.cronograph.sqlite3')

def ensure_db_structure(db):
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

def spawn_db(database_name):
  db = sqlite3.connect(database_name)
  db.row_factory = sqlite3.Row
  return db
