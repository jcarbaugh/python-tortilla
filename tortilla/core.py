import json
import requests
from requests.exceptions import Timeout
from .util import meta_fix

class SalsaObject(object):

    def __init__(self, initial=None):
        _data = {}
        if initial:
            _data.update(initial)
        self.__dict__['_data'] = _data

    def __getattr__(self, attr):
        if attr in self._data:
            return self._data[attr]

    def __setattr__(self, attr, value):
        if attr in self._data:
            self._data[attr] = value
        else:
            self.__dict__[attr] = value

    def whoami(self):
        return self.__class__.__name__

    @classmethod
    def from_list(clazz, objects):
        instances = []
        for obj in objects:
            instances.append(clazz(obj))
        return instances

    @property
    def key(self):
        key_field = "%s_KEY" % self.object
        return self._data.get(key_field)

    def link(self, to_object, with_key):
        pass

    def tag(self, tag):
        pass

    def save(self):
        salsa.save(self.object, self._data, key=self.key)

    def delete(self):
        pass

class Donation(SalsaObject):
    object = 'donation'

class Event(SalsaObject):
    object = 'event'

class Group(SalsaObject):
    object = 'groups'

    def __repr__(self):
        return u"<Group: %s %s>" % (self.key, self.Group_Name)

class Supporter(SalsaObject):
    object = 'supporter'

    def __repr__(self):
        return u"<Supporter: %s %s %s %s>" % (self.key, self.First_Name, self.Last_Name, self.Email)

class SupporterAction(SalsaObject):
    object = 'supporter_action'

class SupporterAddress(SalsaObject):
    object = 'supporter_address'

class SupporterEvent(SalsaObject):
    object = 'supporter_event'

class SupporterGroup(SalsaObject):
    object = 'supporter_groups'

class SignupPage(SalsaObject):
    object = 'signup_page'

class EmailBlast(SalsaObject):
    object = 'email_blast'

# other objects: distributed_event, supporter_action_comment,
# supporter_action_target, supporter_action_content, chapter


def check_authentication(f):
    def wrapper(client, *args, **kwargs):
        if not client.authenticated:
            if client.auth_email and client.auth_password:
                client.authenticate(client.hq, client.auth_email, client.auth_password)
        return f(client, *args, **kwargs)
    return wrapper


class AuthenticationError(Exception):
    pass


class Client(object):

    def __init__(self):
        self.hq = None
        self.auth_email = None
        self.auth_password = None
        self.authenticated = False

        self.timeout = None

        self.http = requests.Session()
        self.http.headers.update({'User-Agent': 'python-tortilla'})
        self.http.params = {'json': 'true'}

    def build_url(self, path, secure=True):
        scheme = 'https' if secure else 'http'
        return "%s://%s.salsalabs.com/%s" % (scheme, self.hq, path)

    @check_authentication
    def get(self, url, params=None, raw=False):

        try:

            resp = self.http.get(url, params=params, timeout=self.timeout)
            content = resp.content

            if params and params.get('object') == 'email_blast':
                content = meta_fix(content)

            if raw:
                return content

            return json.loads(content)

        except Timeout:
            pass

    @check_authentication
    def post(self, url, params=None, raw=False):

        try:

            resp = self.http.post(url, params=params, timeout=self.timeout)

            if raw:
                return resp.content

            return json.loads(resp.content)

        except Timeout:
            pass

    def authenticate(self, hq, email, password, org_key=None, chapter_key=None):

        self.hq = hq
        self.auth_email = email
        self.auth_password = password

        url = self.build_url('api/authenticate.sjs')

        params = {
            'email': email,
            'password': password,
        }

        if org_key:
            params['organization_KEY'] = org_key
        if chapter_key:
            params['chapter_KEY'] = chapter_key

        try:

            resp = self.http.get(url, params=params)
            data = resp.json()

            if 'status' in data and data['status'] == 'success':
                self.authenticated = True
                return True

            raise AuthenticationError(data.get('message', 'Unable to authenticate'))

        except Timeout:
            pass

    def describe(self, object):
        url = self.build_url('api/describe2.sjs')
        params = {'object': object}
        return self.get(url, params=params)

    def object(self, object, key, fields=None):

        url = self.build_url('api/getObject.sjs')

        params = {
            'object': object,
            'key': key,
        }

        if fields:
            params['include'] = fields

        return self.get(url, params=params)

    def objects(self, object, condition=None, order_by=None, limit=None, fields=None):

        url = self.build_url('api/getObjects.sjs')

        params = {'object': object}

        if condition:
            params['condition'] = condition
        if order_by:
            params['orderBy'] = order_by
        if limit:
            params['limit'] = limit
        if fields:
            params['include'] = fields

        return self.get(url, params=params)

    def join(self, object_left, key_left, object_right, key_right=None, object_center=None, **kwargs):

        url = self.build_url('api/getLeftJoin.sjs')

        object = "%s(%s)" % (object_left, key_left)
        if key_right and object_center:
            object = "%s%s(%s)" % (object, object_center, key_right)
        object = "%s%s" % (object, object_right)

        return self.objects(object, **kwargs)

    def tagged(self, object, tag, condition=None, order_by=None, limit=None, fields=None):

        url = self.build_url('api/getTaggedObjects.sjs')

        params = {'object': object, 'tag': tag}

        if condition:
            params['condition'] = condition
        if order_by:
            params['orderBy'] = order_by
        if limit:
            params['limit'] = limit
        if fields:
            params['include'] = fields

        return self.get(url, params=params)

    def report(self, key):
        url = self.build_url('api/getReport.sjs')
        params = {'report_KEY': key}
        return self.get(url, params=params)

    def save(self, object, values, key=None):

        url = self.build_url('save')

        params = {'object': object}
        params.update(values)
        if key:
            params['key'] = key

        data = self.post(url, params=params)

        if data and data[0].get('result') == 'success':
            return data[0].get('key')

    def tag(self, object, key, tag):
        url = self.build_url('api/tagObject.sjs')
        params = {
            'object': object,
            'key': key,
            'tag': tag,
        }
        return self.post(url, params=params)

    def link(self, object, key, to_object, with_key):
        url = self.build_url('save')
        params = {
            'object': object,
            'key': key,
            'link': to_object,
            'linkKey': with_key,
        }
        return self.get(url, params=params)

    def delete(self, object, key):
        url = self.build_url('api/delete')
        params = {'object': object, 'key': key}
        return self.get(url, params=params)

    #
    # custom fetch methods
    #

    def group(self, group_id):
        object = self.object(Group.object, group_id)
        return Group(object)

    def groups(self, **kwargs):
        objects = self.objects(Group.object, **kwargs)
        return Group.from_list(objects)

    def supporter(self, supporter_id):
        object = self.object(Supporter.object, supporter_id)
        return Supporter(object)

    def supporters(self, **kwargs):
        objects = self.objects(Supporter.object, **kwargs)
        return Supporter.from_list(objects)

    #
    # custom action methods
    #

    def add_to_group(self, supporter, group):
        return self.link(supporter.object, supporter.key, group.object, group.key)

    def remove_from_group(self, supporter, group):
        condition = "supporter_KEY=%s&groups_KEY=%s" % (supporter.key, group.key)
        groups = self.objects(SupporterGroup.object, condition=condition)
        if groups:
            self.delete(SupporterGroup.object, groups[0]['key'])
            return True


salsa = Client()
