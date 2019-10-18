#
# Copyright 2019 Genymobile
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Represents an activity on a PR.  An activity may be:
* a comment
* a commit
* an event (examples include assigning, locking, labeling, milestoning):
  https://developer.github.com/v3/issues/events/
"""
import functools
from django.utils import dateparse
from datetime import datetime


@functools.total_ordering
class PrActivity:
    def __init__(self, date="", user="", event=""):
        if isinstance(date, datetime):
            self.date = date
        else:
            self.date = dateparse.parse_datetime(date)
        self.user = user
        self.event = event

    def __eq__(self, other):
        if other is None: return False
        if self.date != other.date: return False
        if self.user != other.user: return False
        if self.event != other.event: return False
        return True

    def __lt__(self, other):
        if other is None: return False
        # Simplification: just compare the dates.
        return self.date < other.date


# Return a PrActivity for the latest event for the given issue.
def get_latest_event(last_event_json):
    if len(last_event_json) == 0:
        return None
    last_event_json = last_event_json.get_last()
    return PrActivity(last_event_json['created_at'],
                             last_event_json['actor']['login'],
                             last_event_json['event'])

# Return a PrActivity for the latest commit for the given PR.
def get_latest_commit(last_commit_json):
    if len(last_commit_json) == 0:
        return None
    last_commit_json = last_commit_json.get_last()
    return PrActivity(last_commit_json['commit']['committer']['date'],
                             last_commit_json['commit']['committer']['name'],
                             "committed")

# Return the PrActivity which is the most recent of the two given activities.
def get_latest_activity(activity1, activity2):
    if activity1 is None: return activity2
    if activity1 > activity2: return activity1
    return activity2
