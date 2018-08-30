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
import Scopuli.Interfaces.MySQL.Schema.Web.Module.Blog as Schema
import Scopuli.Interfaces.WEB.Utils.Pager as UPages

from datetime import datetime
from flask import request
from sqlalchemy import desc
from werkzeug.local import LocalProxy


class WebBlog(WebModule, UPages.Pager):
    """
        Класс наследуемый дочерними веб модулями "Клуба", описывает доступ к обьектам.
    """
    _instance_name = "Blog"
    _instance_filter = "_4g_blog_filter"
    _instance_config = "module-blog"

    _dependency = []
    
    filter_type = ""
    filter_value = ""

    def load(self):
        self.load_pager(self)
        
        self.filter_type = LocalProxy(self.get_filter_type)
        self.filter_value = LocalProxy(self.get_filter_value)


    @staticmethod
    def get_filter_type():
        __filter_type = getattr(request, '{}_type'.format(WebBlog._instance_filter), None)
    
        if __filter_type is not None:
            return __filter_type
        else:
            return ""


    @staticmethod
    def set_filter_type(value):
        setattr(request, '{}_type'.format(WebBlog._instance_filter), value)


    @staticmethod
    def get_filter_value():
        __filter_value = getattr(request, '{}_value'.format(WebBlog._instance_filter), None)
    
        if __filter_value is not None:
            return __filter_value
        else:
            return ""


    @staticmethod
    def set_filter_value(value):
        setattr(request, '{}_value'.format(WebBlog._instance_filter), value)


    @property
    def posts(self):
        return self.get_posts(self.filter_type, self.filter_value)


    @property
    def post(self):
        for post in self.posts:
            return post
    
        return None


    def get_posts(self, filter_type="", filter_value=""):
        query = self._database.query(Schema.WebModuleBlogPost)
        query = query.filter(Schema.WebModuleBlogPost.cd_web_site == self._site.id)
        query = query.filter(Schema.WebModuleBlogPost.is_published == True)
        query = query.filter(Schema.WebModuleBlogPost.is_deleted == False)
        query = query.filter(Schema.WebModuleBlogPost.date_published <= datetime.now())
        query = query.order_by(desc(Schema.WebModuleBlogPost.date_published))
    
        posts = []
        for post in query.all():
            if filter_type == "tag":
                for post_tag in post.tags:
                    if post_tag.tag.url == filter_value:
                        posts.append(post)
                        
            if filter_type == "url":
                if post.url == filter_value:
                    posts.append(post)
                    
            if filter_type == "":
                posts.append(post)
    
        return posts
    
    @property
    def tags(self):
        return self.get_tags(self.filter_type, self.filter_value)


    @property
    def tag(self):
        for tag in self.tags:
            return tag
    
        return None


    def get_tags(self, filter_type="", filter_value=""):
        query = self._database.query(Schema.WebModuleBlogTag)
        query = query.filter(Schema.WebModuleBlogTag.cd_web_site == self._site.id)
        query = query.filter(Schema.WebModuleBlogPost.is_published == True)
        query = query.filter(Schema.WebModuleBlogPost.is_deleted == False)
        query = query.order_by(Schema.WebModuleBlogTag.order)
    

        tags = []
        for tag in query.all():
            tags.append(tag)
        
        return tags
