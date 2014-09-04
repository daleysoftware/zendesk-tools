import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '../python'))

from zendesk.api import DomainConfiguration
from zendesk.api import HelpCenter

def format_img_tags(config, body):
    # Links
    body = body.replace('href="/', 'href="' + config.get_home_url() + '/')
    # Images
    body = body.replace('src="/', 'src="' + config.get_home_url() + '/')
    return body

def main(sub_domain):
    config = DomainConfiguration(sub_domain)

    for category in HelpCenter(config).get_categories():
        for section in category.get_sections():
            for article in section.get_articles():
                # XXX This could probably be improved to be prettier.
                print('<h2>%s</h2>' % article.get_name())
                print (format_img_tags(config, article.get_body()))
                print('<p style="page-break-after:always;"></p>')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python %s <zendesk_sub_domain>' % sys.argv[0]
    else:
        main(sys.argv[1])
