import re
import sys
from shlex import shlex

class BaseParser(object):
    def __init__(self, elem_type, elem_value):
        self.elem_type = elem_type
        self.elem_value = elem_value

        # internal variable to store parsed element values
        self._ = {}
        self.attr_dict = {}
        self.specific_attrs = {}

    def add_class(self, class_str):
        """
        Add html class to current class string
        e,g: Add 'panel-default' to class="panel" -> class="panel panel-default"
        """
        if not class_str:
            return True

        # get original classes
        original_class_str = self.attr_dict.get('class', '').strip()
        if not original_class_str:
            self.attr_dict['class'] = class_str
            return True

        original_classes = set(original_class_str.split())
        new_classes = original_classes | set(class_str.split())
        self.attr_dict['class'] = ' '.join(new_classes)
        return True

    def remove_class(self, class_str):
        """
        Remove html class from current class string
        """
        if not class_str:
            return True

        # get original classes
        original_class_str = self.attr_dict.get('class', '').strip()
        if not original_class_str:
            return True

        original_classes = set(original_class_str.split())
        new_classes = original_classes - set(class_str.split())
        self.attr_dict['class'] = ' '.join(new_classes)
        return True

    def parse_attr_str(self, attr_str):
        """  parse attr string , it is key-value pairs from a shell-like text and returns a dict
             sometimes, it could have single attribute, like: disabled, requied,
             handle it specially and set None as single attribute's value
        """
        if not attr_str:
            print("Empty att_str in parse_attr_str()")
            return {}

        if not isinstance(attr_str, str):
            print("Invalid attr_str while parsing:{0}".format(attr_str))
            return {}

        # initialize a lexer, in POSIX mode (to properly handle escaping)
        lexer = shlex(attr_str, posix=True)
        # include '=' as a word character
        # (this is done so that the lexer returns a list of key-value pairs)
        # (if your option key or value contains any unquoted special character, you will need to add it here)
        lexer.wordchars += "="
        # make sure attribute support 'data-parsley-length' attribute name
        lexer.wordchars += "-"
        # then we separate option keys and values to build the resulting dictionary
        # (maxsplit is required to make sure that '=' in value will not be a problem)
        # sometimes as HTML will has some key like attribute without value, like: 'required', 'disabled'...
        # it need extract those single attribute from the string
        pairs_attrs = []
        single_attrs = []
        for word in lexer:
            if "=" in word:
                # str.split() changed 'maxsplit' to keyword arguments
                # see: https://docs.python.org/3.3/library/stdtypes.html#str.split
                if sys.version_info >= (3,3):
                    pairs_attrs.append(word.split("=", maxsplit=1))
                else:
                    pairs_attrs.append(word.split("=", 1))
            else:
                single_attrs.append(word)

        # convert pairs attribute list to dict
        pairs_attr_dict = dict(pairs_attrs)
        # add single atrribute to dict
        for attr in single_attrs:
            pairs_attr_dict[attr] = None

        return pairs_attr_dict

    def process_attribute_dict(self, attr_dict, remove_list=[]):
        """
        Process attribute dict:
        1. make sure kvpair attribute shows before single atribute
        2. As singal attribute set to be None while converting attribute string to atrribute dict,
           here reformat it to not contains None, e,g: required=None -> required
        3. remove attributes shown up in remove_list
        """
        # Extract k,v pairs attribute and single attribute list
        # k,v pairs attribute is a format like: name="ryan"
        # single attribute is an item like: required, disabled
        pairs_attr_list = []
        single_attr_list = []
        for k, v in attr_dict.items():
            # extract single attr, like: required, disabled
            if v is None:
                single_attr_list.append(k)
                continue

            # only keep standard attributes or the one we want to have
            if k not in remove_list:
                pairs_attr_list.append('{0}="{1}"'.format(k, v))

        # build input attribute
        if single_attr_list:
            attr_str = " ".join(pairs_attr_list) + " " + " ".join(single_attr_list)
        else:
            attr_str = " ".join(pairs_attr_list)

        return attr_str

    def pre_parse(self):
        """
        Extract and build attribute dict from elem value:
        1. if elem_value is a string, then attribute is elem_value
        2. if elem_value is a dict, then attribute contains in elem_value[elem_type]
        """
        #self.debug_elem_value()

        attr_str = None
        # if element type don't have attribute defined, no ':' after element name,
        # then it is a string object, here we need explicitly set attribute string to be None
        # e,g:
        # elements:
        #   - form
        if isinstance(self.elem_value, str):
            attr_str = None
        elif isinstance(self.elem_value, dict):
            attr_str = self.elem_value.get(self.elem_type, None)
        else:
            raise ValueError("Invalid element definition in pre_parse()!")

        if attr_str:
            self.attr_dict = self.parse_attr_str(attr_str)

    def convert_valid_var_name(self, s):
        """ Convert a string to a valid python variable name"""
        # Remove invalid characters
        s = re.sub('[^0-9a-zA-Z_]', '', s)
        # Remove leading characters until we find a letter or underscore
        s = re.sub('^[^a-zA-Z_]+', '', s)
        return s

    def specific_attrs_parse(self):
        for attr_name, attr_parse_func in self.specific_attrs.items():
            # make sure attr_name is a valid variable name
            valid_attr_name = self.convert_valid_var_name(attr_name)
            # call specific attr parsing func
            attr_parse_func(valid_attr_name)

    def post_parse(self):
        """
        1. processing attribute dict and convert to attribute string
        2. set _['attribute'] to be attribute string
        """
        # Python3.x, dict.keys() is a dict_keys type,
        # Python2.x, dict.keys() is a list
        # To keep python2.x and 3.x compatibility, explicitly call list() for dict.keys()
        specific_attr_names = list(self.specific_attrs.keys())
        new_attr_str = self.process_attribute_dict(self.attr_dict, remove_list=specific_attr_names)
        if new_attr_str:
            self._['attribute'] = new_attr_str

        # self._['template'] = 'input.html'

    def parse(self):
        self.pre_parse()
        self.specific_attrs_parse()
        self.post_parse()

        return {self.elem_type: self._}

    def parse_help_label(self, spec_attr_name):
        """ build help label dict for normal HTML element <label> """
        help_label_dict = {}
        if spec_attr_name in self.attr_dict.keys():
            help_label_dict['innertext'] = self.attr_dict[spec_attr_name]
            identifier = self.attr_dict.get("id") or self.attr_dict.get("name")
            if identifier:
                help_label_dict['for'] = identifier

        self._[spec_attr_name] = help_label_dict

    def parse_child_items(self, spec_attr_name):
        """ Parse child items for radio and checkbox element """
        original_items = []
        if isinstance(self.elem_value, dict):
            items = self.elem_value.get(spec_attr_name, [])
            # in case, no items nor attribute defines for radio element, elem_value is a string
            # this is a rare case but still valid, check it here
            # e,g: - form:
            #          - radio
            if items is not None:
                original_items = items

        paresed_items = []
        for item in original_items:
            #  Only handling item with attribute, which should be dict type
            item_attr_dict = {}
            if isinstance(item, dict):
                item_attr_str = item.get('item', None)
                item_attr_dict = self.parse_attr_str(item_attr_str)

            # Append item attributes that not appears in parent radio attribute
            new_item_attr_dict = self.attr_dict.copy()

            # remove specific attributes
            for k in self.specific_attrs.keys():
                if k in new_item_attr_dict.keys():
                    del new_item_attr_dict[k]

            # combine item attribute with parent element's attribute
            for k,v in item_attr_dict.items():
                if k not in new_item_attr_dict.keys():
                    new_item_attr_dict[k] = v

            # 2. build new elem_attr_dict
            new_item_attr_dict['label'] = new_item_attr_dict.get("label", "")
            new_item_attr_dict['attribute'] = self.process_attribute_dict(new_item_attr_dict, remove_list=['label'])

            # 3. append parsed item_attr_dict to parsed_items list
            paresed_items.append(new_item_attr_dict)

        self._[spec_attr_name] = paresed_items