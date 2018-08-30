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

from werkzeug.local import LocalProxy
from importlib import import_module

# Interfaces
from . import Utils as WebUtils


class WebModule:
    #: Уникальное имя модуля
    _instance_name = "Module"
    #: Уникальный префикс фильтров модуля
    _instance_filter = "_4g_module_filter"
    #: Имя ноды в конфиге
    _instance_config = "module-dummy"
    #: Путь до шаблона
    _template_name = "/dummy/module.html"
    #: Контекс
    _context = {}
    #: Список маршрутов обрабатываемых модулем
    _routes = {
        
    }
    #: HTTP Return Code
    _http_code = 200
    #: Перечень зависимостей
    _dependency = []
    
    def __init__(self, application, page=None):
        self._application = application
        self._page = page
        self._site = self._application.site

        self._config = self._application.config_xml
        self._database = LocalProxy(self._application.database.request_get)
        self._form = WebUtils.WebForm(self._application)
        
        self.load()
        
    @property
    def template_name(self):
        """
            Свойство возвращающее название шаблона.
            
            :return: Название шаблона
            :rtype: String
        """
        return self._template_name
 
    
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
    
    
    def load(self):
        pass
    
    def render(self, caller=None):
        if self._page:
            return self._application.render(self._page.template_name, self._page, self._page.module, http_code=self._http_code)
        else:
            return self._application.render(self._template_name, self._context, self, http_code=self._http_code)
    
    
    def render_json(self,json_object, caller=None):
        if self._page:
            return self._application.render_json(json_object, self._page, self._page.module, http_code=self._http_code)
        else:
            return self._application.render_json(json_object, self._context, self, http_code=self._http_code)
    
    
    def register_routes(self):
        for route in self._routes.keys():
            route_func_name = self._routes[route]
            route_func = getattr(self, route_func_name)
            
            self._application.add_url_rule(route, '{}{}'.format(str(route).replace("/", "_"), route_func_name), route_func, methods=['GET', 'POST'])
    
    
    def register(self):
        self._application.module_register(self._instance_name, self)
        
        self.register_routes()


    @property
    def module_name(self):
        return self._instance_name.replace("/", "")

    @staticmethod
    def module_load(page):
        module_list = page.application._config.get("web", "application", "module_list", "Scopuli.WEB.Application.Modules")
        module = getattr(import_module(module_list), page.code)
    
        if module:
            return module(page.application, page)

        return None

    def make_url(self, module_name, module_value, module_prefix="/"):
        from Scopuli.Interfaces.MySQL.Schema.Web.Core import WebPage as dbWebPage
        
        query = self._database.query(dbWebPage)
        query = query.filter(dbWebPage.cd_web_site == self._site.id)
        query = query.filter(dbWebPage.is_enable == 1)
        query = query.filter(dbWebPage.code == module_name)

        for module in query.all():
            return "{}{}{}".format(module.url, module_prefix, module_value)


    def callback_render(self, template, web_page, web_module):
        pass
    
    
    @property
    def sitemap_links(self):
        """
            Функция возвращает список ссылок для карты сайта
             
            :return: Массив ссылок для карты сайта
            :rtype: Array of String
        """
        return []
    
    
    @property
    def robots_disallow(self):
        """
            Функция возвращает список запрещенных ссылок для индексирования в robots.txt

            :return: Массив запрещенных ссылок для robots.txt
            :rtype: Array of String
        """
        return []


    @property
    def robots_allow(self):
        """
            Функция возвращает список разрешенный ссылок для индексирования в robots.txt
            
            :return: Массив разрещенных ссылок для robots.txt
            :rtype: Array of String
        """
        return []


    def __repr__(self):
        return u"<{} template:'{}' instance:'{}' />".format(str(self.__class__), self._template_name, self._instance_name)