"""
Python script to print a single zendesk article.
"""

import sys

from zendesk.api import DomainConfiguration
from zendesk.api import HelpCenter
from zendesk.formatter import format_tags_remote

def main(sub_domain, aid):
    config = DomainConfiguration(sub_domain)
    hc = HelpCenter(config)
    article = HelpCenter.Article(hc, aid)

    print('<h2>%s</h2>' % article.get_name())
    print (format_tags_remote(config, article.get_body()))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: python %s <zendesk_sub_domain> <article_id>' % sys.argv[0]
    else:
        main(sys.argv[1], sys.argv[2])
