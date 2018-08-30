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

from flask import current_app
from Scopuli.WEB.DebugToolbar.Panels import DebugPanel

_ = lambda x: x


class ConfigurateDebugPanel(DebugPanel):
    """
    A panel to display all variables from Flask configuration
    """
    name = 'ConfigVars'
    has_content = True

    def nav_title(self):
        return _('Config')

    def title(self):
        return _('Config')

    def url(self):
        return ''

    def content(self):
        context = self.context.copy()
        context.update({
            'config': current_app.config,
        })

        return self.render('panels/config_vars.html', context)
