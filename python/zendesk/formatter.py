import re

def format_tags_local(config, body):
    return format_img_tags(config, format_a_tags_local(config, body))

def format_tags_remote(config, body):
    return format_img_tags(config, format_a_tags_remote(config, body))

def format_a_tags_remote(config, body):
    return format_a_tags(config, body, False)

def format_a_tags_local(config, body):
    return format_a_tags(config, body, True)

def format_a_tags(config, body, local):
    """
    Format hyper links; point to local anchors if local else point to zendesk help center.
    """
    while True:
        match = re.search('href="(/[0-9,a-z,A-Z,/,-]*)"', body)
        if not match:
            break
        url = match.group(1)
        if 'articles' in url or 'entries' in url:
            article_id = url.split('/')[-1].split('-')[0]

            if local:
                body = body.replace(url, '#' + article_id)
            else:
                body = body.replace(url, config.get_home_url() + '/hc/articles/' + article_id)
        else:
            # Unhandled link will break our loop; bail.
            raise Exception('Unhandled URL: ' + url)

    return body

def format_img_tags(config, body):
    """
    Format img tags; point to the zendesk help center and not just '/'; set width to some
    percentage of the page.
    """
    return body.replace('src="/', 'width="50%" src="' + config.get_home_url() + '/')
