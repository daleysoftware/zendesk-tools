# Zendesk Tools

The `zendesk-tools` project contains a wrapper for the Zendesk API, and a
number of convenient tools that can be used with Zendesk.

## Prerequistes and Setup

You must have `python2.7` and `virtualenv` installed. To your system so that it
can run this software, run the following:

```
./setup.sh
```

## Tools

### Exporter

This tool exports your Zendesk Help Center to a distributable HTML format,
which is useful for not-so-tech-saavy customers. Export is accomplished using
the [Zendesk Developer API](https://developer.zendesk.com/).

See relevant [feature request](https://support.zendesk.com/entries/84241-Print-PDF-button-in-Forums).

To print your site map:

```
python2.7 tools/exporter/print-sitemap.py <zendesk_sub_domain>
```

To export your articles into one large document:

```
python2.7 tools/exporter/print-articles.py <zendesk_sub_domain>
```

To export individual articles:

```
python 2.7 tools/exporter/print-article.py <zendesk_sub_domain> <article_id>
```

And perhaps the most useful command for exporting your Zendesk Help Center into
different knowledge management systems is as follows. This command will export
each article in your system into its own HTML file.

```
./tools/exporter/export-articles.sh <zendesk_sub_domain>
```

### Suspended User Deleter

*Work in progress.*
