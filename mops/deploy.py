#!/usr/bin/env python

#Anirudh Srinivasan
#June 30 2015

from os import chdir
from shlex import split
from subprocess import Popen, call, PIPE
#import readline
import logging
from optparse import OptionParser
import git
import sys

'''Variables used in this script'''
git_dir = '/var/www/MovetoProd/'
stage_server = ''
prod_server = ''
server = ''


parser = OptionParser()
parser.add_option('-e', '--env', dest='env', help='this is the name of the environment like prod or stage')
parser.add_option('-v', '--version', dest='version', help='This is the commit id')
(opts, args) = parser.parse_args()

def see_remote_commit_ids():
        '''This function is ran to see all the commit id on the repo'''
        chdir(git_dir)
        SEECOMMITID = '/usr/bin/git rev-list --remotes --pretty=oneline'
        SEE_COMMIT_ID = split(SEECOMMITID)
        call(SEE_COMMIT_ID)
def git_pull():
        '''This is function to a simple git pull'''
        chdir(git_dir)
        repo = git.Repo(git_dir)
        repo.remotes.origin.pull()
def git_reset():
        '''This function gets the commit id as argument and reset the head to that commit id'''
        chdir(git_dir)
        GITRESET = '/usr/bin/git reset --hard %s' %opts.version
        GIT_RESET = split(GITRESET)
        call(GIT_RESET)
def rsync_cmd():
        '''This is a simple bach rsync command over ssh ran from stage to oush stuff to prod'''
        RSYNCCMD = '/usr/bin/rsync -vrltD --exclude=.git/*** --exclude=event/partners/upload/*** --delete %s root@%s:/opt/www/html/' %(git_dir, server)
        RSYNC_CMD = split(RSYNCCMD)
        call(RSYNC_CMD)
def check_commit_id():
        chdir(git_dir)
        repo = git.Repo(git_dir)
        commits = list(repo.iter_commits(max_count=15))
        commit_list = []
        for commit in commits:
                commit2 = str(commit)
                commit_list.append(commit2)
        if opts.version not in commit_list:
                print "This Commit ID is not present. Type it correctly"
                sys.exit(1)
        else:
                pass

if __name__ == '__main__':
        if opts.env == None or opts.version == None:
                parser.print_help()
                exit(-1)
        logging.basicConfig(filename ='/tmp/pull_and_deploy.log',level =logging.DEBUG, datefmt ='%m/%d/%Y %I:%M:%S %p', format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')
        if opts.env == "stage" :
           server = stage_server
           git_pull()
           check_commit_id()
           git_reset()
           rsync_cmd()
           logging.info('COMMIT ID:%s rsynced to the staging server %s' %(opts.version, server))
           print 'COMMIT ID:%s pushed to the staging server %s' %(opts.version, server)
        elif opts.env == "prod" :
             server = prod_server
             git_pull()
             check_commit_id()
             git_reset()
             rsync_cmd()
             logging.info('COMMIT ID:%s rsynced to the production server %s' %(opts.version, server))
             print 'COMMIT ID:%s pushed to the production server %s' %(opts.version, server)
