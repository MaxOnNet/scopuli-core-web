#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright [2018] Tatarnikov Viktor [viktor@tatarnikov.org]
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
""" """

class DebugPanel(object):
    """
    Base class for debug panels.
    """
    name = 'Base'

    # If content returns something, set to true in subclass
    has_content = False

    # If the client is able to activate/de-activate the panel
    user_enable = False

    # We'll maintain a local context instance so we can expose our template
    # context variables to panels which need them:
    context = {}

    # Panel methods
    def __init__(self, jinja_env, context={}):
        self.context.update(context)
        self.jinja_env = jinja_env

        # If the client enabled the panel
        self.is_active = False

    def render(self, template_name, context):
        template = self.jinja_env.get_template(template_name)
        return template.render(**context)

    def dom_id(self):
        return 'flDebug%sPanel' % (self.name.replace(' ', ''))

    def nav_title(self):
        """Title showing in toolbar"""
        raise NotImplementedError

    def nav_subtitle(self):
        """Subtitle showing until title in toolbar"""
        return ''

    def title(self):
        """Title showing in panel"""
        raise NotImplementedError

    def url(self):
        raise NotImplementedError

    def content(self):
        raise NotImplementedError

    # Standard middleware methods
    def process_request(self, request):
        pass

    def process_view(self, request, view_func, view_kwargs):
        pass

    def process_response(self, request, response):
        pass
