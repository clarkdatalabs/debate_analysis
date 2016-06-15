#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Whoosh stuff
# import setup.py
# from whoosh import store
# from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
# from whoosh.index import getdatastoreindex
# from whoosh.qparser import QueryParser, MultifieldParser
# import logging

# from google.appengine.ext import webapp
# from google.appengine.ext.webapp.util import run_wsgi_app


# Update: Kanchi taught me how to use the google app egine and we reorganized the files
# Got everything reordered and set up how it had been last week
# Started trying to import the Schema.py
# first problem is that whoosh isn't able to import. Steps followed:
# imported it in main.py
# created a set.py file to import it
# following instructions on this github: https://github.com/tallstreet/Whoosh-AppEngine
# some articles say to download Whoosh App engine but I can't find where to download it

# Next work around idea is to create a libs part of the app.
# This directory should contain all the external python packages
# you want to bundle in your app. For ex. in this sample,
# I have bundled mako templating framework
# So I think that I have to take all of the source packages from Whoosh and stick
# them into this lib area
# Then create a fix_path.py file to import os, sys, and all of the libraries
# import fix_path in the main.py file


import appengine_config

# This is all the previous stuff
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import os
import logging
import jinja2
import cgi
import Schema
import search
import json
from whoosh.index import open_dir
from whoosh.qparser import QueryParser





JINJA_ENVIRONMENT=jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions= ['jinja2.ext.autoescape'],
	autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	user = "Kristen"

        template_values = {
            'user': user,
        }

        query = self.request.get('search_query')
        search_query = ndb.StringProperty(indexed=True)

        template=JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))





class ResultsHandler(webapp2.RequestHandler):

    def get(self):
		query = self.request.get('search_query')
		search_query = ndb.StringProperty(indexed=True)
		# results = ndb.JsonProperty('json_object', indexed=True)
		results = search.function(query)

		template_values = {
		    'search_query': search_query,
		    'query': query,
		    'results': unicode(results),
		}
		template = JINJA_ENVIRONMENT.get_template('templates/results.json')
		self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
		self.response.write(results)



    def post(self):
        query = self.request.get('search_query')
        search_query = ndb.StringProperty(indexed=True)
        # results = ndb.JsonProperty('json_object', indexed=True)
        results = search.function(query)

        template_values = {
            'search_query': search_query,
            'query': query,
            'results': results,
        }
        template = JINJA_ENVIRONMENT.get_template('templates/results.json')
        self.response.out.write(unicode(results))

class TestHandler(webapp2.RequestHandler):
    def get(self):
    	user = "Kristen"

        template_values = {
            'user': user,
        }

        query = self.request.get('search_query')
        search_query = ndb.StringProperty(indexed=True)

        template=JINJA_ENVIRONMENT.get_template('templates/results.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', TestHandler),
    ('/index', MainHandler),
    ('/results', ResultsHandler)
], debug=True)
