#!/usr/bin/python
import cherrypy, os, sys
from time import gmtime, strftime, localtime

# Import my view & model
from model_helpers import get_images, download_email
from view_index import HTML_HEADER, HTML_FOOTER, html_navbar

myDir = '.'

class GrisVakt(object):

	def __init__(self):
		self.view_days = 3
	
	@cherrypy.expose
	def days(self, view_days):
		try:
			self.view_days=int(view_days)
		except:
			self.view_days=3
		
		return '<html><head><meta HTTP-EQUIV="REFRESH" content="0; url=/"></head></html>'

	@cherrypy.expose
	def index(self):
		print "(index) Got view_days=%s"% self.view_days
		download_email(myDir)
		update_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
		print "update: %s"% update_time
		
		HTML_LIST=''
		
		the_images = get_images("%s/assets/images/"% myDir, self.view_days)
		
		if len(the_images) > 0:
			for image in the_images:
				HTML_LIST += '\r\
				<div class="container">\r\
					<img src="/assets/images/%s">\r\
				</div>\r\
				<br>\r\
'% image["name"]
		else:
			HTML_LIST = '\r\
				<div class="container">\r\
					<p class="lead">Inga bilder!</p>\r\
				</div>\r\
				<br>\r'

		HTML_BODY = '\r\
		\r\
	<div class="container">\r\
\r\
      <div class="starter-template">\r\
        <br>\r\
        <p class="lead">Hittade <strong>%s</strong> bilder, senast uppdaterad <strong>%s</strong></p>\r\
      </div>\r\
      \r\
    <div>\r\
        %s\r\
    </div>\r\
\r\
    </div><!-- /.container -->\r\
'% (len(the_images), update_time, HTML_LIST)

		return "%s%s%s%s"%(HTML_HEADER, html_navbar(self.view_days), HTML_BODY, HTML_FOOTER)

if __name__ == '__main__':
	conf = {
		'/': {
			'tools.sessions.on': True,
			'tools.staticdir.root': os.path.abspath(myDir)
		},
		'/assets': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './assets'
		}
	}
	
	cherrypy.config.update(
    {'server.socket_host': '0.0.0.0'} )

	if len(get_images("%s/assets/images/"% myDir)) == 0:
		print "No images...pulling all"
		download_email(myDir, 'ALL')
    	
	cherrypy.quickstart(GrisVakt(), '/', conf)