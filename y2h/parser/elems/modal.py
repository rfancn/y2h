from y2h.parser.base import BaseParser
from y2h.parser.factory import ElemParserFactory

class ModalParser(BaseParser):
    def __init__(self, template, elem_type, elem_value):
        super(ModalParser, self).__init__(template, elem_type, elem_value)
        self.specific_attrs = {
            'header': self.parse_modal_header,
            'body': self.parse_modal_body,
            'footer': self.parse_modal_footer,
        }

    def parse_modal_header(self, spec_attr_name):
        """ Parse panel header, now only support text in header """
        ATTR_NAME = 'header'
        if spec_attr_name != ATTR_NAME:
            raise ValueError('Invalid spec_attr_name:{0} in parse_modal_header'.format(spec_attr_name))

        panel_header = self.elem_value.get(ATTR_NAME, None)
        # e,g: text="panel1 header"
        if isinstance(panel_header, str):
            #header_dict = self.parse_attr_str(panel_header)
            #header_text = header_dict.get('text', '')
            self._[ATTR_NAME] = panel_header

    def parse_modal_body(self, spec_attr_name):
        """ There may exist multiple items under panel-body"""
        ATTR_NAME = 'body'
        if spec_attr_name != ATTR_NAME:
            raise ValueError('Invalid spec_attr_name:{0} in parse_modal_body'.format(spec_attr_name))

        panel_body = self.elem_value.get(ATTR_NAME, None)
        if isinstance(panel_body, list):
            body_elements = []
            for elem in panel_body:
                parser = ElemParserFactory.create(self.template, elem)
                if parser:
                    # widget may contains multiple children
                    # e,g: radio widget may contains multiple item
                    body_elements.append(parser.parse())

            self._['body'] = body_elements

    def parse_modal_footer(self, spec_attr_name):
        """ Parse panel footer """
        ATTR_NAME = 'footer'
        if spec_attr_name != ATTR_NAME:
            raise ValueError('Invalid spec_attr_name:{0} in parse_modal_footer'.format(spec_attr_name))

        panel_footer = self.elem_value.get(ATTR_NAME, None)
        if isinstance(panel_footer, list):
            footer_elements = []
            for elem in panel_footer:
                parser = ElemParserFactory.create(self.template, elem)
                if parser:
                    # widget may contains multiple children
                    # e,g: radio widget may contains multiple item
                    footer_elements.append(parser.parse())

            self._['footer'] = footer_elements

