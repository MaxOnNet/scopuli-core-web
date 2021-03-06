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

from Scopuli.WEB.DebugToolbar.Panels import DebugPanel
from flask import current_app

_ = lambda x: x


class AppRoutesDebugPanel(DebugPanel):
    """
    Panel that displays the URL routing rules.
    """
    name = 'RouteList'
    has_content = True
    routes = []

    def nav_title(self):
        return _('Route List')

    def title(self):
        return _('Route List')

    def url(self):
        return ''

    def nav_subtitle(self):
        count = len(self.routes)
        return '%s %s' % (count, 'route' if count == 1 else 'routes')

    def process_request(self, request):
        self.routes = list(current_app.url_map.iter_rules())

    def content(self):
        return self.render('panels/route_list.html', {
            'routes': self.routes,
        })
