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
from flask import session

from Scopuli.WEB.DebugToolbar.Panels import DebugPanel

_ = lambda x: x


class RequestDebugPanel(DebugPanel):
    """
    A panel to display request variables (POST/GET, session, cookies).
    """
    name = 'RequestVars'
    has_content = True

    def nav_title(self):
        return _('Request Vars')

    def title(self):
        return _('Request Vars')

    def url(self):
        return ''

    def process_request(self, request):
        self.request = request
        self.session = session
        self.view_func = None
        self.view_args = []
        self.view_kwargs = {}

    def process_view(self, request, view_func, view_kwargs):
        self.view_func = view_func
        self.view_kwargs = view_kwargs

    def content(self):
        context = self.context.copy()
        context.update({
            'get': self.request.args.lists(),
            'post': self.request.form.lists(),
            'cookies': self.request.cookies.items(),
            'view_func': ('%s.%s' % (self.view_func.__module__,
                                     self.view_func.__name__)
                          if self.view_func else '[unknown]'),
            'view_args': self.view_args,
            'view_kwargs': self.view_kwargs or {},
            'session': self.session.items(),
        })

        return self.render('panels/request_vars.html', context)
