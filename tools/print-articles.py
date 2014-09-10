import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../python'))
from zendesk.api import DomainConfiguration
from zendesk.api import HelpCenter
from zendesk.formatter import format_tags_local

def main(sub_domain):
    config = DomainConfiguration(sub_domain)

    for category in HelpCenter(config).get_categories():
        for section in category.get_sections():
            for article in section.get_articles():
                # XXX This could probably be improved to be prettier.
                print('<a name="%i"></a><h2>%s</h2>' % (article.get_id(), article.get_name()))
                print (format_tags_local(config, article.get_body()))
                print('<p style="page-break-after:always;"></p>')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python %s <zendesk_sub_domain>' % sys.argv[0]
    else:
        main(sys.argv[1])
