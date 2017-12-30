#!/usr/bin/python
#Author : anirudh@nutanix.com

import random
import string
import smtplib
import sys
import os

user = sys.argv[1]
receivers = ["it-systems-team@nutanix.com"]

def genrandpwd():
       	return  ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation) for _ in range(30))

def change_pure_passwd(user, password):
       	p = os.popen("/usr/bin/pure-pw passwd %s -m" %user, "w")
       	p.write(password)
       	p.write("\n")
       	p.write(password)
       	p.close()

def mailpwd(user, password):
       	sender = "root@ftp.nutanix.com"
       	subj = "!!!IMPORTANT!!!, Password changed for user %s" %user
       	text = "The password for the %s user has changed, the new password is: \n\n %s" %(user, password)
       	message = message = 'Subject: %s\n\n%s' % (subj, text)
       	smtpObj = smtplib.SMTP('mailrelay.corp.nutanix.com')
       	smtpObj.sendmail(sender, receivers, message)
       	smtpObj.quit()

def main():
       	newpwd = genrandpwd()
       	change_pure_passwd(user, newpwd)
       	mailpwd(user, newpwd)

if __name__ == "__main__":
       	main()
