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


from ..Blog import WebBlog


class WebBlogTags(WebBlog):
    _instance_name = "Blog/Tags"
    _template_name = "/blog/tags/module.html"
    _routes = {}
    
    
    def load(self):
        WebBlog.load(self)
        
        self._routes = {
            "{}".format(self._page.url): 'render'
        }


    def render(self, caller=None):
        # Init Pager
        self.set_page_settings()
        self.set_page_data(self.tags)
    
        return WebBlog.render(self, caller)
