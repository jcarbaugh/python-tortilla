import requests


class SalsaObject(object):

    _data = {}

    def __init__(self, initial=None):
        if initial:
            self._data.update(initial)

    def __getattr__(self, attr):
        # attr = self.fields.get(attr, attr)
        if attr in self._data:
            return self._data[attr]

    def __setattr__(self, attr, value):
        # attr = self.fields.get(attr, attr)
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

class Supporter(SalsaObject):
    object = 'supporter'

    def __repr__(self):
        return u"<Supporter: %s %s %s>" % (self.first_name, self.last_name, self.email)

class SupporterAction(SalsaObject):
    object = 'supporter_action'

class SupporterEvent(SalsaObject):
    object = 'supporter_event'

class SupporterGroup(SalsaObject):
    object = 'supporter_groups'

class SignupPage(SalsaObject):
    object = 'signup_page'

# other objects: distributed_event, supporter_action_comment,
# supporter_action_target, supporter_action_content, chapter


class AuthenticationError(Exception):
    pass

class Client(object):

    def __init__(self):
        # self.base_url =
        self.hq = None
        self.http = requests.Session()
        self.http.headers.update({'User-Agent': 'python-tortilla'})
        self.http.params = {'json': 'true'}
        self.authenticated = False

    def build_url(self, path, secure=True):
        scheme = 'https' if secure else 'http'
        return "%s://%s.salsalabs.com/%s" % (scheme, self.hq, path)

    def authenticate(self, hq, email, password, org_key=None, chapter_key=None):

        self.hq = hq

        url = self.build_url('api/authenticate.sjs')

        params = {
            'email': email,
            'password': password,
        }

        if org_key:
            params['organization_KEY'] = org_key
        if chapter_key:
            params['chapter_KEY'] = chapter_key

        resp = self.http.get(url, params=params)
        data = resp.json()

        if 'status' in data and data['status'] == 'success':
            self.authenticated = True
            return True

        raise AuthenticationError(data.get('message', 'Unable to authenticate'))

    def describe(self, object):

        url = self.build_url('api/describe2.sjs')

        params = {'object': object}

        resp = self.http.get(url, params=params)
        return resp.json()

    def object(self, object, key):

        url = self.build_url('api/getObject.sjs')

        params = {
            'object': object,
            'key': key,
        }

        resp = self.http.get(url, params=params)
        return resp.json()

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

        resp = self.http.get(url, params=params)
        return resp.json()

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

        resp = self.http.get(url, params=params)
        return resp.json()

    def report(self, key):
        url = self.build_url('api/getReport.sjs')
        params = {'report_KEY': key}
        resp = self.http.get(url, params=params)
        return resp.json()

    def save(self, object, values, key=None):

        url = self.build_url('save')

        params = {'object': object}
        params.update(values)
        if key:
            params['key'] = key

        resp = self.http.post(url, params=params)
        data = resp.json()

        if data and data[0].get('result') == 'success':
            return data[0].get('key')

    def tag(self, object, key, tag):
        url = self.build_url('api/tagObject.sjs')
        params = {
            'object': object,
            'key': key,
            'tag': tag,
        }
        resp = self.http.post(url, params=params)
        return resp.json()

    def link(self, object, key, to_object, with_key):
        url = self.build_url('save')
        params = {
            'object': object,
            'key': key,
            'link': to_object,
            'linkKey': with_key,
        }
        resp = self.http.get(url, params=params)
        return resp.json()

    def delete(self, object, key):
        url = self.build_url('api/delete')
        params = {'object': object, 'key': key}
        resp = self.http.get(url, params=params)
        return resp.json()

salsa = Client()
