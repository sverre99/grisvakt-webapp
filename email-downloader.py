#!/usr/bin/python

import imaplib, email, os, sys

mail = imaplib.IMAP4_SSL(os.environ['GRISVAKT_EMAIL_IMAP_SERVER'])
mail.login(os.environ['GRISVAKT_EMAIL_USER'], os.environ['GRISVAKT_EMAIL_PASSWORD'])
mail.select('inbox')

# Working dir
working_dir = os.path.dirname(sys.argv[0])

# Download new emails
result, data = mail.uid('search', None, 'UNSEEN')

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
			fp = open("%s/images/%s-%s"% (working_dir,uid,filename), 'wb')
			fp.write(part.get_payload(decode=True))
			fp.close()
			print '%s saved!' % filename

