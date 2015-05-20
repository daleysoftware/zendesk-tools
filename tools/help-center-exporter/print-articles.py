"""
Python script to print all zendesk domain articles as a single entity. Useful for checking global
formatting properties or your articles.

N.B. this python app currently does not have a wrapper script.
"""

import sys

from zendesk.api import DomainConfiguration
from zendesk.api import HelpCenter
from zendesk.formatter import format_tags_local

def main(sub_domain):
    config = DomainConfiguration(sub_domain)
    hc = HelpCenter(config)

    for category in hc.get_categories():
        for section in category.get_sections():
            for article in section.get_articles():
                # XXX This could probably be improved to be prettier.
                print('<a name="%i"></a><h2>%s</h2>' % (article.get_id(), article.get_name()))
                print(format_tags_local(config, article.get_body()))
                print('<p style="page-break-after:always;"></p>')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python %s <zendesk_sub_domain>' % sys.argv[0])
    else:
        main(sys.argv[1])
