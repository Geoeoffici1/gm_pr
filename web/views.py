# Create your views here.


from django.shortcuts import render
from django.http import HttpResponse
from gm_pr import settings, chan_proj
from gm_pr.PrFetcher import PrFetcher
import time

def index(request):
    if not request.GET :
        context = {'project_list' : settings.PROJECTS_CHAN.keys()}
        return render(request, 'index.html', context)

    repos, project, channel = chan_proj.chan_proj(request)

    if repos != None:
        before = time.time()

        prf = PrFetcher(settings.TOP_LEVEL_URL, settings.ORG, repos)
        context = {"repo_list" : prf.get_prs()}

        after = time.time()
        print(after - before)
        return render(request, 'pr.html', context)
    else:
        return HttpResponse("No projects found\n", status=404)
