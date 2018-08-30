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


import Scopuli.Interfaces.MySQL.Schema.Web.Module.Vacancy as Schema
from Scopuli.Interfaces.WEB.Module import WebModule


class WebVacancy(WebModule):
    _instance_name = "Vacancy"
    _template_name = ""
    _routes = {}
    _dependency = []
    
    
    def load(self):
        self._template_name = "/vacancy/module.html"
        self._routes = {
            "{}".format(self._page.url)     : 'render',
            "{}/".format(self._page.url)    : 'render',
            "{}/send".format(self._page.url): 'render_send'
        }
    
    
    # Todo: Сделать обработку формы
    def render_send(self, caller=None):
        return '{ "alert": "success", "message": "Сообщение отправлено, спасибо за Сотрудничество!" }', 200
    
    
    @property
    def vacancys(self):
        query = self._database.query(Schema.WebModuleVacancy)
        query = query.filter(Schema.WebModuleVacancy.cd_web_site == self._site.id)
        query = query.filter(Schema.WebModuleVacancy.cd_web_page == self._page.id)
        query = query.filter(Schema.WebModuleVacancy.is_published == 1)
        query = query.order_by(Schema.WebModuleVacancy.order)
        
        vacancys = []
        for vacancy in query.all():
            vacancys.append({
                'id'          : vacancy.id,
                'title'       : vacancy.title,
                'description' : vacancy.description,
                'requirements': vacancy.requirements.split(";"),
                'expectations': vacancy.expectations.split(";"),
                'reward'      : vacancy.reward
            })
        
        return vacancys
