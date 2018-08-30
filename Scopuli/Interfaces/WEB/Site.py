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

from flask import request

from werkzeug.local import LocalProxy

# Interfaces
from . import WebPage


class WebSite:
    def __init__(self, application, site_load=True):
        self._application = application
        self._config = self._application.config_xml
        self._database = LocalProxy(self._application.database.context_get)

        self._sql = None

        if site_load:
            self._id = int(self._config.get("web", "", "site_id", "-1"))
            
        self._title = "Undefined"
        self._description = "Undefined"
        self._url = "Undefined"

        self._is_loaded = False
        self._is_enable = True
        self._is_secure = False
        self._is_devel = True

        self._meta_title = "Undefined"
        self._meta_description = "Undefined"
        self._meta_autor = "Undefined"
        self._meta_autor_url = "Undefined"
        self._meta_description = "Undefined"
        self._meta_keywords = "Undefined"
        self._meta_copyrights = "Undefined"
        
        self._pages = []
        
        if site_load:
            self.load()

    def load(self, db_site=None):
        from Scopuli.Interfaces.MySQL.Schema.Web.Core import WebSite as dbWebSite
        if db_site is None:
            query = self._database.query(dbWebSite)
            query = query.filter(dbWebSite.id == self._id)
            self._sql = query.first()
        else:
            self._sql = db_site
            
        if self._sql:
            self._id = self._sql.id
            self._title = self._sql.title
            self._description = self._sql.description
            self._url = self._sql.url

            self._is_loaded = True
            self._is_enable = self._sql.is_enable
            self._is_secure = self._sql.is_secure
            self._is_devel = self._sql.is_devel
            
            self._meta_title = self._sql.meta_title
            self._meta_description = self._sql.meta_description
            self._meta_autor = self._sql.meta_autor
            self._meta_autor_url = self._sql.meta_autor_url
            self._meta_keywords = self._sql.meta_autor_url
            self._meta_copyrights = self._sql.meta_copyrights

            for db_page in self._sql.pages:
                self._pages.append(WebPage(application=self._application, page_id=db_page.id, page_load=False).load(db_page=db_page))
        
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
    def title(self):
        return self._title
    
    @property
    def description(self):
        return self._description

    @property
    def url(self):
        return self._url

    @property
    def url_prefix(self):
        if self._is_secure:
            return "https://"
        else:
            return "http://"

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
    def meta_copyrights(self):
        return self._meta_copyrights


    @property
    def is_loaded(self):
        return self._is_loaded

    @property
    def is_enable(self):
        return self._is_enable

    @property
    def is_secure(self):
        return self._is_secure

    @property
    def is_devel(self):
        return self._is_devel

    @property
    def pages(self):
        return self._pages


    def __repr__(self):
        return u"<{} id:'{}' is_enable:'{}' is_secure:'{}' url:'{}' title:'{}' description:'{}' />".format(str(self.__class__), self._id,
                                                                                                           self._is_enable, self._is_secure,
                                                                                                           self._url, self._title,
                                                                                                           self._description)