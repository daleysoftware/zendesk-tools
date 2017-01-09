# Zendesk Tools

The `zendesk-tools` project contains a python wrapper for the Zendesk API, and
a number of convenient scripts that can be used with Zendesk.

## See Also

[Eventbrite's Zendesk Python API](https://github.com/eventbrite/zendesk).

While the tools in this repository work, Eventbrite's API is more full-featured
and might serve you better.

## Prerequistes and Setup

You must have `python3` and `virtualenv` installed. To setup your system so
that it can run this software, execute the following:

```
./setup.sh
```

## Tools

### Help Center Exporter

This tool exports your Zendesk Help Center to a distributable HTML format,
which is useful for not-so-tech-saavy customers. Export is accomplished using
the [Zendesk Developer API](https://developer.zendesk.com/).

See relevant [feature request](https://support.zendesk.com/entries/84241-Print-PDF-button-in-Forums).

```
./tools/help-center-exporter/export-articles.sh <zendesk_sub_domain>
```

### Suspended User Deleter

This tool deletes all suspended users in your Zendesk system.

```
./tools/suspended-user-deleter/delete-suspended-users.sh \
    <zendesk_sub_domain> \
    <admin_email> \
    <admin_token>
```
