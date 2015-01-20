from gm_pr import settings

def chan_proj(request):
    """ Retrieve repo list from a Slack request or web request.
    Parameter come from GET and can be either 'channel_name' or 'project' (they
    both give the same result), or 'channel_name' + 'text' which lead to write 'text'
    project in 'channel_name' channel
    return a tuple: list of repos, project, channel name
    """
    repos = None
    project = None
    channel = None
    if request.GET != None and \
       'channel_name' in request.GET or 'project' in request.GET :
        if 'channel_name' in request.GET:
            channel = request.GET['channel_name']
            if 'text' in request.GET:
                project = request.GET['text']
            if not project or len(project) == 0:
                project = channel
        else:
            project = request.GET['project']

        if project in settings.PROJECTS_CHAN:
            repos = settings.PROJECTS_CHAN[project]
    return repos, project, channel
