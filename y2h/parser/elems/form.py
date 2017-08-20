from y2h.parser.base import BaseParser
from y2h.parser.factory import ElemParserFactory

DEFAULT_FORM_LAYOUT = 'horizontal'
FORM_LAYOUTS = {
    'default': None,
    'horizontal': 'form-horizontal',
    'inline': 'form-inline',
}

class FormParser(BaseParser):
    def __init__(self, elem_type, elem_value):
        super(FormParser, self).__init__(elem_type, elem_value)
        self.specific_attrs = {
            'layout': self.parse_form_layout,
            'fieldset' : self.parse_form_fieldset,
        }

    def parse_form_layout(self, spec_attr_name):
        form_layout = self.attr_dict.get(spec_attr_name, DEFAULT_FORM_LAYOUT)
        if form_layout not in FORM_LAYOUTS.keys():
            form_layout = DEFAULT_FORM_LAYOUT

        self.add_class(FORM_LAYOUTS[form_layout])
        self._[spec_attr_name] = form_layout

    def parse_form_fieldset(self, spec_attr_name):
        # get form fieldset
        form_fieldset = []
        if isinstance(self.elem_value, dict):
            fieldset = self.elem_value.get(spec_attr_name, [])
            if fieldset:
                form_fieldset = fieldset

        # fieldset may contains multiple elements
        form_elements = []
        for elem in form_fieldset:
            parser = ElemParserFactory.create(elem)
            if parser:
                # widget may contains multiple children
                # e,g: radio widget may contains multiple item
                form_elements.append(parser.parse())

        self._[spec_attr_name] = form_elements
