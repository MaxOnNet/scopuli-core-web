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

from uuid import uuid4

from importlib import import_module
from jinja2 import nodes
from jinja2.ext import Extension

from Scopuli.Interfaces.WEB.Jinja.Tools import parse

import arrow


class MetaInfoExtension(Extension):
    tags = set(['meta'])


    def parse(self, parser):
        token = parser.stream.next()
        lineno = token.lineno

        meta = parser.parse_statements(['name:endmeta'], drop_needle=True)
        try:
            config = meta[0].nodes[0].data
        except IndexError:
            config = '' # there was no data

        args = [nodes.Name('meta', 'load'), nodes.Const(config)]

        output = [
            nodes.CallBlock(self.call_method('_update_page', args=args),
                            [], [], '').set_lineno(lineno)
            ]
        return output


    def _update_page(self, meta, config, caller):
        meta.update(parse(config))

        return ''


class WidgetExtension(Extension):
    """Adds support for a django-like with block."""
    tags = set(['widget'])

    def parse(self, parser):
        parser_token = parser.stream.next()
        parser_lineno = parser_token.lineno
        
        node = nodes.Scope(lineno=parser_lineno)
        assignments = []
        widget_args = []
        
        while parser.stream.current.type != 'block_end':
            lineno = parser.stream.current.lineno
            if assignments:
                parser.stream.expect('comma')

            widget_target = parser.parse_assign_target()
            parser.stream.expect('assign')
            widget_config = parser.parse_expression()
            widget_name = widget_target.name
            widget_target, widget_node = self._widget_uuid(widget_target, widget_config)
            widget_args = [nodes.Name('widgets', 'load'), nodes.Const(widget_name), widget_config, widget_node]
            assignments.append(nodes.Assign(widget_target, widget_node, lineno=lineno))
        node.body = assignments + list(parser.parse_statements(('name:endwidget',),  drop_needle=True))

        output = [
            nodes.CallBlock(self.call_method('_widget_onload', args=widget_args), [], [], '').set_lineno(parser_lineno), node
        ]
        
        return output
    
    def _widget_uuid(self, widget_target, widget_config):
        widget_uuid = str(uuid4())
        widget_target.name = 'widget'
        widget_node = nodes.Const(widget_uuid)

        return widget_target, widget_node


    def _widget_onload(self, widget_array, widget_name, widget_config, widget_uuid, caller):
        widget_module = "WEB.Widgets"
        widget = getattr(import_module(widget_module), widget_name)
        
        if widget:
            widget_class = widget(self.environment, widget_config, widget_uuid=widget_uuid)
            widget_array[widget_uuid] = widget_class
            
        return ''


class TimeExtension(Extension):
    tags = set(['now'])

    def __init__(self, environment):
        super(TimeExtension, self).__init__(environment)

        # add the defaults to the environment
        environment.extend(datetime_format='%Y-%m-%d')

    def _datetime(self, timezone, operator, offset, datetime_format):
        d = arrow.now(timezone)

        # Parse replace kwargs from offset and include operator
        replace_params = {}
        for param in offset.split(','):
            interval, value = param.split('=')
            replace_params[interval.strip()] = float(operator + value.strip())
        d = d.replace(**replace_params)

        if datetime_format is None:
            datetime_format = self.environment.datetime_format
        return d.strftime(datetime_format)

    def _now(self, timezone, datetime_format):
        if datetime_format is None:
            datetime_format = self.environment.datetime_format
            
        if datetime_format == "%unix":
            return arrow.now(timezone).timestamp
        else:
            return arrow.now(timezone).strftime(datetime_format)


    def parse(self, parser):
        lineno = next(parser.stream).lineno

        node = parser.parse_expression()

        if parser.stream.skip_if('comma'):
            datetime_format = parser.parse_expression()
        else:
            datetime_format = nodes.Const(None)

        if isinstance(node, nodes.Add):
            call_method = self.call_method(
                '_datetime',
                [node.left, nodes.Const('+'), node.right, datetime_format],
                lineno=lineno,
            )
        elif isinstance(node, nodes.Sub):
            call_method = self.call_method(
                '_datetime',
                [node.left, nodes.Const('-'), node.right, datetime_format],
                lineno=lineno,
            )
        else:
            call_method = self.call_method(
                '_now',
                [node, datetime_format],
                lineno=lineno,
            )
            
        return nodes.Output([call_method], lineno=lineno)