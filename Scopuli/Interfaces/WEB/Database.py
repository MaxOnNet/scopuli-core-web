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

import logging
import time

from flask import request
from flask import g as context
from flask import abort

from Scopuli.Interfaces.MySQL.SQLAlchemy.Utils import init, init_fast


log = logging.getLogger(__name__)


class WebDatabase:

    _instance_name = "Database"
    _instance_sid = "_4g_database"

    def __init__(self, application):
        self._application = application
        self._config = self._application.config_xml

        self._register()
        self._context_init()
        
    def _register(self):
        log.info("{}: Register Signals.".format(self._instance_name))
        
        self._application.before_request(self._request_init)
        
        self._application.teardown_request(self._request_teardown)
        self._application.teardown_appcontext(self._context_teardown)

    def _request_init(self):
        if request:
            if request.endpoint != "static":
                database = getattr(request, WebDatabase._instance_sid, None)
            
                if database is None:
                    log.info("{}: Request Inicialise.".format(self._instance_name))

                    request._4g_database = init_fast(self._config)()
    
    def _context_init(self):
        database = getattr(self, WebDatabase._instance_sid, None)
    
        if database is None:
            log.info("{}: Context Inicialise.".format(self._instance_name))
            
            if bool(int(self._config.get("database", "", "use_inicialise", "0"))):
                log.debug("{}: Context Inicialise: Use full mode.".format(self._instance_name))
                
                self._4g_database = init(self._config)()
            else:
                log.debug("{}: Context Inicialise: Use fast mode.".format(self._instance_name))
                
                self._4g_database = init_fast(self._config)()
            
            
    def request_get(self):
        database = getattr(request, WebDatabase._instance_sid, None)
    
        if database is None:
            abort(501)
        
        return database
 
     
    def context_get(self):
        database = getattr(self, WebDatabase._instance_sid, None)
    
        if database is None:
            abort(501)
    
        return database

   
    def _context_teardown(self, exception):
        database = getattr(self, WebDatabase._instance_sid, None)

        if database is not None:
            try:
                log.info("{}: Context Teardown.".format(self._instance_name))
                database.rollback()
            except:
                log.error("{}: Context Teardown Error.".format(self._instance_name))
            finally:
                database.close()
                
                setattr(self, WebDatabase._instance_sid, None)

    @staticmethod
    def _request_teardown(exception):
        if request:
            if request.endpoint != "static":
                database = getattr(request, WebDatabase._instance_sid, None)
                
                if database is not None:
                    try:
                        log.info("{}: Request Teardown start.".format(WebDatabase._instance_name))
                        teardown_start = time.time()
                        database.commit()
                        log.info("{}: Request Teardown complate at {} sec.".format(WebDatabase._instance_name, round(time.time() - teardown_start, 4)))
                    except Exception as e:
                        log.error("{}: Request Teardown Error.".format(WebDatabase._instance_name))
                        log.error("{}: {}".format(WebDatabase._instance_name, str(e)))
                    finally:
                        database.close()

                        setattr(request, WebDatabase._instance_sid, None)

