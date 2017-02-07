import re
from scrapy.utils.markup import replace_tags

class Sanitizer(object):

    exclusions = ['\t', '\xa0', '"']
    replacements = ['\r\n']

    @classmethod
    def trim(cls, data):
        try:
            for exc in cls.exclusions:
                data = re.sub(exc, '', data, flags=re.UNICODE)
            for exc in cls.replacements:
                data = re.sub(exc, ' ', data, flags=re.UNICODE)
            data = replace_tags(data.strip())
        except:
            pass
        return data or 'N/A'

    @classmethod
    def extract_date(cls, data):
        posted = data.find("Posted:") + len("Posted:")
        posted_subj = data.find("Post subject:")
        return data[posted:posted_subj].strip()

    @classmethod
    def extract_content(cls, data):
        body = data.split('_____')
        return body[0]
