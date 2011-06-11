import db
import sys
import web

def serve():
  sys.argv.pop(1)

  urls = (
      '/', 'index',
      '/cronjobs/(\d+)', 'show'
  )
  
  db.ensure_structure(db.spawn())

  app = web.application(urls, globals())
  app.run()

class Action:
  def __init__(self):
    self._db = None
    self.render = web.template.render('templates', base='layout')

  def db(self):
    self._db = self._db or db.spawn()
    return self._db

class index(Action):
  def GET(self):
    return self.render.index(self.db().execute('SELECT * FROM cronjobs'))

class show(Action):
  def GET(self, id):
    return self.render.show(self.db().execute('SELECT * FROM cronjobs WHERE id=?', [id]).fetchone())
