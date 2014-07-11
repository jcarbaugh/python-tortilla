import datetime
import re


def parse_timestamp(ts):
    # Wed Jun 25 2014 14:43:35 GMT-0400 (EDT)
    return datetime.datetime.strptime(ts, '%a %b %d %Y %H:%M:%S GMT-0400 (%Z)')

def meta_fix(content):
    content = re.sub(r'<meta .*?>', '', content)
    return content
