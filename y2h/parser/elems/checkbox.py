from y2h.parser.base import BaseParser

class CheckboxParser(BaseParser):
    def __init__(self, elem_type, elem_value):
        super(CheckboxParser, self).__init__(elem_type, elem_value)
        self.specific_attrs = {
            'help-label': self.parse_help_label,
            'items': self.parse_child_items,
        }