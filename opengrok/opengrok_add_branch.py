#!/usr/bin/python
#Apr 20 2016
#author = Anirudh Srinivasan

import os
from shlex import split
from subprocess import Popen, call, PIPE
import re
import git

#Variables
opengrok_dir = '/var/opengrok/'
git_dir = opengrok_dir + 'git/'
main_dir = git_dir + 'main/'
toolbox_dir = git_dir + 'toolbox/'


'''This creates a list called branch_list which has danube-4*, ncc-2*, installer-* branches'''
lrb='git branch -a'
list_remote_branch = split(lrb)
os.chdir(main_dir)
proc = Popen(list_remote_branch,stdout=PIPE)
outputlines = filter(lambda x:len(x)>0,(line.strip() for line in proc.stdout))
r = re.compile(r'\bremotes/origin/installer-\b|\bremotes/origin/ncc-2\b|\bremotes/origin/danube-4\b')
new_list=filter(r.match, outputlines)
branch_list = [re.sub(r'\bremotes/origin/\b', '', x) for x in new_list]

'''This iterates through the branch_list and if not present in the ~/git/<branch-name> then adds it here
Also writes to the opengrok_provision.sh in the toolbox git_dir and pushes it to the master remote origin.'''

for i in branch_list:
	os.chdir(git_dir)
	if os.path.isdir(i):
		pass
	else:
		print "Adding a new branch %s to opengrok" %i
		string = "./opengrok_create_branch.sh %s" %i
		os.chdir(opengrok_dir)
		call(split(string))
		print "Adding this to the opengrok_provision.sh in the toolbox repo"
		f = open("/var/opengrok/git/toolbox/opengrok/opengrok_provision.sh", 'a')
		f.write(string + "\n")
		f.close()
		repo=git.Repo(toolbox_dir)
		repo.git.pull()
		repo.git.add('opengrok/opengrok_provision.sh')
		repo.git.commit(m='new branch %s added to the file opengrok/opengrok_provision.sh' %i)
		repo.git.push()
