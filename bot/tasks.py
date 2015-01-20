from __future__ import absolute_import

import json
import urllib.request
from gm_pr.PrFetcher import PrFetcher
from gm_pr.celery import app

@app.task
def slack(url, org, weburl, repos, slack, project, channel):
    """ Celery task, use github api and send result to slack
    """
    prf = PrFetcher(url, org, repos)
    repo_list = prf.get_prs()
    nb_repo = len(repo_list)
    total_pr = 0
    for repo in repo_list:
        nb_pr = len(repo['pr_list'])
        total_pr += nb_pr

    txt = """Hey, we have %d PR in %d repo(s) for project *%s* (<%s|web version>)
""" % (total_pr, nb_repo, project, weburl)

    if total_pr > 0:
        txt += "\n"
        for repo in repo_list:
            txt += "*%s*\n" % repo['name']
            for pr in repo['pr_list']:
                txt += "<%s|%s> -" % (pr.url, pr.title)
                if pr.milestone:
                    txt += " *%s* -" % (pr.milestone)
                if pr.label:
                    txt += " *%s* -" % (pr.label['name'])
                txt += " %s review:%d LGTM:%d :+1::%d\n" % (pr.user, pr.nbreview, pr.lgtm, pr.plusone)


    payload = {"channel": channel,
               "username": "genypr",
               "text": txt,
               "icon_emoji": ":y:"}

    urllib.request.urlopen(slack, json.dumps(payload).encode('utf-8'))
