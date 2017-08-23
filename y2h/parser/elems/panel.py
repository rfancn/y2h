from y2h.parser.base import BaseParser
from y2h.parser.factory import ElemParserFactory

PANEL_TYPE_CLASSES = {
    'default':   'panel panel-default',
    'primary':   'panel panel-primary',
    'success':   'panel panel-success',
    'info':      'panel panel-info',
    'warning':   'panel panel-warning',
    'danger':    'panel panel-danger',
}

class PanelParser(BaseParser):
    def __init__(self, template, elem_type, elem_value):
        super(PanelParser, self).__init__(template, elem_type, elem_value)
        self.specific_attrs = {
            'header': self.parse_panel_header,
            'body': self.parse_panel_body,
            'footer': self.parse_panel_footer,
        }

    def pre_parse(self):
        # after pre paresing, self.attr_dict has been built
        super(PanelParser, self).pre_parse()

        panel_type = self.attr_dict.get('type', 'default')
        panel_class = PANEL_TYPE_CLASSES[panel_type]
        self.add_class(panel_class)
        if 'type' in self.attr_dict.keys():
            del self.attr_dict['type']

    def parse_panel_header(self, spec_attr_name):
        """ Parse panel header, now only support text in header """
        ATTR_NAME = 'header'
        if spec_attr_name != ATTR_NAME:
            raise ValueError('Invalid spec_attr_name:{0} in parse_panel_header'.format(spec_attr_name))

        panel_header = self.elem_value.get(ATTR_NAME, None)
        # e,g: text="panel1 header"
        if isinstance(panel_header, str):
            header_dict = self.parse_attr_str(panel_header)
            header_text = header_dict.get('text', '')
            self._[ATTR_NAME] = header_text

    def parse_panel_body(self, spec_attr_name):
        """ There may exist multiple items under panel-body"""
        ATTR_NAME = 'body'
        if spec_attr_name != ATTR_NAME:
            raise ValueError('Invalid spec_attr_name:{0} in parse_panel_footer'.format(spec_attr_name))

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

    def parse_panel_footer(self, spec_attr_name):
        """ Parse panel footer """
        ATTR_NAME = 'footer'
        if spec_attr_name != ATTR_NAME:
            raise ValueError('Invalid spec_attr_name:{0} in parse_panel_footer'.format(spec_attr_name))

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
