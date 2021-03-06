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


class WebClubRoom(WebClub):
    _instance_name = "Club/Room"
    _template_name = "/club/room/module.html"
    

    @property
    def sitemap_links(self):
        for room in self.rooms:
            yield {'url': room.web_url, 'lastmod': room.date_change}



    def load(self):
        WebClub.load(self)
        
        self._routes = {
            "{}/<string:name>".format(self._page.url): 'render'
        }
    
    
    def render(self, name, caller=None):
        self.set_filter_type("room")
        self.set_filter_value(name)
        
        if self.room is None:
            abort(404)
        
        return WebClub.render(self, caller)
