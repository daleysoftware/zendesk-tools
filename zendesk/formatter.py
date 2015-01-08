import re

def format_tags_local(config, body):
    return _format_img_tags(config, _format_a_tags_local(body))

def format_tags_remote(config, body):
    return _format_img_tags(config, _format_a_tags_remote(body))

def _format_a_tags_remote(body):
    return _format_a_tags(body, False)

def _format_a_tags_local(body):
    return _format_a_tags(body, True)

def _format_a_tags(body, local):
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
                body = body.replace(url, './' + article_id + '.html')
        else:
            # Unhandled link will break our loop; bail.
            raise Exception('Unhandled URL: ' + url)

    return body

def _format_img_tags(config, body):
    """
    Format img tags; point to the zendesk help center and not just '/'; set width to some
    percentage of the page.
    """
    body = body.replace('src=', 'style="max-width:50%" src=')
    return body.replace('src="/', 'src="' + config.get_home_url() + '/')
