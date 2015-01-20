from gm_pr import models
from celery import group
from gm_pr.celery import app

import json, urllib.request
import re

def get_json(url):
    """ get json data from url.
    Auth is managed in __init__.py in this module
    """
    response = urllib.request.urlopen(url)
    charset = response.info().get_content_charset()
    if charset == None:
        charset = 'utf-8'
    string = response.read().decode(charset)
    return json.loads(string)

@app.task
def fetch_data(repo_name, url, org):
    """ Celery task, call github api
    """
    pr_list = []
    repo = {'name' : repo_name,
            'pr_list' : pr_list,
           }
    url = "%s/repos/%s/%s/pulls" % (url, org, repo_name)
    jdata = get_json(url)
    if len(jdata) == 0:
        return
    for jpr in jdata:
        if jpr['state'] == 'open':
            detail_json = get_json(jpr['url'])
            comment_json = get_json(detail_json['comments_url'])
            plusone = 0
            lgtm = 0
            milestone = jpr['milestone']
            label_json = get_json(jpr['issue_url'] + '/labels')
            label = None
            for jcomment in comment_json:
                body = jcomment['body']
                if re.search(":\+1:", body):
                    plusone += 1
                if re.search("LGTM", body, re.IGNORECASE):
                    lgtm += 1
            if milestone:
                milestone = milestone['title']
            if len(label_json) > 0:
                label = {'name' : label_json[0]['name'],
                         'color' : label_json[0]['color'],
                        }
            pr = models.Pr(url=jpr['html_url'],
                           title=jpr['title'],
                           updated_at=jpr['updated_at'],
                           user=jpr['user']['login'],
                           repo=jpr['base']['repo']['full_name'],
                           nbreview=int(detail_json['comments']) + \
                                    int(detail_json['review_comments']),
                           plusone=plusone,
                           lgtm=lgtm,
                           milestone=milestone,
                           label=label)
            pr_list.append(pr)

    sorted(pr_list, key=lambda pr: pr.updated_at)

    if len(pr_list) == 0:
        return None
    return repo


class PrFetcher:
    def __init__(self, url, org, repos):
        self.__url = url
        self.__org = org
        self.__repos = repos

    def get_prs(self):
        """
        fetch the prs from github

        return a list of { 'name' : repo_name, 'pr_list' : pr_list }
        pr_list is a list of models.Pr
        """
        res = group(fetch_data.s(repo_name, self.__url, self.__org)
                    for repo_name in self.__repos)()
        data = res.get()
        return [repo for repo in data if repo != None]
