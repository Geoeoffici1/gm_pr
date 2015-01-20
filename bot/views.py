from django.http import HttpResponse
from gm_pr import settings, chan_proj
from bot import tasks, slackAuth

@slackAuth.isFromSlack
def index(request):
    repos, project, channel = chan_proj.chan_proj(request)
    if repos != None:
        tasks.slack.delay(settings.TOP_LEVEL_URL, settings.ORG,
                          "%s?project=%s" % (settings.WEB_URL, project),
                          repos,
                          settings.SLACK_URL,
                          project,
                          "#%s" % channel)
        return HttpResponse("One moment, Octocat is considering your request\n")
    else:
        return HttpResponse("No projects found\n", status=404)
