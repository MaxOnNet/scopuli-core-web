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
import Scopuli.Interfaces.MySQL.Schema.Web.Module.Club as Schema

from flask import request
from werkzeug.local import LocalProxy


class WebClub(WebModule):
    """
        Класс наследуемый дочерними веб модулями "Клуба", описывает доступ к обьектам.
    """
    _instance_name = "Club"
    _instance_filter = "_4g_club_filter"
    
    _club_id = 0
    _dependency = []

    filter_type = ""
    filter_value = ""
    
    def load(self):
        self.filter_type = LocalProxy(self.get_filter_type)
        self.filter_value = LocalProxy(self.get_filter_value)
        
        self._club_id = int(self._config.get("web", "module-club", "club_id", "0"))


    @staticmethod
    def get_filter_type():
        """
            Получение значения типа текущего фильтра из сессии.
            
            :return: Тип используемого фильтра
            :rtype: String
        """
        __filter_type = getattr(request, '{}_type'.format(WebClub._instance_filter), None)
    
        if __filter_type is not None:
            return __filter_type
        else:
            return ""


    @staticmethod
    def set_filter_type(value):
        """
            Сохраниение значения типа фильтра в сессии.

            :param value: Тип используемого фильтра
            :type value: String
            
            :return: None
        """
        setattr(request, '{}_type'.format(WebClub._instance_filter), value)


    @staticmethod
    def get_filter_value():
        """
            Получение значения текущего фильтра из сессии.

            :return: Значение фильтра
            :rtype: String
        """
        __filter_value = getattr(request, '{}_value'.format(WebClub._instance_filter), None)
    
        if __filter_value is not None:
            return __filter_value
        else:
            return ""


    @staticmethod
    def set_filter_value(value):
        """
            Сохраниение значения фильтра в сессии.

            :param value: Тип используемого фильтра
            :type value: String

            :return: None
        """
        setattr(request, '{}_value'.format(WebClub._instance_filter), value)


    @property
    def club(self):
        """
        
            :return: Экземпляр текущего :ref:`module-web-modules-club`
            :rtype: :ref:`module-web-modules-club`
        """
        query = self._database.query(Schema.Club)
        query = query.filter(Schema.Club.cd_club == self._club_id)
        query = query.filter(Schema.Club.is_enable == 1)
    
        for club in query.all():
            return club
    
        return None


    @property
    def rooms(self):
        return self.get_rooms(self.filter_type, self.filter_value)
    
    @property
    def room(self):
        for room in self.rooms:
            return room
    
        return None
    
    def get_rooms(self, filter_type="", filter_value=""):
        """

            :param filter_type:
            :param filter_value:
            :return: Массив
        """
        
        query = self._database.query(Schema.ClubRoom)
        query = query.filter(Schema.ClubRoom.cd_club == self._club_id)
        query = query.filter(Schema.ClubRoom.is_public == 1)
        query = query.order_by(Schema.ClubRoom.order)
    
        rooms = []
        for room in query.all():
            # Пропускаем если клуб отключен
            if not room.club.is_public or not room.club.is_enable:
                continue
                
            if filter_type == "room":
                if room.web_url == filter_value:
                    rooms.append(room)
        
            if filter_type == "":
                rooms.append(room)
    
        return rooms
    
    @property
    def services(self):
        return self.get_services(self.filter_type, self.filter_value)

    @property
    def service(self):
        for service in self.services:
            return service
    
        return None


    def get_services(self, filter_type="", filter_value=""):
        """

            :param filter_type:
            :param filter_value:
            :return: Массив
        """
        if len(filter_value.split(",")) == 0:
            filter_value = [filter_value]
        else:
            filter_value = filter_value.split(",")
            
        query = self._database.query(Schema.ClubService)
        query = query.filter(Schema.ClubService.cd_club == self._club_id)
        query = query.filter(Schema.ClubService.is_public == 1)
        query = query.filter(Schema.ClubService.is_enable == 1)
        query = query.order_by(Schema.ClubService.order)
    
        services = []
        for service in query.all():
            # Пропускаем если клуб отключен
            if not service.club.is_public or not service.club.is_enable:
                continue
                
            if filter_type == "room":
                for service_room in service.rooms:
                    if service_room.room.web_url in filter_value:
                        services.append(service)

            
            if filter_type == "service":
                if service.web_url in filter_value:
                    services.append(service)
            
            if filter_type == "":
                services.append(service)
    
        return services


    @property
    def coachers(self):
        return self.get_coachers(self.filter_type, self.filter_value)


    @property
    def coacher(self):
        for coacher in self.coachers:
            return coacher
    
        return None


    def get_coachers(self, filter_type="", filter_value=""):
        """
        
            :param filter_type:
            :param filter_value:
            :return: Массив
        """
        query = self._database.query(Schema.ClubCoacher)
        query = query.filter(Schema.ClubCoacher.cd_club == self._club_id)
        # query = query.filter(Schema.Club.is_enable == 1)
        query = query.filter(Schema.ClubCoacher.is_enable == 1)
        query = query.filter(Schema.ClubCoacher.is_public == 1)

        query = query.order_by(Schema.ClubCoacher.web_order)
    
        coachers = []
        for coacher in query.all():
            # Пропускаем если клуб отключен
            if not coacher.club.is_public or not coacher.club.is_enable:
                continue
            
            # Пропускаем если пользователь отключен
            if coacher.user.is_delete or not coacher.user.is_enable:
                continue
                
            if filter_type == "room":
                for coacher_service in coacher.services:
                    for coacher_service_room in coacher_service.rooms:
                        if coacher_service_room.room.web_url == filter_value:
                            coachers.append(coacher)
        
            if filter_type == "service":
                for coacher_service in coacher.services:
                    if coacher_service.service.web_url == filter_value:
                        coachers.append(coacher)
                        
            if filter_type == "coacher":
                if coacher.web_url == filter_value:
                    coachers.append(coacher)
                    
            if filter_type == "":
                coachers.append(coacher)
    
        return coachers


    @property
    def offers(self):
        return self.get_offers(self.filter_type, self.filter_value)


    @property
    def offer(self):
        for offer in self.offers:
            return offer
    
        return None


    def get_offers(self, filter_type="", filter_value=""):
        """

            :param filter_type:
            :param filter_value:
            :return: Массив
        """
    
        query = self._database.query(Schema.ClubOffer)
        query = query.filter(Schema.ClubOffer.cd_club == self._club_id)
        query = query.filter(Schema.ClubOffer.is_deleted == 0)
        query = query.filter(Schema.ClubOffer.is_enable == 1)
        query = query.filter(Schema.ClubOffer.is_public == 1)
        query = query.filter(Schema.ClubOffer.is_private == 0)
        query = query.order_by(Schema.ClubOffer.order)
    
        offers = []
        for offer in query.all():
            # Пропускаем если клуб отключен
            if not offer.club.is_public or not offer.club.is_enable:
                continue
        
            if filter_type == "offer":
                if offer.uuid == filter_value:
                    offers.append(offer)
        
            if filter_type == "":
                offers.append(offer)
    
        return offers


    def render_search(self, search_type, search_value, caller=None):
        self.set_filter_type(search_type)
        self.set_filter_value(search_value)
    
        return WebClub.render(self, caller)

