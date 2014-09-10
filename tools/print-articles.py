import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '../python'))
from zendesk.api import DomainConfiguration
from zendesk.api import HelpCenter

def format_img_tags(config, body):
    # Link everything to local anchors, not the public zendesk site.
    while True:
        match = re.search('href="(/[0-9,a-z,A-Z,/,-]*)"', body)
        if not match:
            break
        url = match.group(1)
        # TODO FIXME unsure if this is actually working.
        if 'articles' in url or 'entries' in url:
            article_id = url.split('/')[-1].split('-')[0]
            body = body.replace(url, '#' + article_id)
        else:
            # Unhandled link will break out loop; bail.
            print 'Unhandled URL: ' + url
            exit(1)

    # Images link back to public URL.
    body = body.replace('src="/', 'width="50%" src="' + config.get_home_url() + '/')
    return body

def main(sub_domain):
    config = DomainConfiguration(sub_domain)

    for category in HelpCenter(config).get_categories():
        for section in category.get_sections():
            for article in section.get_articles():
                # XXX This could probably be improved to be prettier.
                print('<a name="%i"></a><h2>%s</h2>' % (article.get_id(), article.get_name()))
                print (format_img_tags(config, article.get_body()))
                print('<p style="page-break-after:always;"></p>')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python %s <zendesk_sub_domain>' % sys.argv[0]
    else:
        main(sys.argv[1])
