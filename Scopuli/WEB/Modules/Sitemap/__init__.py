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
import xml.dom.minidom as xdom


class WebSitemap(WebModule):
    _instance_name = "Sitemap"
    _template_name = ""
    _dependency = ['Robots']
    _routes = {
        "/sitemap.xml": 'render'
    }
    
    
    def register(self):
        self.register_routes()
    
    
    def render(self, caller=None):
        self._application.render_callback(None, None, self)
        
        xml_document = xdom.Document()
        xml_sitemap = xml_document.createElement('urlset')
        xml_sitemap.setAttribute("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        
        for page in self._site.pages:
            page_links_exist = False
            
            for page_links in page.sitemap_links:
                self._make_node_url(xml_document, xml_sitemap,
                                    "{}{}{}/{}".format(self._site.url_prefix, self._site.url, page.url, page_links['url']),
                                    page_links['lastmod'].strftime('%Y-%m-%d'))
                
                page_links_exist = True
            
            if not page_links_exist:
                self._make_node_url(xml_document, xml_sitemap, "{}{}{}".format(self._site.url_prefix, self._site.url, page.url),
                                    page.date_change.strftime('%Y-%m-%d'))
        
        xml_document.appendChild(xml_sitemap)
        
        return xml_document.toprettyxml("\t", "\n", encoding="UTF-8"), 200
    
    
    @staticmethod
    def _make_node_url(xml_document, xml_sitemap, page_url, page_lastmod):
        xml_url = xml_document.createElement('url')
        
        xml_loc = xml_document.createElement('loc')
        xml_loc.appendChild(xml_document.createTextNode(page_url))
        
        xml_lastmod = xml_document.createElement('lastmod')
        xml_lastmod.appendChild(xml_document.createTextNode(page_lastmod))
        
        xml_url.appendChild(xml_loc)
        xml_url.appendChild(xml_lastmod)
        
        xml_sitemap.appendChild(xml_url)