from google.appengine.api import users
from google.appengine.ext import db

class RSS( db.Model ):
   user = db.UserProperty()
   url = db.LinkProperty()
   
   
