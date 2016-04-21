import os
import urllib
import cgi

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

import search


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

MAIN_PAGE_HTML = """\
<html>
  <body>
    
  </body>
</html>
"""
class results(webapp2.RequestHandler):
    def post(self):
       
        query = self.request.get('search_query')
        
        # Variable below passes through to the results
        search_query = ndb.StringProperty(indexed=True)


        template_values = {
            
            'search_query': search_query,
            'query': query,
            'json_object': json_object,
        }

        template = JINJA_ENVIRONMENT.get_template('results.html')
        self.response.write(template.render(template_values))

class MainPage(webapp2.RequestHandler):
    def get(self):
    	
    	query = self.request.get('search_query')
    	
    	# This variable passes through to the results
    	search_query = ndb.StringProperty(indexed=True)


    	user = "Kristen"
        
        template_values = {
            'user': user,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/index', MainPage),
    ('/results', results),
], debug=True)