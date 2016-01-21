#!/usr/bin/python
import cherrypy, os, sys
from time import gmtime, strftime, localtime

HTML_HEADER = '\
<!DOCTYPE html>\r\
<html lang="en">\r\
  <head>\r\
    <meta charset="utf-8">\r\
    <meta http-equiv="X-UA-Compatible" content="IE=edge">\r\
    <meta name="viewport" content="width=device-width, initial-scale=1">\r\
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->\r\
    <meta name="description" content="">\r\
    <meta name="author" content="">\r\
    <link rel="icon" href="../../favicon.ico">\r\
\r\
    <title>Bj&aumllleberg grisvakt</title>\r\
\r\
    <!-- Bootstrap core CSS -->\r\
    <link href="/assets/css/bootstrap.min.css" rel="stylesheet">\r\
\r\
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->\r\
    <link href="./assets/css/ie10-viewport-bug-workaround.css" rel="stylesheet">\r\
\r\
    <!-- Custom styles for this template -->\r\
    <link href="./assets/css/grid.css" rel="stylesheet">\r\
\r\
    <!-- Just for debugging purposes. Don\'t actually copy these 2 lines! -->\r\
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->\r\
    <script src="./assets/js/ie-emulation-modes-warning.js"></script>\r\
\r\
    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->\r\
    <!--[if lt IE 9]>\r\
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>\r\
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>\r\
    <![endif]-->\r\
  </head>\r\
  \r\
  <body>\r\
\r\
    <nav class="navbar navbar-inverse navbar-fixed-top">\r\
      <div class="container">\r\
        <div class="navbar-header">\r\
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">\r\
            <span class="sr-only">Toggle navigation</span>\r\
            <span class="icon-bar"></span>\r\
            <span class="icon-bar"></span>\r\
            <span class="icon-bar"></span>\r\
          </button>\r\
          <a class="navbar-brand" href="#">Bj&aumlllebergs jaktlag</a>\r\
        </div>\r\
      </div>\r\
    </nav>\r\
'

HTML_FOOTER = "\r\
    <!-- Bootstrap core JavaScript\r\
    ================================================== -->\r\
    <!-- Placed at the end of the document so the pages load faster -->\r\
    <script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js\"></script>\r\
    <script>window.jQuery || document.write('<script src=\"../../assets/js/vendor/jquery.min.js\"><\/script>')</script>\r\
    <script src=\"../../dist/js/bootstrap.min.js\"></script>\r\
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->\r\
    <script src=\"../../assets/js/ie10-viewport-bug-workaround.js\"></script>\r\
  </body>\r\
</html>\r\
"

def download_email(email_flag='UNSEEN'):
	import imaplib, email, os, sys

	mail = imaplib.IMAP4_SSL(os.environ['GRISVAKT_EMAIL_IMAP_SERVER'])
	mail.login(os.environ['GRISVAKT_EMAIL_USER'], os.environ['GRISVAKT_EMAIL_PASSWORD'])
	mail.select('inbox')

	# Working dir
	working_dir = "."

	# Download new emails
	result, data = mail.uid('search', None, email_flag)

	# Split to list
	uids = data[0].split()

	print "Got %s new emails to process..."% len(uids)

	for uid in uids:
		result, data = mail.uid('fetch', uid, '(RFC822)')
		m = email.message_from_string(data[0][1])

		if m.get_content_maintype() == 'multipart': #multipart messages only
			for part in m.walk():
				#find the attachment part
				if part.get_content_maintype() == 'multipart': continue
				if part.get('Content-Disposition') is None: continue

				#save the attachment in the program directory
				filename = part.get_filename()
				fp = open("%s/assets/images/%s-%s"% (working_dir,uid,filename), 'wb')
				fp.write(part.get_payload(decode=True))
				fp.close()
				print '%s saved!' % filename
				
	return len(uids)

def get_images(myDir):
	myFiles = os.listdir(myDir)
	sorted_list = []
	
	for n in sorted([int(x.split('-')[0]) for x in myFiles if '-' in x], reverse=1):
		sorted_list.extend([x for x in myFiles if x.startswith('%s-'% n)])
		
	return sorted_list

class GrisVakt(object):
	@cherrypy.expose
	def index(self):
		download_email()
		update_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
		print "update: %s"% update_time
		
		HTML_LIST=''
		
		the_images = get_images("./assets/images")
		
		if len(the_images) > 0:
			for image in the_images:
				HTML_LIST += '\r\
				<div class="container">\r\
					<img src="/assets/images/%s">\r\
				</div>\r\
				<br>\r\
'% image
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
        <h1>V&aumllkommen till &aringtelkameran i Bj&aumllleberg</h1>\r\
        <p class="lead">Senast uppdaterad <strong>%s</strong></p>\r\
      </div>\r\
      \r\
    <div>\r\
        %s\r\
    </div>\r\
\r\
    </div><!-- /.container -->\r\
'% (update_time, HTML_LIST)

		return "%s%s%s"%(HTML_HEADER, HTML_BODY, HTML_FOOTER)

if __name__ == '__main__':
	conf = {
		'/': {
			'tools.sessions.on': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/assets': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': './assets'
		}
	}
	
	cherrypy.config.update(
    {'server.socket_host': '0.0.0.0'} )

	if get_images("./assets/images") == 0:
		download_email('ALL')
    	
	cherrypy.quickstart(GrisVakt(), '/', conf)