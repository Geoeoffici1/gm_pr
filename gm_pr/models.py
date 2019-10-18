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

from django.db import models
from django.core.exceptions import ValidationError
from gm_pr import settings_projects


class Column(models.Model):
    """ Info you want to display (milestone, activity, title, ...)
    """
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


def default_columns():
    columns = []
    for column in settings_projects.DEFAULT_COLUMNS:
        columns.append(Column.objects.get(name=column))

    return columns

class Project(models.Model):
    """ Project: group of many github repo
    """
    name = models.CharField(max_length=256, unique=True)
    columns = models.ManyToManyField("Column", default=default_columns)

    def __eq__(self, other):
        return self.name == other

    def __str__(self):
        return self.name


class Repo(models.Model):
    """ Repo: github repo
    """
    name = models.CharField(max_length=256, unique=True)
    projects = models.ManyToManyField(Project)

    def __eq__(self, other):
        return self.name == other

    def __str__(self):
        return self.name
