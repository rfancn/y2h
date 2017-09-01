from y2h.parser.base import BaseParser

RADIO_STYLE_CLASSES = {
    'default':   'radio',
    'inline':   'radio-inline',
}

class RadioParser(BaseParser):
    def __init__(self, template, elem_type, elem_value):
        super(RadioParser, self).__init__(template, elem_type, elem_value)
        self.specific_attrs = {
            'help-label': self.parse_help_label,
            'items': self.parse_child_items,
        }

    def pre_parse(self):
        # after pre paresing, self.attr_dict has been built
        super(RadioParser, self).pre_parse()

        # handling 'style' keyword
        KEYWORD_STYLE = 'style'
        radio_style = self.attr_dict.get(KEYWORD_STYLE, 'default')
        radio_class = RADIO_STYLE_CLASSES.get(radio_style, RADIO_STYLE_CLASSES['default'])
        self.add_class(radio_class)
        if KEYWORD_STYLE in self.attr_dict.keys():
            del self.attr_dict[KEYWORD_STYLE]