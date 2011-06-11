import db
import sys
import pipes

def handle():
  from subprocess import Popen, PIPE
  from datetime import datetime
  
  process = None
  out = None
  err = None
  exit_code = None
  
  database = db.ensure_structure(db.spawn()) 

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

  duration = (datetime.now() - start_time).seconds

  if process:
    out = process.stdout.read()
    err = process.stderr.read()
    exit_code = process.returncode
  else:
    out = out or ""
    err = err or ""
    exit_code = -1
  
  data = [build_command_line(args), start_time, duration, out, err, exit_code]
  
  database.execute('insert into cronjobs (command_line, start_time, duration, stdout, stderr, exit_code) values(?, ?, ?, ?, ?, ?)', data)
  database.commit()

  if should_notify_by_email(*data):
    print_email_notification(*data)

def build_command_line(args):
  return ' '.join([pipes.quote(a) for a in args])

def should_notify_by_email(command_line, start_time, duration, out, err, exit_code):
  return exit_code != 0

def print_email_notification(command_line, start_time, duration, out, err, exit_code):
  print '''Cronograph recorded cronjob failing with return code {0}

COMMAND LINE: {1}
DURATION: {2}s, started on {3}

================
ERROR OUTPUT:
{4}

================
STANDARD OUTPUT:
{5}
'''.format(exit_code, command_line, duration, start_time, err, out)
