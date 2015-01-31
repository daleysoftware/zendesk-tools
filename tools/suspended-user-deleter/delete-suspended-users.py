"""
Python script to delete all suspended users in your zendesk system.
"""

import sys

from zendesk.api import DomainConfiguration
from zendesk.api import HelpCenter
from zendesk.api import HelpCenterCredentials

def main(sub_domain, admin_email, admin_token):
    config = DomainConfiguration(sub_domain)
    credentials = HelpCenterCredentials(admin_email, admin_token)
    hc = HelpCenter(config, credentials)
    hc.delete_suspended_users()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python %s <zendesk_sub_domain> <admin_email> <admin_token>" % sys.argv[0])
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
