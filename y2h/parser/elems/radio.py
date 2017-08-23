from y2h.parser.base import BaseParser

class RadioParser(BaseParser):
    def __init__(self, template, elem_type, elem_value):
        super(RadioParser, self).__init__(template, elem_type, elem_value)
        self.specific_attrs = {
            'help-label': self.parse_help_label,
            'items': self.parse_child_items,
        }