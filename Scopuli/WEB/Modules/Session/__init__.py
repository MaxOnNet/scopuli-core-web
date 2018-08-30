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


import Scopuli.Interfaces.MySQL.Schema.Web.Module.Session as Schema
import Scopuli.Interfaces.MySQL.Schema.Core.User as SchemaUser
from Scopuli.Interfaces.WEB.Module import WebModule

from datetime import datetime
from flask import request, session, abort


class WebSession(WebModule):
    """
        Модуль ведения сессии, отвечает за сохранение статистики и параметров пользователя.
    """
    _instance_name = "Session"
    _instance_config = "module-session"
    _template_name = ""
    _routes = {}
    _dependency = []
    
    
    def register(self):
        """
            Регистрация модуля в приложении, подключение обработчиков событий.

            :return: None
        """
        self._application.module_register(self._instance_name, self)
        
        self._application.secret_key = self._config.get("web", self._instance_config, "key", "")
        
        self._application.before_request(self._request_init)
        self._application.teardown_request(self._request_teardown)
    
    
    def _request_init(self):
        """
            Функция вызывается при получении запроса к серверу.

            :return: None
        """
        if request:
            if request.endpoint != "static":
                self._database_init()
                self._database_update()
    
    
    def _request_teardown(self, exception):
        """
            Функция вызывается при завершении обработки запроса.

            :param exception: ХЗ
            :return: None
        """
        if request:
            if request.endpoint != "static":
                pass
    
    
    def _database_init(self):
        """
            Функция инициализации подключения к базе данных при инициализации обработки запроса, с сохранением инстанса в переменной запроса.

            :returтранс n: None
        """
        if '_4g_session_id' not in session:
            self._database_create()
        
        self._application.module_request_save(self._instance_name,
                                              self._database.query(Schema.WebModuleSession).get(session['_4g_session_id']))
        
        if not self._application.module_request(self._instance_name, check_only=True):
            self._database_create()
            self._database_init()
    
    
    def _database_create(self):
        self._database.begin_nested()
        
        try:
            db_session = Schema.WebModuleSession()
            db_session.cd_web_site = self._site.id
            
            self._database.add(db_session)
            self._database.commit()
            
            session['_4g_session_id'] = db_session.id
        except Exception as exp:
            self._database.rollback()
            raise exp
    
    
    def _database_update(self):
        self._database.begin_nested()
        
        try:
            if self._application.module_exist(self._instance_name):
                mod_session = self._application.module_request(self._instance_name)
                
                mod_session.date_active = datetime.utcnow()
                mod_session.request_url = request.path
                
                # Nginx Proxy support
                if 'X-Real-IP' in request.headers:
                    mod_session.user_ip = request.headers['X-Real-IP']
                else:
                    mod_session.user_ip = request.remote_addr
                
                mod_session.user_agent = request.user_agent.string
            
            # Сохраняем изменения
            self._database.commit()
        except Exception as exp:
            self._database.rollback()
            raise exp
    
    
    def callback_render(self, template, web_page, web_module):
        self._database.begin_nested()
        
        if self._application.module_exist(self._instance_name):
            mod_session = self._application.module_request(self._instance_name)
            mod_club = self._application.module_search("Club/", load_first=True)
            
            try:
                if hasattr(mod_club, "_club_id"):
                    mod_session.cd_club = getattr(mod_club, "_club_id")
                
                if web_page:
                    mod_session.cd_web_page = web_page.id
                else:
                    mod_session.cd_web_page = None
                
                # Сохраняем изменения
                self._database.commit()
            except Exception as exp:
                self._database.rollback()
                raise exp
    
    
    @property
    def is_authenticated(self):
        if self._application.module_exist(self._instance_name):
            mod_session = self._application.module_request(self._instance_name)
            
            if mod_session.cd_user:
                return True
        
        return False
    
    
    @property
    def user(self):
        if self._application.module_exist(self._instance_name):
            mod_session = self._application.module_request(self._instance_name)
            
            if mod_session.cd_user:
                return self._database.query(SchemaUser.User).get(int(mod_session.cd_user))
        
        return None
