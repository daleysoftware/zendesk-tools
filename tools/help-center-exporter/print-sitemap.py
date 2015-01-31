"""
Python script to print the sitemap of a zendesk help center.
"""

import sys

from zendesk.api import DomainConfiguration
from zendesk.api import HelpCenter

def main(sub_domain):
    config = DomainConfiguration(sub_domain)
    hc = HelpCenter(config)

    for category in hc.get_categories():
        print category
        for section in category.get_sections():
            print '\t%s' % section
            for article in section.get_articles():
                print '\t\t%s' % article

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python %s <zendesk_sub_domain>' % sys.argv[0]
    else:
        main(sys.argv[1])

