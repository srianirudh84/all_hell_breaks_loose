#!/usr/bin/python

import random
import string
import smtplib
import sys
import os
from subprocess import call
import socket

user = sys.argv[1]
receivers = ["%s@xyz.com" %user]

def genrandpwd():
        return  ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits + string.ascii_uppercase + string.punctuation) for _ in range(30))

def change_passwd(user, password):
        p = os.popen("/usr/bin/passwd %s" %user, "w")
        p.write(password)
        p.write("\n")
        p.write(password)
        p.close()

def chage(user):
        agepasswd = call(["/usr/bin/chage", "-d", "0", "%s" %user])

def mailpwd(user, password):
        sender = "admin@%s" %socket.gethostname()
        subj = "!!!IMPORTANT!!!, Unix password changed for user %s" %user
        text = "The password for the %s user has changed, the new password is:\n\n %s \n\n Note: The system will force to change the password upon initial login. Please use the password provided in the mail as your current password and type the password of your choice as the New password" %(user, password)
        message = message = 'Subject: %s\n\n%s' % (subj, text)
        smtpObj = smtplib.SMTP('')
        smtpObj.sendmail(sender, receivers, message)
        smtpObj.quit()

def main():
        newpwd = genrandpwd()
        change_passwd(user, newpwd)
        chage(user)
        mailpwd(user, newpwd)

if __name__ == "__main__":
        main()
