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


from Scopuli.Interfaces.WEB.Module import WebModule

from flask import request, session, abort, redirect


class WebFavicon(WebModule):
    _instance_name = "Hook/Favicon"
    _template_name = ""
    _dependency = ['']
    _routes = {
        "/favicon.ico": 'render',
        "/manifest.json": 'render',
        "/browserconfig.xml": 'render',
    }

    def register(self):
        self.register_routes()

    def render(self, caller=None):
        self._application.render_callback(None, None, self)
        
        return self._application.send_static_file("favicons/{}".format(request.path))
