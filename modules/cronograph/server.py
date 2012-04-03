import db
import os
import sys
import web
from math import ceil

def serve():
  sys.argv.pop(0)

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
    self.render = web.template.render(os.path.dirname(__file__)+'/../../templates', base='layout')

  def db(self):
    self._db = self._db or db.spawn()
    return self._db

class index(Action):
  def GET(self):
    data = web.input(page=1)
    page = int(data.page)
    limit_clause='LIMIT %(start)s,20' % {'start': (page-1)*20}
    jobs = self.db().execute('SELECT * FROM cronjobs ORDER BY start_time DESC '+limit_clause)
    count = self.db().execute('SELECT COUNT(*) FROM cronjobs').fetchone()[0]
    total_pages = int(ceil(count/20.0))
    print total_pages
    return self.render.index(page, total_pages, jobs)

class show(Action):
  def GET(self, id):
    return self.render.show(self.db().execute('SELECT * FROM cronjobs WHERE id=?', [id]).fetchone())
