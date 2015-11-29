#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Demonstration GET users/suggestions
# See https://dev.twitter.com/rest/reference/get/users/suggestions

from secret import twitter_instance

tw = twitter_instance()
response = tw.users.suggestions()

for i in response:
    print('{name}|{slug}|{size}'.format(**i))
