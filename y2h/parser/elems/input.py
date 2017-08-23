from y2h.parser.base import BaseParser

class InputParser(BaseParser):
    def __init__(self, template, elem_type, elem_value):
        super(InputParser, self).__init__(template, elem_type, elem_value)
        # define specific attr handing func
        self.specific_attrs = {
            'help-label': self.parse_help_label
        }