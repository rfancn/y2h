from y2h.parser.base import BaseParser

BTN_OPTION_CLASSES = {
    'default':  'btn btn-default',
    'primary':  'btn btn-primary',
    'success':  'btn btn-success',
    'info':      'btn btn-info',
    'warning':  'btn btn-warning',
    'danger':   'btn btn-danger',
    'link':     'btn btn-link',
}

BTN_SIZE_CLASSES = {
    'default':  None,
    'small':    'btn-sm',
    'xsmall':   'btn-xs',
    'large':    'btn-lg',
}

class ButtonParser(BaseParser):
    def __init__(self, template, elem_type, elem_value):
        super(ButtonParser, self).__init__(template, elem_type, elem_value)
        self.specific_attrs = {
            'option': self.parse_button_option,
            'size': self.parse_button_size,
            # no specific parse func, defined here to make sure it will not show in attribute string
            'text': self.pares_button_text,
        }

    def parse_button_option(self, spec_attr_name):
        btn_option = self.attr_dict.get(spec_attr_name, 'default')
        btn_class =  BTN_OPTION_CLASSES[btn_option]
        self.add_class(btn_class)

    def parse_button_size(self, spec_attr_name):
        btn_size = self.attr_dict.get(spec_attr_name, 'default')
        btn_class = BTN_SIZE_CLASSES[btn_size]
        if btn_class:
            self.add_class(btn_class)

    def pares_button_text(self, spec_attr_name):
        btn_text = self.attr_dict.get('text', '')
        self._['text'] = btn_text