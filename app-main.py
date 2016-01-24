#!/usr/bin/python
import cherrypy, os, sys
from time import gmtime, strftime, localtime

# Import my view & model
from model_helpers import get_images, download_email
from view_index import HTML_HEADER, HTML_FOOTER, html_navbar

myDir = '.'

class GrisVakt(object):

	@cherrypy.expose
	def index(self):
		download_email(myDir)
		update_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
		print "update: %s"% update_time
		
		HTML_LIST=''
		
		the_images = get_images("%s/assets/images/"% myDir)
		
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
        <p class="lead">Senast uppdaterad <strong>%s</strong></p>\r\
      </div>\r\
      \r\
    <div>\r\
        %s\r\
    </div>\r\
\r\
    </div><!-- /.container -->\r\
'% (update_time, HTML_LIST)

		return "%s%s%s%s"%(HTML_HEADER, html_navbar(0), HTML_BODY, HTML_FOOTER)

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