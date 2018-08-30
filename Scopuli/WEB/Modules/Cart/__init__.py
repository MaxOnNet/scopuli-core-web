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

from flask import jsonify


class WebCart(WebModule):
    _instance_name = "Cart"
    _template_name = ""
    _routes = {}
    _dependency = ['Session']
    
    
    @property
    def robots_disallow(self):
        return [self._page.url]
    
    
    def load(self):
        self._template_name = "/cart/module.html"
        self._routes = {
            "{}".format(self._page.url)                          : 'render',
            "/json{}/get".format(self._page.url)                 : 'json_get',
            "/json{}/insert".format(self._page.url)              : 'json_insert',
            "/json{}/update/<int:item_id>".format(self._page.url): 'json_update',
            "/json{}/delete/<int:item_id>".format(self._page.url): 'json_delete'
        }
    
    
    def json_get(self, caller=None):
        return jsonify({'dummy': 'none'})
    
    
    def json_insert(self, caller=None):
        return jsonify({'dummy': 'none'})
    
    
    def json_update(self, item_id, caller=None):
        return jsonify({'dummy': 'none'})
    
    
    def json_delete(self, item_id, caller=None):
        return jsonify({'dummy': 'none'})