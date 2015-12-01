# -*- coding: utf-8 -*-
"""secret.py: Encapsulate initializing Twitter interface.
"""

# The module 'twitter' is provided by Python Twitter Tools.
import twitter
import os

__version__ = '1.3.0'

# Keep the "Consumer Secret" a secret.
# This key should never be human-readable in your application.
CONSUMER_KEY = 'pBXKrfuhVW14XWnE4Mvm9Tfs6'
CONSUMER_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# The following values (only rhs values) are written in ~/.my_app_credentials
# by twitter.oauth_dance.
#USER_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
#USER_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

MY_TWITTER_CREDS = os.path.expanduser('~/.my_app_credentials')

def setup_auth():
    """Setup an instance of class OAuth."""

    if not os.path.exists(MY_TWITTER_CREDS):
        twitter.oauth_dance(
            "My App Name", CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)

    oauth_token, oauth_secret = twitter.read_token_file(MY_TWITTER_CREDS)
    return twitter.OAuth(
        oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET)

def twitter_instance():
    """Create an instance of class Twitter."""
    return twitter.Twitter(auth=setup_auth())

def twitter_stream(**kwargs):
    """Create an instance of class TwitterStream."""
    return twitter.TwitterStream(auth=setup_auth(), **kwargs)
