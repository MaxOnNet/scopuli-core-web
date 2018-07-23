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

from flask import request
from flask import g as context
from flask import abort

import Interfaces.MySQL as MySQL


class WebForm:
    def __init__(self, application):
        self._application = application
        self._config = self._application.config_xml
    
    def _validate_integer(self, value):
        return True
    
    def _validate_string(self, value):
        return True
    
    def _validate_boolean(self, value):
        return True
    
    def _validate_email(self, value):
        return True
    
    def get(self, attribute_name, attribute_type="integer", requred=True, default=""):
        if str(request.method).lower() == "post":
            if attribute_name in request.form:
                attribute_value = request.form[attribute_name]
                fn_validate_name = "_validate_{}".format(attribute_type)
                
                if hasattr(self, fn_validate_name):
                    fn_validate = getattr(self, fn_validate_name)
                    
                    if fn_validate(attribute_value):
                        return attribute_value

        if not requred:
            return default
        else:
            abort(400)
