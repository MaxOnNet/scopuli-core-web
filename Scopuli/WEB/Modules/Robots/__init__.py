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


class WebRobots(WebModule):
    _instance_name = "Robots"
    _template_name = ""
    _dependency = ['']
    _routes = {
        "/robots.txt": 'render'
    }
    
    
    def register(self):
        self.register_routes()
    
    
    def render(self, caller=None):
        self._application.render_callback(None, None, self)
        
        robots_txt = ""
        robots_txt = "{}{}\n\n".format(robots_txt, self._make_yandex())
        robots_txt = "{}{}\n\n".format(robots_txt, self._make_google())
        robots_txt = "{}{}\n\n".format(robots_txt, self._make_all())
        
        return robots_txt, 200
    
    
    def _make_yandex(self):
        robots_txt = "User-Agent: Yandex \n"
        robots_disallow_exist = False
        
        for page in self._site.pages:
            for rule in page.robots_disallow:
                robots_txt += "Disallow: {}\n".format(rule)
                robots_disallow_exist = True
        
        for page in self._site.pages:
            for rule in page.robots_allow:
                robots_txt += "Allow: {}\n".format(rule)
        
        if not robots_disallow_exist:
            robots_txt += "Disallow: \n"
        
        robots_txt += "Crawl-delay: 2\n"
        robots_txt += "Sitemap: {}{}/sitemap.xml\n".format(self._site.url_prefix, self._site.url)
        robots_txt += "Host: {}".format(self._site.url)
        
        return robots_txt
    
    
    def _make_google(self):
        robots_txt = "User-Agent: googlebot \n"
        robots_disallow_exist = False
        
        for page in self._site.pages:
            for rule in page.robots_disallow:
                robots_txt += "Disallow: {}\n".format(rule)
                robots_disallow_exist = True
        
        for page in self._site.pages:
            for rule in page.robots_allow:
                robots_txt += "Allow: {}\n".format(rule)
        
        if not robots_disallow_exist:
            robots_txt += "Disallow: \n"
        
        robots_txt += "Sitemap: {}{}/sitemap.xml\n".format(self._site.url_prefix, self._site.url)
        robots_txt += "Host: {}".format(self._site.url)
        
        return robots_txt
    
    
    def _make_all(self):
        robots_txt = "User-Agent: * \n"
        robots_disallow_exist = False
        
        for page in self._site.pages:
            for rule in page.robots_disallow:
                robots_txt += "Disallow: {}\n".format(rule)
                robots_disallow_exist = True
        
        for page in self._site.pages:
            for rule in page.robots_allow:
                robots_txt += "Allow: {}\n".format(rule)
        
        if not robots_disallow_exist:
            robots_txt += "Disallow: \n"
        
        robots_txt += "Sitemap: {}{}/sitemap.xml\n".format(self._site.url_prefix, self._site.url)
        robots_txt += "Host: {}".format(self._site.url)
        
        return robots_txt
