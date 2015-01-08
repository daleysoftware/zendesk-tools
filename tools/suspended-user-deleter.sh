#!/bin/bash
set -eu

# Starting point:
curl -s -u matt@aerofs.com/token:<REDACTED> https://aerofs.zendesk.com/api/v2/users | python -m json.tool
