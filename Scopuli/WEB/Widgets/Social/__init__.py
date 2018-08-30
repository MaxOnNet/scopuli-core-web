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


from Scopuli.Interfaces.WEB.Widget import WebWidget
import Scopuli.Interfaces.MySQL.Schema.Web.Widget.Social as Schema


class WebWidgetSocial(WebWidget):
    
    @property
    def links(self):
        query = self._database.query(Schema.WebWidgetSocial)
        query = query.filter(Schema.WebWidgetSocial.cd_web_site == self._site.id)
        query = query.filter(Schema.WebWidgetSocial.is_enable == 1)
        query = query.order_by(Schema.WebWidgetSocial.order)
        
        links = []
        for link in query.all():
            links.append({
                'id'  : link.id,
                'url' : link.url,
                'code': link.type.code,
                'name': link.name
                
            })
        
        return links
