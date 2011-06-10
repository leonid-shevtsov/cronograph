#!/usr/bin/env python
import sys
import os.path

def get_database_name():
  return sys.argv.pop(1) if len(sys.argv)>1 and sys.argv[1].endswith('.sqlite3') else os.path.expanduser('~/cronograph.sqlite3')

def serve():
  import web
  import sqlite3

  sys.argv.pop(1)

  urls = (
      '/', 'index'
  )
  
  database_name = get_database_name()

  class index:
    def GET(self):
      db = sqlite3.connect(database_name)
      db.row_factory = sqlite3.Row
      result = ""
      for row in db.execute('SELECT * FROM cronjobs'):
        result += row['stdout']
      return result

  app = web.application(urls, {'index': index})
  app.run()

def init_db():
  import sqlite3

  db = sqlite3.connect(get_database_name())
  c = db.cursor()
  c.execute('''
    CREATE TABLE IF NOT EXISTS cronjobs (
      start_time INTEGER,
      end_time INTEGER,
      command_line TEXT,
      stdout TEXT,
      stderr TEXT,
      exit_code INTEGER
    )
  ''')
  db.commit()

def handle_cron():
  import sqlite3
  from subprocess import Popen, PIPE
  from datetime import datetime
  
  db = sqlite3.connect(get_database_name())

  args = sys.argv
  args.pop(0)

  if len(args)==0:
    print "Need a command line in arguments"
    exit(1)

  start_time = datetime.now()
  process = Popen(args, 0, None, None, PIPE, PIPE)
  process.wait()
  end_time = datetime.now()
  out = process.stdout.read()
  err = process.stderr.read()
  exit_code = process.returncode
  
  c=db.cursor()
  c.execute('insert into cronjobs (start_time, end_time, command_line, stdout, stderr, exit_code) values(?, ?, ?, ?, ?, ?)',
      [start_time, end_time, ' '.join(args), out, err, exit_code]
      )
  db.commit()
   


#### MAIN

if __name__ == "__main__": 
  if len(sys.argv)>1 and sys.argv[1] == "serve":
    serve()
  elif len(sys.argv)>1 and sys.argv[1] == "init":
    init_db() 
  else:
    handle_cron()
