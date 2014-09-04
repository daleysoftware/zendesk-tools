import json
import urllib2

from zendesk.cache import AbstractObjectCacher
from zendesk.web import read_json_from_url
from zendesk.encoding import merge_json_objects

class DomainConfiguration:
    """
    Represents configuration related to your Zendesk domain.
    """

    def __init__(self, sub_domain):
        self.sub_domain = sub_domain
        self.base_url = 'https://%s.zendesk.com' % sub_domain

    def get_home_url(self):
        return self.base_url

    def get_help_center_url(self, url):
        return self.base_url + '/api/v2/help_center/' + url

class HelpCenter(AbstractObjectCacher):
    """
    Represents a Zendesk Help Center.
    """

    def __init__(self, config):
        AbstractObjectCacher.__init__(self)
        self.config = config

    def _process(self):
        def get_url():
            return self.config.get_help_center_url('categories.json')
        self._cache(json.loads(urllib2.urlopen(get_url()).read()))

    def get_categories(self):
        """
        Get the category objects belonging to this help center.
        """
        categories = []
        for category in self._get()['categories']:
            categories.append(Category(self.config, category['id']))
        return categories

class Category(AbstractObjectCacher):
    """
    Represents a Zendesk Help Center Category.
    """

    def __init__(self, config, category_id):
        AbstractObjectCacher.__init__(self)
        self.config = config
        self.category_id = category_id

    def _process(self):
        def get_categories_url():
            return self.config.get_help_center_url('/categories/' + str(self.category_id))
        def get_sections_url():
            return get_categories_url() + '/sections.json'

        info = read_json_from_url(get_categories_url())['category']
        sections = read_json_from_url(get_sections_url())['sections']
        self._cache(merge_json_objects('info', info, 'sections', sections))

    def get_sections(self):
        """
        Get the section objects belonging to this help center.
        """
        sections = []
        for section in self._get()['sections']:
            # XXX The Zendesk API is not cleanly RESTful here.
            #
            # The API gives ALL section object detail when querying /sections, which isn't ideal.
            # We could avoid querying the section detail on creation of this object. For the
            # purposes of this project though, we repeat the query to opt for a cleaner
            # implementation.
            sections.append(Section(self.config, section['id']))
        return sections

    def __str__(self):
        return 'category: %i (%s)' % (self.category_id, self._get()['info']['name'])

class Section(AbstractObjectCacher):
    """
    Represents a Zendesk Help Center Section.
    """

    def __init__(self, config, section_id):
        AbstractObjectCacher.__init__(self)
        self.config = config
        self.section_id = section_id

    def _process(self):
        def get_sections_url():
            return self.config.get_help_center_url('/sections/' + str(self.section_id))
        def get_articles_url():
            return get_sections_url() + '/articles.json'

        info = read_json_from_url(get_sections_url())['section']
        articles = read_json_from_url(get_articles_url())['articles']
        self._cache(merge_json_objects('info', info, 'articles', articles))

    def get_articles(self):
        articles = []
        for article in self._get()['articles']:
            # XXX As with get_sections(), we could avoid the duplicate query here.
            articles.append(Article(self.config, article['id']))
        return articles

    def __str__(self):
        return 'section: %i (%s)' % (self.section_id, self._get()['info']['name'])

class Article(AbstractObjectCacher):
    """
    Represents a Zendesk Help Center Article.
    """

    def __init__(self, config, article_id):
        AbstractObjectCacher.__init__(self)
        self.config = config
        self.article_id = article_id

    def _process(self):
        def get_url():
            return self.config.get_help_center_url('/articles/' + str(self.article_id))
        self._cache(read_json_from_url(get_url())['article'])

    def get_body(self):
        return self._get()['body']

    def get_name(self):
        return self._get()['name']

    def __str__(self):
        return 'article: %i (%s)' % (self.article_id, self.get_name())
