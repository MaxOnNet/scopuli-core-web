#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright [2017] Tatarnikov Viktor [viktor@tatarnikov.org]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
from distutils.sysconfig import get_python_lib

from flask import __version__ as flask_version
from Scopuli.WEB.DebugToolbar.Panels import DebugPanel

_ = lambda x: x


def relpath(location, python_lib):
    location = os.path.normpath(location)
    relative = os.path.relpath(location, python_lib)
    if relative == os.path.curdir:
        return ''
    elif relative.startswith(os.path.pardir):
        return location
    return relative


class VersionsDebugPanel(DebugPanel):
    """
    Panel that displays the Flask version.
    """
    name = 'Version'
    has_content = True

    def nav_title(self):
        return _('Versions')

    def nav_subtitle(self):
        return 'Flask %s' % flask_version

    def url(self):
        return ''

    def title(self):
        return _('Versions')

    def content(self):
        try:
            import pkg_resources
        except ImportError:
            packages = []
        else:
            packages = sorted(pkg_resources.working_set,
                              key=lambda p: p.project_name.lower())

        return self.render('panels/versions.html', {
            'packages': packages,
            'python_lib': os.path.normpath(get_python_lib()),
            'relpath': relpath,
        })
