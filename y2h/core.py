#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2016 Ryan Fan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""
import yaml
from jinja2 import Environment, FileSystemLoader

from y2h.parser.html import HtmlHelper
from y2h.parser.js import JavascriptHelper

class Yaml2Html(object):
    def __init__(self):
        # YAML converts to json result and stores here after load()
        self.jsonret = None
        self.html_elements = []

    def read(self, yaml_file):
        """ load yaml definition file and return html list """
        try:
            with open(yaml_file, 'r') as f:
                self.jsonret = yaml.load(f)
        except Exception as ex:
            print(ex)
            return False

        return True

    def get_html(self):
        html_helper = HtmlHelper(self.jsonret)

        env = Environment(
            autoescape=False,
            loader=FileSystemLoader(html_helper.template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        htmls = []
        for elem in html_helper.elements:
            for elem_name, elem_value in elem.items():
                template = '{0}.html'.format(elem_name)
                s = env.get_template(template).render(elem)
                htmls.append(s)

        return ''.join(htmls)

    def get_javascript(self):
        js_helper = JavascriptHelper(self.jsonret)
        return js_helper.js_content_list

    def convert(self):
        html = self.get_html()
        css = self.jsonret.get('css', None)
        js = self.get_javascript()

        return (html, css, js)
