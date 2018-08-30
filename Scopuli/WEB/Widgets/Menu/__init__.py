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
from sqlalchemy import null


from Scopuli.Interfaces.WEB.Widget import WebWidget
import Interfaces.MySQL.Schema.Web.Widget.Menu as Schema


class WebWidgetMenu(WebWidget):
    
    def _make_links_array(self, cd_parent):
        query = self._database.query(Schema.WebWidgetMenu)
        query = query.filter(Schema.WebWidgetMenu.is_enable == 1)
        query = query.filter(Schema.WebWidgetMenu.type == self._widget_config['type'])
        query = query.filter(Schema.WebWidgetMenu.cd_web_site == self._site.id)
        query = query.filter(Schema.WebWidgetMenu.cd_parent == cd_parent)
        query = query.order_by(Schema.WebWidgetMenu.order)
        
        links = []
        
        for db_link in query.all():
            if db_link.page.is_enable:
                links_child = self._make_links_array(db_link.id)
                links.append({
                    'id'                   : db_link.id,
                    'child'                : links_child,
                    'target'               : db_link.target,
                    'css_class_lg'         : db_link.css_class_lg,
                    'css_class_md'         : db_link.css_class_md,
                    'css_class_sm'         : db_link.css_class_sm,
                    'css_class_xs'         : db_link.css_class_xs,
                    'css_class_xxs'        : db_link.css_class_xxs,
                    'order'                : db_link.order,
                    
                    'title'                : db_link.page.title,
                    'description'          : db_link.page.description,
                    
                    'url'                  : db_link.page.url,
                    'url_title'            : db_link.page.url_title,
                    'url_title_short'      : db_link.page.url_title_short,
                    'url_description'      : db_link.page.url_description,
                    'url_description_short': db_link.page.url_description_short,
                    
                    'is_active'            : request.path == db_link.page.url,
                    'has_child'            : len(links_child) > 0
                })
        
        return links
    
    
    @property
    def links(self):
        return self._make_links_array(null())
