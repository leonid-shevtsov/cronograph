from db import *

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
  
  data = [' '.join(args), start_time, end_time, out, err, exit_code]
  
  db.execute('insert into cronjobs (command_line, start_time, end_time, stdout, stderr, exit_code) values(?, ?, ?, ?, ?, ?)', data)
  db.commit()

  if should_notify_by_email(*data):
    print_email_notification(*data)

def should_notify_by_email(command_line, start_time, end_time, out, err, exit_code):
  return exit_code != 0

def print_email_notification(command_line, start_time, end_time, out, err, exit_code):
  print '''Cronograph recorded cronjob failing with return code {0}

COMMAND LINE: {1}
DURATION: {2}, started on {3}

================
ERROR OUTPUT:
{4}

================
STANDARD OUTPUT:
{5}
'''.format(exit_code, command_line, end_time-start_time, start_time, err, out)
