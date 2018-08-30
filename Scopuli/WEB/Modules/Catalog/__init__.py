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
import Scopuli.Interfaces.MySQL.Schema.Web.Module.Catalog as Schema

from flask import request, abort
from werkzeug.local import LocalProxy


class WebCatalog(WebModule):
    _instance_name = "Catalog"
    _template_name = "/catalog/module.html"
    _routes = {}
    
    _dependency = []
    
    filter_type = ""
    filter_value = ""
    
    
    def load(self):
        self.filter_type = LocalProxy(self.get_filter_type)
        self.filter_value = LocalProxy(self.get_filter_value)
        
        self._routes = {
            "{}".format(self._page.url)             : 'render_root',
            "{}/<string:url>".format(self._page.url): 'render_child'
        }
    
    
    @staticmethod
    def get_filter_type():
        __filter_type = getattr(request, '_4g_catalog_filter_type', None)
        
        if __filter_type is not None:
            return __filter_type
        else:
            return ""
    
    
    @staticmethod
    def set_filter_type(value):
        setattr(request, '_4g_catalog_filter_type', value)
    
    
    @staticmethod
    def get_filter_value():
        __filter_value = getattr(request, '_4g_catalog_filter_value', None)
        
        if __filter_value is not None:
            return __filter_value
        else:
            return ""
    
    
    @staticmethod
    def set_filter_value(value):
        setattr(request, '_4g_catalog_filter_value', value)
    
    
    @property
    def item(self):
        if self.filter_type == "url":
            query = self._database.query(Schema.WebModuleCatalog)
            query = query.filter(Schema.WebModuleCatalog.cd_web_site == self._site.id)
            query = query.filter(Schema.WebModuleCatalog.is_published == True)
            query = query.filter(Schema.WebModuleCatalog.is_deleted == False)
            query = query.filter(Schema.WebModuleCatalog.url == self.filter_value)
            
            for item in query.all():
                return item
        
        return None
    
    
    @property
    def items(self):
        query = self._database.query(Schema.WebModuleCatalog)
        query = query.filter(Schema.WebModuleCatalog.cd_web_site == self._site.id)
        query = query.filter(Schema.WebModuleCatalog.is_deleted == False)
        query = query.filter(Schema.WebModuleCatalog.is_published == True)
        
        if self.filter_type == "url":
            query = query.filter(Schema.WebModuleCatalog.cd_parent == self.item.id)
        
        items = []
        for item in query.all():
            items.append(item)
        
        return items
    
    
    def render_root(self, caller=None):
        self.set_filter_type("")
        self.set_filter_value("")
        
        return WebModule.render(self)
    
    
    def render_child(self, url=None, caller=None):
        self.set_filter_type("url")
        self.set_filter_value(url)
        
        if self.item is None:
            abort(404)
        
        return WebModule.render(self)
