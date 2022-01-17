import argparse
import logging
import sys
import time
import requests
from github import Github
import os
from requests.models import Response


def get_logger(name=None):
    if name==None:
        name = "payload_generator"
    logging.basicConfig(stream=sys.stdout, level='INFO',format="[%(asctime)s] %(levelname)s [%(threadName)s] [%(filename)s:%(funcName)s:%(lineno)s] %(message)s",
                            datefmt='%Y-%m-%dT%H:%M:%S')
    logger = logging.getLogger(name)
    return logger


class PollGithub:

    def __init__(self, repo,pr_label,author,query,token):
        self.repo=repo
        self.pr_label=pr_label
        self.author=author
        self.query=query
        self.token=token

    def get_pr_no(self):
        g = Github(self.token)
        repo = g.get_repo(self.repo)
        issues = g.search_issues(query=self.query, state='open', author=self.author, type='pr', label=self.pr_label)
        pr_no_list=[]
        for issue in issues:
            pr_no_list.append(issue.number)
        get_logger().info("PR No. is {}".format(pr_no_list[0]))
        return pr_no_list[0]

    def pr_status(self,pr_no):
        headers = {'content-type': 'application/json', 'Authorization': 'token {}'.format(self.token)}
        response = requests.get(url="https://api.github.com/repos/{}/pulls/{}".format(self.repo, pr_no), headers=headers)
        if response!=None and response.status_code==200:
            get_logger().info("PR Status is {}".format(response.json()['state']))    
            return response.json()['state']

    def get_merge_commit_sha(self,pr_no):
        headers = {'content-type': 'application/json', 'Authorization': 'token {}'.format(self.token)}
        response = requests.get(url="https://api.github.com/repos/{}/pulls/{}".format(self.repo, pr_no), headers=headers)
        if response!=None and response.status_code==200:
            get_logger().info("Merge Commit sha is {}".format(response.json()['merge_commit_sha']))    
            return response.json()['merge_commit_sha']

    def get_worflow_job_url(self, merge_commit_sha):
        headers = {'content-type': 'application/json', 'Authorization': 'token {}'.format(self.token)}
        response = requests.get(url="https://api.github.com/repos/{}/actions/runs".format(self.repo), headers=headers)
        if response!=None and response.status_code==200:
            for action in response.json()['workflow_runs']:
                if action['head_sha'] == merge_commit_sha:
                    get_logger().info("Job URL is {}".format(action['jobs_url']))
                    return action['jobs_url']

    def _jobs_steps_dict(self, job_url):
        jobs_steps_dict={}
        headers = {'content-type': 'application/json', 'Authorization': 'token {}'.format(self.token)}
        response = requests.get(url="{}".format(job_url), headers=headers)
        if response!=None and response.status_code==200:
            for job in range(len(response.json()['jobs'])):
                jobs_steps_dict[response.json()['jobs'][job]['name']]=response.json()['jobs'][job]['steps']
        #get_logger().info("Jobs and Steps json is  {}".format(jobs_steps_dict))
        return jobs_steps_dict

    def job_step_status(self, job_url, bin):
        time.sleep(20)
        jobs_steps_map=self._jobs_steps_dict(job_url)
        for job in jobs_steps_map:
        #print ("Running job {}".format(job))
            for step in range(len(jobs_steps_map[job])):
                if str(job) + str(jobs_steps_map[job][step]['name']) in bin:
                  continue
                elif jobs_steps_map[job][step]['conclusion'] == 'success' and jobs_steps_map[job][step]['status'] == 'completed':
                    get_logger().info("Step {} of Job {} ran successfully".format(jobs_steps_map[job][step]['name'], job))
                    bin.append(str(job) + str(jobs_steps_map[job][step]['name']))
                elif jobs_steps_map[job][step]['status'] == 'in_progress'and jobs_steps_map[job][step]['conclusion'] == None:
                    get_logger().info("Step {} of Job {} is in progress".format(jobs_steps_map[job][step]['name'], job))
                    self.job_step_status(job_url, bin)
                elif jobs_steps_map[job][step]['status'] == 'completed' and jobs_steps_map[job][step]['conclusion'] == 'failure':
                    get_logger().error("Step {} of Job {} is a failure , quiting....".format(jobs_steps_map[job][step]['name'], job))
                    return 'Failed'
        return 'Done'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Github  polling script.', epilog="Please run the script to poll github from your CI engine.")
    parser.add_argument('-r', '--repo', type=str, required=True, help="repo name.")
    parser.add_argument('-l', '--label', type=str, required=True, help="lable information.")
    parser.add_argument('-a', '--author', type=str, required=True, help="author name.")
    parser.add_argument('-q', '--query', type=str, required=True, help="query string.")
    parser.add_argument('-t', '--token', type=str, required=True, help="github token string.")
    parser.add_argument('-pr', '--get_pr', action=argparse.BooleanOptionalAction, type=bool, required=False, help="if true, get pr number.")
    parser.add_argument('-prno', '--pr_num', type=int, default=None, required=False, help="pr number.")
    params = parser.parse_args()
    repo=params.repo
    label=params.label
    author=params.author
    query=params.query
    token=params.token
    get_pr=params.get_pr
    pr_num=params.pr_num
    get_logger().info("User Input to script repo : {}, label: {}, author: {}, query: {}, token: {}, get_pr: {}, pr_num: {}".format(repo, label, author, query, token, get_pr, pr_num))
    #a=PollGithub(repo="infacloud/ct-k8-gitops", pr_label="kubeyard", author="infa-ctgitauto",query='intcloud-anitest-eks-qa-usw2')
    a=PollGithub(repo=repo, pr_label=label, author=author,query=query, token=token)
    #a=PollGithub(repo="infacloud/netblocks_workflow", pr_label="dependencies ", author="infa-netopsbot ",query='HAWK-VPC-1639762644')
    if get_pr:
        print (a.get_pr_no())
    else:
        while True:
            get_logger().info(a.pr_status(pr_no=pr_num))
            if a.pr_status(pr_no=pr_num) == 'closed':
                break
        get_logger().info(a.get_merge_commit_sha(pr_no=pr_num))
        get_logger().info(a.get_worflow_job_url(merge_commit_sha=a.get_merge_commit_sha(pr_no=pr_num)))
        done_bucket=[]
        x=a.job_step_status(job_url=a.get_worflow_job_url(merge_commit_sha=a.get_merge_commit_sha(pr_no=pr_num)), bin=done_bucket)
        if x == 'Done':
            os.putenv("HARNESS_APPROVAL_STATUS", "APPROVED")
        elif x == 'Failed':
            os.putenv("HARNESS_APPROVAL_STATUS", "REJECTED")
        #print(x)
        #print(done_bucket)
