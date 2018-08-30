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
from Scopuli.Interfaces.MySQL.Schema.Core.Login import Login as dbLogin

from flask import request, session, abort, redirect
from werkzeug.local import LocalProxy


class WebAccount(WebModule):
    _instance_name = "Account"
    _template_name = ""
    _routes = {}
    _dependency = ['Session']
    
    _mode = "login"  # login | logout | account | restore
    
    
    @property
    def robots_disallow(self):
        return [self._page.url]
    
    
    def load(self):
        self._template_name = "/account/module.html"
        self._routes = {
            "{}".format(self._page.url)         : 'render_account',
            "{}/settings".format(self._page.url): 'render_settings',
            "{}/login".format(self._page.url)   : 'render_login',
            "{}/logout".format(self._page.url)  : 'render_logout',
            "{}/restore".format(self._page.url) : 'render_restore'
        }
    
    
    def render_account(self, caller=None):
        if request._4g_session:
            if request._4g_session.cd_user is None:
                self._mode = "login"
            else:
                self._mode = "account"
        else:
            abort(1001)
        
        return self.render()
    
    
    def render_settings(self, caller=None):
        if request._4g_session:
            if request._4g_session.cd_user is None:
                self._mode = "login"
            else:
                self._mode = "settings"
        else:
            abort(1001)
        
        return self.render()
    
    
    def render_login(self, caller=None):
        if request._4g_session:
            if request._4g_session.cd_user is None:
                if str(request.method).lower() == "post":
                    frm_login = self._form.get('login-form-username', 'email', True, "")
                    frm_password = self._form.get('login-form-password', 'string', True, "")
                    frm_remember_me = self._form.get('login-form-remember-me', 'boolean', False, False)
                    
                    if self.login(login=frm_login, password=frm_password, remember_me=frm_remember_me):
                        login_page_url = "{}/login".format(self._page.url)
                        
                        if str(request.referrer)[-(len(login_page_url)):] != login_page_url:
                            return redirect(request.referrer)
                        else:
                            return redirect(self._page.url)
                    else:
                        return redirect("{}/login".format(self._page.url))
                else:
                    self._mode = "login"
            else:
                self._mode = "account"
        else:
            abort(1001)
        
        return self.render()
    
    
    def render_logout(self, caller=None):
        if request._4g_session:
            if request._4g_session.cd_user is not None:
                self.logout()
            else:
                pass
            
            return redirect("/")
        else:
            abort(1001)
        
        return self.render()
    
    
    def render_restore(self, caller=None):
        if request._4g_session:
            if request._4g_session.cd_user is None:
                if request.method == 'GET':
                    self._mode = "restore"
            else:
                self._mode = "account"
        else:
            abort(1001)
        
        return self.render()
    
    
    @property
    def render_mode(self):
        """

        :return:
        """
        return self._mode
    
    
    def login(self, login, password, remember_me=True):
        """
            Функция авторизации пользователя и внесения всех изменений в сессию.

            :param login: Логин пользователя, или EMail, или телефон
            :type login: String
            :param password:
            :type password: String
            :param remember_me: Запоминать ли пользователя более чем на 10 мин.
            :type remember_me: Boolean
            :return: True авторизация прошла, иначе False
            :rtype: Boolean
        """
        query_user = self._database.query(dbLogin)
        # query_user = query_user.filter(Schema.Login.)
        
        self._database.begin_nested()
        
        try:
            request._4g_session.cd_user = 1
            
            self._database.commit()
        except:
            self._database.rollback()
        
        return True
    
    
    def logout(self):
        """
            Функция выхода пользователя, очищаем сессию.

            :return: None
        """
        self._database.begin_nested()
        
        try:
            request._4g_session.cd_user = None
            
            self._database.commit()
        except:
            self._database.rollback()
    
    
    def restore(self):
        pass