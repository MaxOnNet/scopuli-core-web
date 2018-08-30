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

_ = lambda x: x


class HttpHeadersDebugPanel(DebugPanel):
    """
    A panel to display HTTP headers.
    """
    name = 'HttpHeader'
    has_content = True
    
    # List of headers we want to display
    header_filter = (
        'CONTENT_TYPE',
        'HTTP_ACCEPT',
        'HTTP_ACCEPT_CHARSET',
        'HTTP_ACCEPT_ENCODING',
        'HTTP_ACCEPT_LANGUAGE',
        'HTTP_CACHE_CONTROL',
        'HTTP_CONNECTION',
        'HTTP_HOST',
        'HTTP_KEEP_ALIVE',
        'HTTP_REFERER',
        'HTTP_USER_AGENT',
        'QUERY_STRING',
        'REMOTE_ADDR',
        'REMOTE_HOST',
        'REQUEST_METHOD',
        'SCRIPT_NAME',
        'SERVER_NAME',
        'SERVER_PORT',
        'SERVER_PROTOCOL',
        'SERVER_SOFTWARE',
    )

    def nav_title(self):
        return _('HTTP Заголовки')

    def title(self):
        return _('HTTP Заголовки')

    def url(self):
        return ''

    def process_request(self, request):
        self.headers = dict(
            [(k, request.environ[k])
                for k in self.header_filter if k in request.environ]
        )

    def content(self):
        context = self.context.copy()
        context.update({
            'headers': self.headers
        })
        return self.render('panels/headers.html', context)
