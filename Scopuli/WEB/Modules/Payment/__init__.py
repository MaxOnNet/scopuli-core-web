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

from flask import redirect, request, abort, jsonify
from flask.json import JSONEncoder


class WebPayment(WebModule):
    _instance_name = "Payment"
    _template_name = "/payment/module.html"
    _routes = {}
    _steps = []
    _dependency = ['Session', 'Cart']
    
    
    @property
    def robots_disallow(self):
        return [self._page.url]
    
    
    def load(self):
        self._template_name = "/payment/module.html"
        self._routes = {
            "{}".format(self._page.url)                                       : 'render',
            "{}/transfer".format(self._page.url)                              : 'render_transfer',
            "{}/response/ok".format(self._page.url)                           : 'render_response_good',
            "{}/response/fault".format(self._page.url)                        : 'render_response_failed',
            "{}/<uuid:order_uuid>".format(self._page.url)                     : 'render_order',
            "{}/<uuid:order_uuid>/<string:render_mode>".format(self._page.url): 'render_order_with_mode'
        }
    
    
    @property
    def basket(self):
        if hasattr(request, '_4g_basket'):
            return getattr(request, '_4g_basket')
        else:
            return []
    
    
    def _payment_make(self, amount, client_email, client_phone, client_uuid):
        pass
    
    
    def render_order_with_mode(self, order_uuid, render_mode, caller=None):
        return self.render(caller)
    
    
    def render_order(self, order_uuid, caller=None):
        return self.render(caller)
    
    
    def render_simple(self, amount, caller=None):
        if amount <= 0 or amount >= 50000:
            abort(403)
        
        request._4g_basket = [{'id': 0, 'name': "Пополнение счета", 'count': 1, 'amount': amount, 'editable': False}]
        
        return self.render(caller)
    
    
    def render_transfer(self, caller=None):
        pass
    
    
    def render_response_query(self, caller=None):
        return self.render(caller)
    
    
    def render_response_good(self, caller=None):
        return self.render(caller)
    
    
    def render_response_failed(self, caller=None):
        return self.render(caller)
    
    
    def _payment_configure(self):
        pass
    
    
    def _payment_register(self, payment):
        pass
