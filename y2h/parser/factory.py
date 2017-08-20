from importlib import import_module

SUPPORTED_ELEMENT_TYPES =('form', 'input', 'radio', 'checkbox')

class ElemParserFactory(object):
    @classmethod
    def load_parser(cls, elem_type):
        """
        Given a element type returns the corresponding parser instance.
        All errors raised by the import process (ImportError, AttributeError) are allowed to propagate.
        """
        module_path = 'y2h.parser.elems.{0}'.format(elem_type.lower())
        try:
            module = import_module(module_path)
        except Exception as e:
            raise

        parser_class_name = '{0}Parser'.format(elem_type.title())
        return getattr(module, parser_class_name, None)

    @classmethod
    def guess_elem_type(cls, elem_value):
        """
        Try to identify element's type, e,g: form, input, radio...
        elem can be a string or dict

        # e,g:
        # html:
        #  - form
        #  - form:
        #       fieldset:
        # the first form is a string type, the second form is a dict type
        """
        elem_type = None
        if isinstance(elem_value, str):
            # e,g: elem is 'form'
            elem_type = elem_value
        elif isinstance(elem_value, dict):
            for guess_type in SUPPORTED_ELEMENT_TYPES:
                if guess_type in elem_value.keys():
                    elem_type = guess_type
                    break
        else:
            raise ValueError("Invalid element while creating element parser")

        return elem_type

    @classmethod
    def create(cls, elem_value):
        elem_type = cls.guess_elem_type(elem_value)
        if not elem_type:
            return None

        parser_class = cls.load_parser(elem_type)
        if not parser_class:
            return None

        return parser_class(elem_type, elem_value)
