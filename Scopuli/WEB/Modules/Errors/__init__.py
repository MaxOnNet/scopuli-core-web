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


class WebError_400(WebModule):
    _template_name = "/errors/400.html"
    
    _routes = {
        "/errors/400": 'render'
    }
    _http_code = 400
    _dependency = []
    
    
    def register(self):
        self.register_routes()
        
        self._application.register_error_handler(self._http_code, self.render)


class WebError_401(WebModule):
    _template_name = "/errors/401.html"
    
    _routes = {
        "/errors/401": 'render'
    }
    _http_code = 401
    _dependency = []
    
    
    def register(self):
        self.register_routes()
        
        self._application.register_error_handler(self._http_code, self.render)


class WebError_404(WebModule):
    _template_name = "/errors/404.html"
    
    _routes = {
        "/errors/404": 'render'
    }
    _http_code = 404
    _dependency = []
    
    
    def register(self):
        self.register_routes()
        
        self._application.register_error_handler(self._http_code, self.render)

