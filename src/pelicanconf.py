#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Structured Commons'
SITENAME = u'Structured Commons'
SITEURL = 'http://www.structured-commons.org'

TIMEZONE = 'Europe/Amsterdam'

TYPOGRIFY = True

THEME = u'gum-sc'

DEFAULT_LANG = u'en'

PLUGIN_PATH = 'plugins'
PLUGINS = ['html_rst_directive','specs']
DIRECT_TEMPLATES = ['archives']

# Pages
DISPLAY_PAGES_ON_MENU = True
PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
#LINKS =  (('Python', 'http://python.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# required by theme
GITHUB_URL = ''
TWITTER_URL = ''
FACEBOOK_URL = ''
GOOGLEPLUS_URL = ''
GOOGLE_ANALYTICS_ID = ''
GOOGLE_ANALYTICS_SITENAME = ''

# List of files to copy from source to destination
STATIC_PATHS = []
EXTRA_PATH_METADATA = { }
from os import popen
for i in popen('find content/static ! -type d'):
    n = i.rstrip()
    if n == 'content/static': continue
    static = n.split('/', 1)[1]
    rel = static.split('/', 1)[1]
    STATIC_PATHS.append(static)
    EXTRA_PATH_METADATA[static] = { 'path' : rel, 'status' : 'hidden' }
