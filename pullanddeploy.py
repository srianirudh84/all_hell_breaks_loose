#!/usr/bin/python

from os import chdir
from shlex import split
from subprocess import Popen, call, PIPE
import readline
import logging

'''Variables used in this script'''
git_dir = '/var/www/webapp-prod'

def see_remote_commit_ids():
	chdir(git_dir)
	SEECOMMITID = 'git rev-list --remotes --pretty=oneline'
	SEE_COMMIT_ID = split(SEECOMMITID)
	f1 = call(SEE_COMMIT_ID)
def git_pull():
	chdir(git_dir)
	GITPULL = 'git pull'
	GIT_PULL = split(GITPULL)
	f2 = call(GIT_PULL)
def git_reset():
	chdir(git_dir)
	GITRESET = 'git reset --hard %s' %a
	GIT_RESET = split(GITRESET)
	f3 = call(GIT_RESET)
def rsyn_cmd():
	RSYNCCMD = '/usr/bin/rsync -vrlptD --delete /opt/www/html/ prod-server:/opt/www/html/'
	RSYNC_CMD = split(RSYNCCMD)
	f4 = call(RSYNC_CMD)

if __name__ == '__main__':
    	logging.basicConfig(filename='/tmp/pull_and_deploy.log',level=logging.DEBUG)
	see_remote_commit_ids()
    	a = raw_input("Please pick a commit ID: ")
 	git_pull()
	git_reset()
	logging.info('COMMIT ID:%s pulled to the staging server stage-server' %a)
	yes_or_no = raw_input('Do you want to push the COMMIT ID:%s to the Production server ? Type y/n:' %a)
	if yes_or_no == 'y':
		logging.info('Pushing the COMMIT ID: %s to the Production server prod-server' %a)
		print 'Pushing the COMMIT ID: %s to the Production server prod-server' %a
		#rsyn_cmd()
	elif yes_or_no == 'n':
		 logging.info('Pushed notting to the Production server')
