import wsgiref.handlers
from google.appengine.ext import webapp
import mainPage
import postEvent
import addRSS

def main():
  application = webapp.WSGIApplication(
                                       [('/', mainPage.MainPage),
                                        ('/post', postEvent.PostEvent),
                                        ('/addRSS', addRSS.AddRSS)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()