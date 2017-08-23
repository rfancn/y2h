import os

from y2h.parser.base import BaseParser
from y2h.parser.factory import ElemParserFactory

DEFAULT_TEMPLATE = 'bootstrap3'

class HtmlMeta(object):
    def __init__(self, jsonret):
        self.jsonret = jsonret

        self.template = self.jsonret.get('template', DEFAULT_TEMPLATE)
        self.template_dir = self.get_template_dir()

        self.elements = self.parse_elements()

    def parse_elements(self):
        parsed_elements = []

        elem_list = self.jsonret.get('elements', [])
        for elem in elem_list:
            elem_parser = ElemParserFactory.create(self.template, elem)
            if elem_parser:
                elem_dict = elem_parser.parse()
                parsed_elements.append(elem_dict)

        return parsed_elements

    def get_template_dir(self):
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "templates",
            self.template
        )





