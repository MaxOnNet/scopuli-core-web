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


from flask import abort
from ..Club import WebClub


class WebClubCoacher(WebClub):
    _instance_name = "Club/Coacher"
    _template_name = "/club/coacher/module.html"
    _routes = {}

    @property
    def sitemap_links(self):
        for coacher in self.coachers:
            yield {'url': coacher.web_url, 'lastmod': coacher.date_change}

    
    def load(self):
        WebClub.load(self)
    
        self._routes = {
            "{}/<string:name>".format(self._page.url): 'render'
        }
    
    
    def render(self, name, caller=None):
        self.set_filter_type("coacher")
        self.set_filter_value(name)
        
        if self.coacher is None:
            abort(404)
        
        return WebClub.render(self, caller)


