#!/usr/bin/python
#Sep 19 2016
#author = Anirudh Srinivasan

import os
from shlex import split
from subprocess import Popen, call, PIPE
import re
import git
import sys

#Variables
opengrok_dir = '/var/opengrok/'
git_dir = opengrok_dir + 'git/'
main_dir = git_dir + 'main/'
toolbox_dir = git_dir + 'toolbox/'


def remote_branch_list():
    lrb='git branch -a'
    list_remote_branch = split(lrb)
    os.chdir(main_dir)
    proc = Popen(list_remote_branch,stdout=PIPE)
    outputlines = filter(lambda x:len(x)>0,(line.strip() for line in proc.stdout))
    branch_list = [re.sub(r'\bremotes/origin/\b', '', x) for x in outputlines]
    return branch_list

def add_new_branch(name):
    string = "./opengrok_create_branch.sh %s" %name
    os.chdir(opengrok_dir)
    call(split(string))
    print "Adding this to the opengrok_provision.sh in the toolbox repo"
    f = open("/var/opengrok/git/toolbox/opengrok/opengrok_provision.sh", 'a')
    f.write(string + "\n")
    f.close()
    repo=git.Repo(toolbox_dir)
    repo.git.pull()
    repo.git.add('opengrok/opengrok_provision.sh')
    repo.git.commit(m='new branch %s added to the file opengrok/opengrok_provision.sh' %name)
    repo.git.push()

def main():
    list_of_remote_branch = remote_branch_list()
    short_list = filter(lambda x:'%s' %sys.argv[1] in x, list_of_remote_branch)
    print short_list
    branch_name = raw_input("Enter the branch name from this list above to add to opengrok: ")
    os.chdir(git_dir)
    if os.path.isdir(branch_name):
        print "the branch dir already exist in opengrok"
        pass
    else:
        print "Adding a new branch %s to opengrok" %branch_name
        add_new_branch(branch_name)

if __name__ == '__main__':
	if len(sys.argv) > 1:
	    main()
	else:
	    print "No argument was passed, try again with argument"
