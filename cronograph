#!/usr/bin/env python
import sys
import os.path
import sqlite3

def banner():
  print "cronograph - Collect, view and analyze cronjob execution logs"
  print
  print "cronograph [path-to-sqlite3-database] <cronjob>"
  print "    Log execution of given <cronjob>"
  print
  print "cronograph serve [path-to-sqlite3-database] [port]"
  print "    Start server on given port (default is 8080)"
  print
  print "Default database file used is ~/.cronograph.sqlite3"
  print
  print "Example crontab entry:"
  print
  print "0 0 * * * /home/user/bin/cronograph rsnapshot daily"
  exit(1)

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
    banner()

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
