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

from flask import request, redirect, session
from werkzeug.local import LocalProxy


class Pager:
    _module = None
    _config = None
    _application = None

    _instance_name = "Pager"
    
    def __init__(self):
        pass

    def load_pager(self, module):
        self._module = module
        self._config = module._config
        self._application = module._application

        self._load_mode = self._config.get("web", self._module._instance_config, "page_load_mode", "pager")  # pager | infiniti
        self._display_mode = self._config.get("web", self._module._instance_config, "page_display_mode", "list")  # list | grid
        self._item_count = int(self._config.get("web", self._module._instance_config, "page_items_count", 20))  # list | grid

        # propertys
        self.page_load_mode = LocalProxy(self.get_page_load_mode)
        self.page_display_mode = LocalProxy(self.get_page_display_mode)
        self.page_items_count = LocalProxy(self.get_page_items_count)
        self.page_data = LocalProxy(self.get_page_data)


    def _get_property_name(self, name):
        """
            Генерация имени параметра с привязкой к подключенному модулю.
            
            :param name: Имя параметра
            :return: Уникальное имя параметра
        """
        return "{}-{}-{}".format(self._module._instance_name.lower(), Pager._instance_name.lower(), name)


    def _get_property(self, name, default, use_session=True):
        """
            Получение значение параметра из обьекта request или модуля :ref:`module-web-modules-session`.
            
            :param name: Имя параметра
            :type name: String
            :param default: Значение по умолчанию
            :type default: Any
            :param use_session: Использовать сессию для поиска
            :type use_session: Boolean
            :return: Значение параметра
        """
        prop_name = self._get_property_name(name)
        prop_value_session = None
        prop_value_request = getattr(request, prop_name, None)
        
        if use_session:
            if self._application.module_exist("Session"):
                prop_value_session = self._application.module_request("Session").get_property(prop_name)

        if prop_value_request is not None:
            return prop_value_request
        elif prop_value_session is not None and use_session:
            return prop_value_session
    
        return default


    def _set_property(self, name, value, use_session=True):
        """
            Сохранение значение параметра в обьект request и модуль :ref:`module-web-modules-session`.

            :param name: Имя параметра
            :type name: String
            :param value: Значение параметра
            :type value: Any
            :param use_session: Использовать сессию для сохранения
            :type use_session: Boolean
            :return: Nothing
            :rtype None:
        """
        prop_name = self._get_property_name(name)
        
        if use_session:
            if self._application.module_exist("Session"):
                self._application.module_request("Session").set_property(prop_name, value)
         
        setattr(request, prop_name, value)
    
    
    def get_page_display_mode(self):
        """
            Получение значения типа текущего фильтра из сессии.

            :return: Тип используемого фильтра
            :rtype: String
        """
        return self._get_property('display_mode', self._display_mode)
        
    def set_page_display_mode(self, value):
        """
            Сохраниение значения типа фильтра в сессии.

            :param value: Тип используемого фильтра
            :type value: String

            :return: None
        """
        self._set_property('display_mode', value)

    def get_page_load_mode(self):
        """
            Получение значения типа текущего фильтра из сессии.

            :return: Тип используемого фильтра
            :rtype: String
        """
        return self._get_property('load_mode', self._load_mode)

    def set_page_load_mode(self, value):
        """
            Сохраниение значения типа фильтра в сессии.

            :param value: Тип используемого фильтра
            :type value: String

            :return: None
        """
        self._set_property('load_mode', value)

    def get_page_items_count(self):
        """
            Получение значения типа текущего фильтра из сессии.

            :return: Тип используемого фильтра
            :rtype: String
        """
        return self._get_property('items_count', self._item_count)

    def set_page_item_count(self, value):
        """
            Сохраниение значения типа фильтра в сессии.

            :param value: Тип используемого фильтра
            :type value: String

            :return: None
        """
        self._set_property('items_count', value)

    def get_page_data(self):
        """
            Получение значения типа текущего фильтра из сессии.

            :return: Тип используемого фильтра
            :rtype: String
        """
        __data = self._get_property('data', None, False)
        __data_return = []
        
        if __data is not None:
            for data_index in xrange((self.page_current-1) * self.page_items_count, self.page_current * self.page_items_count, 1):
                if data_index < len(__data):
                    __data_return.append(__data[data_index])

        return __data_return

    def set_page_data(self, value):
        """
            Сохраниение значения типа фильтра в сессии.

            :param value: Тип используемого фильтра
            :type value: String

            :return: None
        """
        self._set_property('data', value, False)

    def set_page_settings(self):
        """
            Сохраниение значения типа фильтра в сессии.

            :param value: Тип используемого фильтра
            :type value: String

            :return: None
        """
        if request.method == "POST":
            self.set_page_display_mode(self._module._form.get("page_display_mode", attribute_type="string", requred=True))
            self.set_page_load_mode(self._module._form.get("page_load_mode", attribute_type="string", requred=True))
            self.set_page_item_count(int(self._module._form.get("page_items_count", attribute_type="integer", requred=True)))


    @property
    def page_current(self):
        """
            Функция возвращает текущую страницу, начиная с 1.
            
            :rtype: Int
            :return: Номер текущей страницы
        """
        if request.method == "GET":
            if 'page' in request.args:
                if str.isdigit(str(request.args['page'])):
                    if int(request.args['page']) > 0:
                        return int(request.args['page'])
                    
        return 1
       
        
    @property
    def page_count(self):
        """
            Функция возвращает номер текущей страницы, начиная с 1.
            
            :rtype: Int
            :return: Номер последней страницы
        """
        page_data = self._get_property('data', None, False)

        if page_data:
            return int(round(len(page_data) / self.page_items_count + 0.5))
        else:
            return 1


    @property
    def page_has_next(self):
        """
            Функция возвращает True если есть следущая страница.
            
            :rtype: Boolean
            :return: True если есть следущая страница
        """
        return self.page_current < self.page_count
    
    
    @property
    def page_has_prev(self):
        """
            Функция возвращает True если есть предыдущая страница.
            
            :rtype: Boolean
            :return: True если есть следущая страница
        """
        return self.page_current > 1


    @property
    def page_array(self):
        array = []
        
        for index in xrange(1, self.page_count+1, 1):
            array.append(index)
            
        return array
