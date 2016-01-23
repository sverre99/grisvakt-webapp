#!/usr/bin/python
import os
from time import gmtime, strftime, localtime, mktime

def get_images(myDir, max_result=10):
	print "Checking directory: %s" %myDir	
	myFiles = os.listdir(myDir)
	print "myfiles: %s"% myFiles
	sorted_list = []
	
	for n in sorted([int(x.split('-')[0]) for x in myFiles if '-' in x], reverse=1):
		sorted_list.extend([x for x in myFiles if x.startswith('%s-'% n)])
	
	if len(sorted_list) > max_result:
		return sorted_list[0:max_result]
	else:
		return sorted_list

def download_email(myDir,email_flag='UNSEEN'):
	import imaplib, email
	
	mail = imaplib.IMAP4_SSL(os.environ['GRISVAKT_EMAIL_IMAP_SERVER'])
	mail.login(os.environ['GRISVAKT_EMAIL_USER'], os.environ['GRISVAKT_EMAIL_PASSWORD'])
	mail.select('inbox')

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
				my_file = "%s/assets/images/%s-%s"% (myDir,uid,filename)
				fp = open(my_file, 'wb')
				fp.write(part.get_payload(decode=True))
				fp.close()
				print '%s saved!' % filename
				
				# Now set the correct creating-date and time on the file
				timestamp=strftime("%Y%m%d%H%M.%S",localtime(mktime(email.utils.parsedate(m.values()[7]))))
				os.system("touch -t %s %s"% (timestamp, my_file))
				
	return len(uids)
