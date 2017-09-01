import sys
import collections
from shlex import shlex

def parse_attr_str(attr_str):
    """  parse attr string , it is key-value pairs from a shell-like text and returns a dict
         sometimes, it could have single attribute, like: disabled, requied,
         handle it specially and set None as single attribute's value
    """
    if not attr_str:
        print("Empty att_str in parse_attr_str()")
        return {}

    if sys.version_info[0] == 3:
        string_types = str
    else:
        string_types = basestring

    if not isinstance(attr_str, string_types):
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
            if sys.version_info >= (3, 3):
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

class OrderedSet(collections.MutableSet):
    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)
