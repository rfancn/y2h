import os

from y2h.parser.base import BaseParser
from y2h.parser.factory import ElemParserFactory

DEFAULT_TEMPLATE = 'bootstrap3'

class HtmlMeta(object):
    def __init__(self, jsonret):
        self.jsonret = jsonret
        self.elements = self.parse_elements()
        self.template_dir = self.get_template_dir()

    def parse_elements(self):
        parsed_elements = []

        elem_list = self.jsonret.get('elements', [])
        for elem in elem_list:
            elem_parser = ElemParserFactory.create(elem)
            if elem_parser:
                elem_dict = elem_parser.parse()
                parsed_elements.append(elem_dict)

        return parsed_elements

    def get_template_dir(self):
        # get template and template_dir
        template = self.jsonret.get('template', DEFAULT_TEMPLATE)
        template_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "templates",
            template
        )

        return template_dir





