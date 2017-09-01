from y2h.parser.base import BaseParser
from y2h.parser.factory import ElemParserFactory

TABLE_STYLE_CLASSES = {
    'default':    'table',
    'striped':    'table table-striped',
    'bordered':   'table table-bordered',
    'hover':       'table table-hover',
    'condensed':  'table table-condensed',
}

class TableParser(BaseParser):
    def __init__(self, template, elem_type, elem_value):
        super(TableParser, self).__init__(template, elem_type, elem_value)
        self.specific_attrs = {
            'thead': self.parse_table_thead,
            'tbody': self.parse_table_tbody,
        }
        # number of columns
        self.col_num = 0

    def pre_parse(self):
        # after pre paresing, self.attr_dict has been built
        super(TableParser, self).pre_parse()

        # handle keyword 'style'
        KEYWORD_STYLE = 'style'
        table_style = self.attr_dict.get(KEYWORD_STYLE, 'default')
        table_class = TABLE_STYLE_CLASSES.get(table_style, TABLE_STYLE_CLASSES['default'])
        self.add_class(table_class)
        if KEYWORD_STYLE in self.attr_dict.keys():
            del self.attr_dict[KEYWORD_STYLE]

    def parse_table_thead(self, spec_attr_name):
        """ Parse panel header, now only support text in header """
        ATTR_NAME = 'thead'
        if spec_attr_name != ATTR_NAME:
            raise ValueError('Invalid spec_attr_name:{0} in parse_table_thead'.format(spec_attr_name))

        if not isinstance(self.elem_value, dict):
            return

        thead_value = self.elem_value.get(ATTR_NAME, None)
        if isinstance(thead_value, list):
            self._[ATTR_NAME] = thead_value
            # save number of columns
            self.col_num = len(thead_value)

    def parse_table_tbody(self, spec_attr_name):
        """ There may exist multiple items under panel-body"""
        ATTR_NAME = 'tbody'
        if spec_attr_name != ATTR_NAME:
            raise ValueError('Invalid spec_attr_name:{0} in parse_table_tbody'.format(spec_attr_name))

        if not isinstance(self.elem_value, dict):
            return

        tbody_value = self.elem_value.get(ATTR_NAME, None)
        if isinstance(tbody_value, list):
            # as we already make sure tbody_value is a list
            for tr in tbody_value:
                if not isinstance(tr, list):
                    raise ValueError('Invalid table row, it should be a list')

                if len(tr) != self.col_num:
                    raise ValueError('Invalid table row, it should equals to number of columns:{0}'.format(self.col_num))

            self._[ATTR_NAME] = tbody_value
