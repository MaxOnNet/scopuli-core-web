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


import uuid
import json
from flask import request, session, abort, jsonify
from ..Club import WebClub, Schema


class WebClubSubscribe(WebClub):
    _instance_name = "Club/Subscribe"
    _template_name = "/club/subscribe/module.html"
    _routes = {}

    def load(self):
        WebClub.load(self)
    
        self._routes = {
            "/json{}/<string:name>".format(self._page.url): 'render_json_subscribe',
            "/json{}/<string:name>/unsubscribe".format(self._page.url): 'render_json_unsubscribe'
        }
    
    def get_subscribe(self, name):
        query = self._database.query(Schema.ClubSubscribe)
        query = query.filter(Schema.ClubSubscribe.cd_club == self._club_id)
        query = query.filter(Schema.ClubSubscribe.web_url == name)
        query = query.filter(Schema.ClubSubscribe.is_enable == 1)
    
        for club_subscribe in query.all():
            return club_subscribe
    
    def render_json_subscribe(self, name, caller=None):
        json_dict = {
            "alert": "success", "message": "Вы успешно подали заявку, в ближайщее время с Вами свяжутся."
        }
        
        db_subs = self.get_subscribe(name)

        if db_subs:
            self._database.begin_nested()
    
            try:
                db_subs_data = Schema.ClubSubscribeData()
                db_subs_data.cd_club_subscribe = db_subs.id
    
                db_subs_data.uuid = str(uuid.uuid4())
                db_subs_data.data = str(json.dumps(request.form))
    
                self._database.add(db_subs_data)
                self._database.commit()
            except:
                self._database.rollback()
                raise
            
        else:
            json_dict['alert'] = "error"
            json_dict['message'] = "Подписка не найдена"

        return self.render_json(json_dict)


    def render_json_unsubscribe(self, name, caller=None):
        json_dict = {
            "alert": "success", "message": "Вы успешно отписаны."
        }

        return self.render_json(json_dict)

