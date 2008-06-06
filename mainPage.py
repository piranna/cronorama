from google.appengine.ext import webapp
from google.appengine.api import users
import events
import datetime


class MainPage(webapp.RequestHandler):

   def userLogin(self):
      style = '<div style="position:absolute; right:5%; top:10%; font-family: Helvetica; font-size: 14;">'
      login = style + "<a href=\"%s\">Login</a></div>" % users.create_login_url("/") + "</div>"
      logout = style + "<a href=\"%s\">Logout</a></div>" % users.create_logout_url("/") + "</div>"      
      user = users.get_current_user()      
      if user:
         self.currentUser = user.nickname()
         output = '<div style="position:absolute; right:5%; top:5%; font-family: Helvetica; font-size: 24;";>Hello ' + self.currentUser + "!" + "</div>"
         return output + logout
      else:
         return login
       
   def get(self):
      
      self.response.headers['Content-Type'] = 'text/html'

      #creator = events.EventCreator()
      #creator.insertEvent( users.get_current_user() , "Titulo", "Descripcion", datetime.datetime.utcnow(), datetime.datetime.utcnow())
      #creator.getUserEvents(users.User("test@example.com"))
      
      self.response.out.write('''
            <html>
              <head>
                 <link rel="shortcut icon" href="images/favicon.ico">
                 <!--<script src="http://simile.mit.edu/timeline/api/timeline-api.js" type="text/javascript"></script> -->
                 <script src="timeline/api/timeline-api.js" type="text/javascript"></script>       
                 <script>
                    var lowerBarResol = Timeline.DateTime.DAY;
                    var upperBarResol = Timeline.DateTime.HOUR;   
                    var upperDate;
                    var lowerDate;
                    var tl;
                  </Script>           
                  <script language="javascript" type="text/javascript" src="datetimepicker.js"></script>    
              <title>Cronorama</title>        
              </head>
              <body onload="onLoad(true);" onresize="onResize();">
              <table><tr><td>
                <img src="images/logo.png"></td></tr><tr><td>
                <img src="http://code.google.com/appengine/images/appengine-noborder-120x30.gif" alt="Powered by Google App Engine" />
                </td></tr></table>
      
                <div style="position: absolute; bottom: 50px; right: 5%"><a href="javascript:decResol()" style="-moz-outline-style: none;" onclick="this.hideFocus=true;"><img src="images/minus.png" style="border-style: none; "></a><a href="javascript:incResol()"  style="-moz-outline-style: none;" onclick="this.hideFocus=true;"><img src="images/plus.png" style="border-style: none; -moz-outline-style: none;"></a></div>
                <div id="mainTimeline" style="position:absolute; bottom:100px; top: 150px; width:99%; font-family: Helvetica; font-size: 14; border: 1px solid #aaa"></div>

                
                
                                
                <script>
        
                  function incResol()
                  {

                     if( lowerBarResol > 1 )
                     {
                        lowerBarResol = lowerBarResol - 1;                                                                                                                                                                     
                        upperBarResol = upperBarResol - 1;
          	
                        onLoad(false);

                     }
                  }
                  
                  function decResol()
                  {
                     if( lowerBarResol < 9 )
                     {
                        lowerBarResol = lowerBarResol + 1;                                                                                                                                                                     
                        upperBarResol = upperBarResol + 1;
                   
                        onLoad(false);
                     }
                  }
                                    
                 
                  function onLoad(recenter) {

		    <!-- Get user time zone -->
   		    var visitortime = new Date();
  		    var timezone = visitortime.getTimezoneOffset()/60;
		    timezone = timezone * -1;

		    				var theme = Timeline.ClassicTheme.create();
							theme.event.bubble.width = 500;
							theme.event.bubble.height = 350;
							theme.firstDayOfWeek = 1; 
							theme.event.instant.icon = "images/favicon.ico";

                    var eventSource = new Timeline.DefaultEventSource();
                    var dt = new Date(); // today
                    var d = Timeline.DateTime.parseGregorianDateTime(dt.toUTCString());
                    if( recenter )
                    {
                    var bandInfos = [
                      Timeline.createBandInfo({
                          eventSource:    eventSource,
                          date:           d,
                          timeZone:	timezone,
                          width:          "90%", 
                          intervalUnit:   upperBarResol, 
                          intervalPixels: 53,
                          theme:				theme
                      }),
                      Timeline.createBandInfo({
                          showEventText:  false,
                          trackHeight:    0.5,
                          trackGap:       0.2,
                          eventSource:    eventSource,
                          date:           d,
                          timeZone:	timezone,                          
                          width:          "10%", 
                          intervalUnit:   lowerBarResol, 
                          intervalPixels: 182,
                          theme:				theme
                      })
                    ];
                    }
                    else
                    {

                    var bandInfos = [
                      Timeline.createBandInfo({
                          eventSource:    eventSource,
                          timeZone:	timezone,
                          width:          "90%", 
                          date:           tl.getBand(0).getCenterVisibleDate(),                          
                          intervalUnit:   upperBarResol, 
                          intervalPixels: 53,
                          theme:				theme                          
                      }),
                      Timeline.createBandInfo({
                          showEventText:  false,
                          trackHeight:    0.5,
                          trackGap:       0.2,
                          eventSource:    eventSource,
                          timeZone:	timezone,    
                          date:           tl.getBand(1).getCenterVisibleDate(),                      
                          width:          "10%", 
                          intervalUnit:   lowerBarResol, 
                          intervalPixels: 182,
                          theme:				theme                          
                      })
                    ];
                    }                    
                    bandInfos[1].syncWith = 0;
                    bandInfos[1].highlight = true;
                  
                    tl = Timeline.create(document.getElementById("mainTimeline"), bandInfos);
                  
                    Timeline.loadXML("getEvents.html", function(xml, url) { eventSource.loadXML(xml, url); });
                  }
                  
                  var resizeTimerID = null;
                  function onResize() {
                      if (resizeTimerID == null) {
                          resizeTimerID = window.setTimeout(function() {
                              resizeTimerID = null;
                              tl.layout();
                          }, 500);
                      }
                  }
                  
                  </script>''')
                 
      if users.get_current_user() :                   
         self.response.out.write( """<div style="position:absolute; bottom:1%;">
            <form action="/post" method="POST">

		<script>
		    <!-- Get user time zone -->
   		    var visitortime = new Date();
  		    var timezone = visitortime.getTimezoneOffset()/60;
		   document.write('<input type="hidden" name="tz" value="' + timezone + '">');
		</script>

            <table style="font-family: Helvetica; font-size: 14;">
               <tr>
                  <td>Start</td>
                  <td><input id="start" name="start" type="text" size="25"><a href="javascript:NewCal('start','ddmmmyyyy',true,24)"><img src="images/cal.gif" width="16" height="16" border="0" alt="Pick a date"></a></td>
                  <td>End</td>
                  <td align="right"><input name="end" id="end" type="text" size="25"><a href="javascript:NewCal('end','ddmmmyyyy',true,24)"><img src="images/cal.gif" width="16" height="16" border="0" alt="Pick a date"></a></td>
                  <td align="right" rowspan="2"><textarea name="description" rows="2" cols="80" style="font-family: Helvetica; font-size: 14;"></textarea></td>
                  <td>

		<input type="submit" value="Publish!"></td>
               </tr>
               <tr>
                  <td>Title</td>
                  <td colspan="4"><input name="title" type="text" size="60"></td>
               </tr>
            </table>
            </form>
            </div>
            
            <div style="position: absolute; top: 110px; right: 5%;">
               <form action="/addRSS" method="POST">
                  <table>
                     <tr>
                        <td><input name="url" type="text" size="50" ></td>
                        <td><input type="submit" value="Add RSS"></td>
                     </tr>
                  </table>
               </form>
            </div>
            
            
            
            """)

      self.response.out.write( self.userLogin() )
      self.response.out.write( "</body></head>")
          
