import cherrypy
from pyencoder import db
import json

class OnePage(object):
    def index(self):
        myDB = db.DBConnection()
        request = myDB.select("SELECT * from watch WHERE id = 1")
        return json.dumps(request)
    index.exposed = True

class HelloWorld(object):
    onepage = OnePage()

    def index(self):
        return "hello world"
    index.exposed = True

cherrypy.quickstart(HelloWorld())