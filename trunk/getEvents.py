import events
import cgi
import RSSParser
import feedparser
import time
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import urlfetch

html_escape_table = {
   "&": "&amp;",
   '"': "&quot;",
   "'": "&apos;",
   ">": "&gt;",
   "<": "&lt;",
}

def html_escape(text):
   """Produce entities within text."""
   L=[]
   for c in text:
      L.append(html_escape_table.get(c,c))
   return "".join(L)

print "Content-Type: text/xml"

print ""
print "<data>"

if users.get_current_user():
   user = users.get_current_user()
else:
   user = users.User("cronoramanews@gmail.com")
   
# EVENTS
events = db.GqlQuery("SELECT * FROM Event WHERE user = :1", user)
for event in events:
   start = event.start.strftime( "%b %d %Y %H:%M:%S +0000 UTC" )
   end = event.end.strftime( "%b %d %Y %H:%M:%S +0000 UTC" )
   print "<event title='" + event.title + "' description='" + event.description + "' start='" + start + "' end='" + end + "'>"
   print event.description
   print "</event>"
   
# RSS
feeds = db.GqlQuery("SELECT * FROM RSS WHERE user = :1", user)
for feedURL in feeds:
	feed = urlfetch.fetch(feedURL.url)
	d = feedparser.parse(feed.content)
	favicon = d.feed.link.encode('utf-8');
	if( favicon[-1] != "/" ):
		favicon = favicon + "/"
	favicon = favicon + "favicon.ico"
	faviconURL = urlfetch.fetch( favicon )
	for item in d.entries:
 		if (faviconURL.status_code != 404 ): #favicon  found
 			faviconAtt = ' icon="' + favicon + '"'
 		else:
 			faviconAtt = ' icon="images/favicon.ico" ';
		print "<event title='" + html_escape(item.title.encode('utf-8')) + "' start='" + time.asctime(item.date_parsed) + " +0000 UTC' " + faviconAtt + ">"
		print html_escape(item.description.encode('utf-8'))
		print "</event>"
   
      
print "</data>"
      
   
