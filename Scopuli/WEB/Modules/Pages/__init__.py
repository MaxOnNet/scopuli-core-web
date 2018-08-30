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


class WebPage_Index(WebModule):
    _instance_name = "PageIndex"
    _template_name = "index/module.html"
    _routes = {
        "/"       : 'render',
        "/home"   : 'render',
        "/index"  : 'render',
        "/default": 'render'
    }
    _dependency = []


class WebPage_Simple(WebModule):
    _template_name = ""
    _routes = {}
    _dependency = []
    
    
    def load(self):
        self._template_name = self._page._template_name
        self._routes = {
            "{}".format(self._page.url) : 'render',
            "{}/".format(self._page.url): 'render'
        }
