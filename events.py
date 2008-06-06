from google.appengine.api import users
from google.appengine.ext import db
import datetime


class Event( db.Model ):
   user = db.UserProperty()
   title = db.StringProperty()
   description = db.StringProperty(multiline=True)
   start = db.DateTimeProperty()
   end = db.DateTimeProperty()
   
   
class EventCreator():
   
   def insertEvent(self, user, title, description, start, end):
      event = Event()
      event.user = user
      event.title = title
      event.description = description
      event.start = start
      event.end = end
      event.put()
      
   def getUserEvents(self, user):
         
      events = db.GqlQuery("SELECT * FROM Event WHERE user = :1", user)
      
      for event in events:
         print "User ", event.user
         print "Title ", event.title
         print "Description ", event.description
         print "Start ", event.start
         print "End ", event.end



