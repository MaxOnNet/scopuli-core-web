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


from ..Club import WebClub


class WebClubOffers(WebClub):
    _instance_name = "Club/Offers"
    _template_name = "/club/offers/module.html"
    _routes = {}
    
    
    def load(self):
        WebClub.load(self)
        
        self._routes = {
            "{}".format(self._page.url): 'render',
            "{}/download/<string:render_mode>".format(self._page.url): 'render_download',
    
            "{}/by/<string:search_type>/<string:search_value>".format(self._page.url): 'render_search',
            "{}/by/<string:search_type>/<string:search_value>/download/<string:render_mode>".format(self._page.url): 'render_search_download'
        }


    def render_search_download(self, search_type, search_value, render_mode, caller=None):
        self.set_filter_type(search_type)
        self.set_filter_value(search_value)

        return self.render_download(render_mode, caller)
    
    def render_download(self, render_mode, caller=None):
        return WebClub.render(self, caller)
