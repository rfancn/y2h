from y2h.parser.base import BaseParser

CHECKBOX_STYLE_CLASSES = {
    'default':   'checkbox',
    'inline':   'checkbox-inline',
}

class CheckboxParser(BaseParser):
    def __init__(self, template, elem_type, elem_value):
        super(CheckboxParser, self).__init__(template, elem_type, elem_value)
        self.specific_attrs = {
            'help-label': self.parse_help_label,
            'items': self.parse_child_items,
        }

    def pre_parse(self):
        # after pre paresing, self.attr_dict has been built
        super(CheckboxParser, self).pre_parse()

        # handling 'style' keyword
        KEYWORD_STYLE = 'style'
        checkbox_style = self.attr_dict.get(KEYWORD_STYLE, 'default')
        checkbox_class = CHECKBOX_STYLE_CLASSES.get(checkbox_style, CHECKBOX_STYLE_CLASSES['default'])
        self.add_class(checkbox_class)
        if KEYWORD_STYLE in self.attr_dict.keys():
            del self.attr_dict[KEYWORD_STYLE]