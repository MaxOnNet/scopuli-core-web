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


class WebContacts(WebModule):
    _instance_name = "Contacts"
    _template_name = ""
    _routes = {}
    _dependency = []
    _google_api_gmap = ""
    
    
    def load(self):
        self._template_name = "/contacts/module.html"
        self._routes = {
            "{}".format(self._page.url)     : 'render',
            "{}/".format(self._page.url)    : 'render',
            "{}/send".format(self._page.url): 'render_send'
        }
        
        self._google_api_gmap = self._config.get("web", "google-api", "gmap", "")
    
    
    def render_send(self, caller=None):
        return '{ "alert": "success", "message": "Сообщение отправлено, спасибо за Сотрудничество!" }', 200
    
    
    @property
    def google_map_key(self):
        return self._google_api_gmap
