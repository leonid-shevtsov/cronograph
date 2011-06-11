#!/usr/bin/env python
import sys
import os.path
import sqlite3

database_name = None

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

def serve():
  import web

  sys.argv.pop(1)

  urls = (
      '/', 'index'
  )
  
  database_name = get_database_name()
  ensure_db_structure(spawn_db(database_name))

  class index:
    def GET(self):
      result = ""
      for row in spawn_db(database_name).execute('SELECT * FROM cronjobs'):
        result += row['stdout']
      return result

  app = web.application(urls, {'index': index})
  app.run()

def handle_cron():
  from subprocess import Popen, PIPE
  from datetime import datetime
  
  process = None
  out = None
  err = None
  exit_code = None

  
  db = ensure_db_structure(spawn_db(get_database_name()))

  args = sys.argv
  args.pop(0)

  if len(args)==0:
    print "Need a command line in arguments"
    exit(1)

  start_time = datetime.now()
  try:
    process = Popen(args, 0, None, None, PIPE, PIPE)
    process.wait()
  except OSError as (errno, strerror):
    err = strerror

  end_time = datetime.now()

  if process:
    out = process.stdout.read()
    err = process.stderr.read()
    exit_code = process.returncode
  else:
    out = out or ""
    err = err or ""
    exit_code = -1

  
  c=db.cursor()
  c.execute('insert into cronjobs (start_time, end_time, command_line, stdout, stderr, exit_code) values(?, ?, ?, ?, ?, ?)',
      [start_time, end_time, ' '.join(args), out, err, exit_code]
      )
  db.commit()
   


#### MAIN

if __name__ == "__main__": 
  if len(sys.argv)>1 and sys.argv[1] == "serve":
    serve()
  else:
    handle_cron()
