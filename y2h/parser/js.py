from y2h.parser.utils import parse_attr_str

EXTERNAL_JS = '<script src={url}></script>'

BOOTCSS_URL_FORMART = 'https://cdn.bootcss.com/{category}/{ver}/{file}'
CLOUDFLARE_URL_FORMAT = 'https://cdnjs.cloudflare.com/ajax/libs/{category}/{ver}/{file}'

LOCALE_CDN = {
    'cn': BOOTCSS_URL_FORMART,
    'en': CLOUDFLARE_URL_FORMAT,
}

DEFAULT_LOCALE = "cn"

class JavascriptHelper(object):
    def __init__(self, jsonret):
        self.jsonret = jsonret
        self.js_content_list = self.parse()

    def parse(self):
        js_list = self.jsonret.get('javascript', [])
        if not isinstance(js_list, list):
            raise ValueError('Invalid javascript: it should be a list')

        js_content_list = []
        for js_value in js_list:
            if not isinstance(js_value, dict):
                raise ValueError('Invalid javascript part: script must be a dict')

            for k,v in js_value.items():
                js_content = self.get_js_content(k, v)
                if js_content:
                    js_content_list.append(js_content)

        return js_content_list

    def get_js_content(self, js_key, js_value):
        content = None
        if js_key == 'cdn':
            js_dict = self.get_js_value_dict(js_value, requires=['category', 'ver', 'file'])
            content = self.get_cdn_content(js_dict)
        elif js_key == 'external':
            js_dict = self.get_js_value_dict(js_value, requires=['src'])
            content = self.get_external_content(js_dict)
        elif js_key == 'inline':
            if not isinstance(js_value, str):
                raise ValueError('Invalid javascript inline: it should be string')

            content = ('inline', js_value)

        return content

    def get_js_value_dict(self, js_value, requires=[]):
        # Firstly, we assume js_value is a dict type
        # If it is a string, then try to convert js_value string to js_dict dict type
        # e,g: category="select" ver=1.9 file="datatable.min.js"
        # {'category':'select', 'ver':1.9, 'file':'datatable.min.js'}
        js_dict = js_value
        if isinstance(js_value, str):
            js_dict = parse_attr_str(js_value)

        if not isinstance(js_dict, dict):
            raise ValueError('Invalid javascript line.')

        required_keys = set(requires)
        current_keys = set(list(js_dict.keys()))
        if not required_keys.issubset(current_keys):
            raise ValueError('Invalid javascript line: requies {0}'.format(requires))

        return js_dict

    def get_cdn_content(self, js_dict):
        """ Return type is a dict, key is js content type, value is real content"""
        js_locale = js_dict.get('locale', DEFAULT_LOCALE)
        js_cdn_template = LOCALE_CDN.get(js_locale, LOCALE_CDN[DEFAULT_LOCALE])
        js_url = js_cdn_template.format(category=js_dict['category'], ver=js_dict['ver'], file=js_dict['file'])
        return ('external', EXTERNAL_JS.format(url=js_url))

    def get_external_content(self, js_dict):
        return ('external', EXTERNAL_JS.format(url=js_dict['src']))
