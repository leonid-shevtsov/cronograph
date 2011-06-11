from db import *

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
