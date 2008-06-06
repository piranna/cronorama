import cgi
import wsgiref.handlers
import datetime
import time
import events


from google.appengine.api import users
from google.appengine.ext import webapp

class PostEvent(webapp.RequestHandler):
   def post(self):
      if users.get_current_user():
         event = events.Event()
         event.user = users.get_current_user()
         event.title = self.request.get('title')
         event.description = self.request.get('description')
         timezone = datetime.timedelta(hours=int(self.request.get('tz')))
         try:            
            event.start = datetime.datetime.strptime( self.request.get('start'), "%d-%b-%Y %H:%M:%S")
            event.start = event.start + timezone
         except ValueError:
            event.start = datetime.datetime.today()

         try:
            event.end = datetime.datetime.strptime( self.request.get('end'), "%d-%b-%Y %H:%M:%S")
            event.end = event.end + timezone
         except ValueError:
            event.end = event.start
         
         #start = datetime.datetime.strptime( self.request.get('start'), "%d-%b-%Y %H:%M:%S")
         #end = datetime.datetime.strptime( self.request.get('end'), "%d-%b-%Y %H:%M:%S")       
         
         #print event.start.strftime( "%b %d %Y %H:%M:%S +0000 GMT" )
         
         event.put()

      self.redirect('/')
         
      
