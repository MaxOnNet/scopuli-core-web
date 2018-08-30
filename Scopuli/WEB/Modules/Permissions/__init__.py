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

from datetime import datetime
from flask import request, session, abort


class WebPermissions(WebModule):
    _instance_name = "Permissions"
    _template_name = ""
    _routes = {}
    _dependency = ["Session"]
    
    _order = ["Permit", "Denied"]
    
    
    def register(self):
        self._application.module_register(self._instance_name, self)
        
        self._application.before_request(self._request_init)
        self._application.teardown_request(self._request_teardown)
    
    
    def _request_init(self):
        if request:
            if request.endpoint != "static":
                pass
    
    
    def _request_teardown(self, exception):
        if request:
            if request.endpoint != "static":
                pass
    
    
    def callback_render(self, template, web_page, web_module):
        # check rules
        pass
