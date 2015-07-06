# Django settings for gm_pr projects.

import os

GITHUB_LOGIN = "foo@genymobile.com"
GITHUB_PASSWORD = "password"
#web version
WEB_URL = "http://jenkins.genymobile.com/gm_pr/"
SLACK_TOKEN = "s9Wdn8diWL8bGItBNL1SuEIz"
SLACK_URL = "https://hooks.slack.com/services/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"

TOP_LEVEL_URL = "https://api.github.com"
ORG = "Genymobile"
# Number of days a PRs without update can be flagged as OLD.
OLD_PERIOD=4
# only PRs with one of those labels can be considered as OLD.
# Use None for "no label"
OLD_LABELS=("Needs Reviews", None)

PROJECTS_CHAN = \
    { 'general' : ("genymotion-binocle",
                  ),
      'random' : ('FridgeCheckup',
                 ),
    }

