Zendesk Exporter
===

This tool exports your Zendesk Help Center to a distributable HTML format,
which is useful for not-so-tech-saavy customers. Export is accomplished using
the [Zendesk Developer API](https://developer.zendesk.com/).

See relevant [feature request](https://support.zendesk.com/entries/84241-Print-PDF-button-in-Forums).

Prerequisites
---
* Python 2.7.x

Usage
---

To print your site map:

    python2.7 tools/print-sitemap.py <zendesk_sub_domain>

To export your articles into one large document:

    python2.7 tools/print-articles.py <zendesk_sub_domain>

To export individual articles:

    python 2.7 tools/print-article.py <zendesk_sub_domain> <article_id>
