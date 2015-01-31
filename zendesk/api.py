from requests.auth import HTTPBasicAuth

from zendesk.cache import AbstractObjectCacher
from zendesk.web import read_json_from_url
from zendesk.web import do_delete
from zendesk.encoding import merge_json_objects


LOGGING_ENABLED = True

def log(message):
    if LOGGING_ENABLED: print(message)


class DomainConfiguration:
    """
    Represents configuration related to your Zendesk domain.
    """

    def __init__(self, sub_domain):
        self.sub_domain = sub_domain
        self.base_url = 'https://%s.zendesk.com' % sub_domain

    def get_home_url(self):
        return self.base_url

    def get_hc_url(self, url):
        return self.base_url + '/api/v2/help_center' + url


    def get_api_url(self, url):
        return self.base_url + '/api/v2' + url

class HelpCenterCredentials:
    """
    Represents token or username/password credentials for your Zendesk help center.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_basic_auth_object(self):
        return HTTPBasicAuth(username=self.username + '/token', password=self.password)


class HelpCenter(AbstractObjectCacher):
    """
    Represents a Zendesk Help Center.
    """


    class Category(AbstractObjectCacher):
        """
        Represents a Zendesk Help Center Category.
        """

        def __init__(self, hc, cit):
            AbstractObjectCacher.__init__(self)
            self.hc = hc
            self.cit = cit

        def _process(self):
            def get_categories_url():
                return self.hc.domain_config.get_hc_url('/categories/' + str(self.cit))
            def get_sections_url():
                return get_categories_url() + '/sections.json'

            info = self.hc.read_json_from_url(get_categories_url())['category']
            sections = self.hc.read_json_from_url(get_sections_url())['sections']
            self._cache(merge_json_objects('info', info, 'sections', sections))

        def get_sections(self):
            """
            Get the section objects belonging to this help center.
            """
            sections = []
            for section in self._get()['sections']:
                sections.append(HelpCenter.Section(self.hc, section['id']))
            return sections

        def __str__(self):
            return 'category: %i (%s)' % (self.cit, self._get()['info']['name'])


    class Section(AbstractObjectCacher):
        """
        Represents a Zendesk Help Center Section.
        """

        def __init__(self, hc, sid):
            AbstractObjectCacher.__init__(self)
            self.hc = hc
            self.sid = sid

        def _process(self):
            def get_sections_url():
                return self.hc.domain_config.get_hc_url('/sections/' + str(self.sid))
            def get_articles_url():
                return get_sections_url() + '/articles.json'

            info = self.hc.read_json_from_url(get_sections_url())['section']
            articles = self.hc.read_json_from_url(get_articles_url())['articles']
            self._cache(merge_json_objects('info', info, 'articles', articles))

        def get_articles(self):
            articles = []
            for article in self._get()['articles']:
                articles.append(HelpCenter.Article(self.hc, article['id']))
            return articles

        def __str__(self):
            return 'section: %i (%s)' % (self.sid, self._get()['info']['name'])


    class Article(AbstractObjectCacher):
        """
        Represents a Zendesk Help Center Article.
        """

        def __init__(self, hc, aid):
            AbstractObjectCacher.__init__(self)
            self.hc = hc
            self.aid = aid

        def _process(self):
            def get_url():
                return self.hc.domain_config.get_hc_url('/articles/' + str(self.aid))
            self._cache(self.hc.read_json_from_url(get_url())['article'])

        def get_id(self):
            return self.aid

        def get_body(self):
            return self._get()['body']

        def get_name(self):
            return self._get()['name']

        def __str__(self):
            return 'article: %i (%s)' % (self.aid, self.get_name())


    class User:
        """
        Respresents a Zendesk Help Center user.
        """

        def __init__(self, hc, uid):
            self.hc = hc
            self.uid = uid

        def delete(self):
            def get_url():
                return self.hc.domain_config.get_api_url('/users/%i.json' % self.uid)
            do_delete(get_url(), self.hc.auth)

        def __str__(self):
            return 'user %i' % self.uid


    def __init__(self, domain_config, credentials=None):
        AbstractObjectCacher.__init__(self)
        self.domain_config = domain_config

        self.auth = credentials
        if credentials is not None:
            self.auth = credentials.get_basic_auth_object()

    def _process(self):
        def get_url():
            return self.domain_config.get_hc_url('/categories.json')
        self._cache(read_json_from_url(get_url(), auth=self.auth))

    def read_json_from_url(self, url):
        return read_json_from_url(url, auth=self.auth)

    def get_categories(self):
        """
        Get the category objects belonging to this help center.
        """
        categories = []
        for category in self._get()['categories']:
            categories.append(HelpCenter.Category(self, category['id']))
        return categories


    def get_suspended_users(self, max_users=0):
        def get_url():
            return self.domain_config.get_api_url('/users.json')
        def append_to_result():
            for user in json['users']:
                if user['suspended']:
                    result.append(HelpCenter.User(self, user['id']))
        log("Getting users list...")
        counter = 0
        result = []
        url = get_url()
        while True:
            log("(%i) GET %s" % (len(result), url))
            counter += 1
            json = self.read_json_from_url(url)
            append_to_result()
            if 'next_page' not in json or json['next_page'] is None: break
            if max_users != 0 and len(result) >= max_users: break
            url = json['next_page']
        return result

    def delete_suspended_users(self):
        for user in self.get_suspended_users():
            log("Delete %s" % user)
            user.delete()

