#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright [2017] Tatarnikov Viktor [viktor@tatarnikov.org]
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

from flask import request
from datetime import datetime
from werkzeug.local import LocalProxy

import Interfaces.MySQL.Schema as Schema
import Interfaces.WEB.Module


class WebPage:
    def __init__(self, application, page_id, page_load=True):
        self._application = application
        self._config = self._application.config_xml
        self._database = LocalProxy(self._application.database.context_get)

        self._sql = None
        self._module = None
        
        self._id = page_id
        self._cd_parent = "Undefined"

        self._code = "Undefined"

        self._title = "Undefined"
        self._description = "Undefined"

        self._url = "Undefined"
        self._url_title = "Undefined"
        self._url_title_short = "Undefined"
        self._url_discription = "Undefined"
        self._url_discription_short = "Undefined"

        self._is_enable = False
        self._is_loaded = False
        
        self._template_name = "Undefined"

        self._meta_title = "Undefined"
        self._meta_description = "Undefined"
        self._meta_autor = "Undefined"
        self._meta_autor_url = "Undefined"
        self._meta_keywords = "Undefined"

        self._date_create = datetime.today()
        self._date_change = datetime.today()

        if page_load:
            self.load()

    def load(self, db_page=None):
        if db_page is None:
            query = self._database.query(Schema.WebPage)
            query = query.filter(Schema.WebPage.id == self._id)
            self._sql = query.first()
        else:
            self._sql = db_page
         
        if self._sql:
            self._cd_parent = self._sql.cd_parent
    
            self._code = self._sql.code
    
            self._title = self._sql.title
            self._description = self._sql.description
    
            self._url = self._sql.url
            self._url_title = self._sql.url_title
            self._url_title_short = self._sql.url_title_short
            self._url_description = self._sql.url_description
            self._url_description_short = self._sql.url_description_short
    
            self._is_enable = self._sql.is_enable
            self._is_loaded = True
    
            self._template_name = self._sql.template_name
        
            self._meta_title = self._sql.meta_title
            self._meta_description = self._sql.meta_description
            self._meta_autor = self._sql.meta_autor
            self._meta_autor_url = self._sql.meta_autor_url
            self._meta_keywords = self._sql.meta_autor_url

            self._date_create = self._sql.date_create
            self._date_change = self._sql.date_change

        return self


    @property
    def application(self):
        """
            Свойство возвращающее текущее приложение.

            :return: Загруженный обьект :ref:`module-web-application`
            :rtype: :ref:`module-web-application`
        """
        return self._application


    @property
    def config(self):
        """
            Свойство возвращающее текущий конфиг.

            :return: Загруженный обьект :ref:`module-interfaces-config`
            :rtype: :ref:`module-interfaces-config`
        """
        return self._config


        
    @property
    def id(self):
        return self._id
    
    @property
    def cd_parent(self):
        return self._cd_parent
    
    @property
    def code(self):
        return self._code
    
    @property
    def title(self):
        return self._title
    
    @property
    def description(self):
        return self._description

    @property
    def url(self):
        return self._url
    
    @property
    def url_title(self, short=False):
        if short:
            if len(self._url_title_short) != 0:
                return self._url_title_short

        return self._url_title
    
    @property
    def url_description(self, short=False):
        if short:
            if len(self._url_description_short) != 0:
                return self._url_description_short

        return self._url_description
    
    @property
    def is_enable(self):
        return self._is_enable

    
    @property
    def is_loaded(self):
        if self._is_loaded and self._module:
            return True
    
        return False

    @property
    def meta_autor(self):
        return self._meta_autor

    @property
    def meta_autor_url(self):
        return self._meta_autor_url

    @property
    def meta_title(self):
        return self._meta_title
    
    @property
    def meta_description(self):
        return self._meta_description

    @property
    def meta_keywords(self):
        return self._meta_keywords

    @property
    def date_create(self):
        return self._date_create

    @property
    def date_change(self):
        return self._date_change

    @property
    def robots_disallow(self):
        if self._module:
            if hasattr(self._module, "robots_disallow"):
                return self._module.robots_disallow
        
        return []
    
    @property
    def robots_allow(self):
        if self._module:
            if hasattr(self._module, "robots_allow"):
                return self._module.robots_allow

        return []
    
    @property
    def sitemap_links(self):
        if self._module:
            if hasattr(self._module, "sitemap_links"):
                return self._module.sitemap_links

        return []
    
    @property
    def module(self):
        if not self._module:
            self._module = Interfaces.WEB.Module.module_load(self)
            
        return self._module
    
    @property
    def template_name(self):
        if len(self._template_name) != 0:
            return self._template_name
        
        if self._module:
            return self._module.template_name
        
        return "dummy/module.html"

    def __repr__(self):
        return u"<{} id:'{}' parent:'{}' is_enable:'{}' code:'{}' url:'' template:'{}' />".format(str(self.__class__), self._id, self._cd_parent,
                                                                                                 self._is_enable, self._code, self._url,
                                                                                                 self._template_name)
