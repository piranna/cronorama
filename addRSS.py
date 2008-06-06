import cgi
import wsgiref.handlers
import rssCreator

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db

class AddRSS(webapp.RequestHandler):
   def post(self):
      if users.get_current_user():
         rss = rssCreator.RSS()
         rss.user = users.get_current_user()
         rss.url  = self.request.get('url') 
         
         # Check if RSS is already stored
         addedFeeds = db.GqlQuery("SELECT * FROM RSS WHERE user = :1", rss.user)
         for checkRSS in addedFeeds:
            if( checkRSS.url == rss.url ):
               break
         else:
            rss.put()
         
      self.redirect('/')
