import db
import sys

def serve():
  import web
  sys.argv.pop(1)

  urls = (
      '/', 'index'
  )
  
  db.ensure_structure(db.spawn())

  app = web.application(urls, globals())
  app.run()

class Request:
  def __init__(self):
    self._db = None

  def db(self):
    self._db = self._db or db.spawn()
    return self._db

class index(Request):
  def GET(self):
    result = ""
    for row in self.db().execute('SELECT * FROM cronjobs'):
      result += row['stdout']
    return result
