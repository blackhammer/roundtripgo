#!/usr/bin/env python

import sys
import os
import re
import hashlib
import random
import string
import logging

sys.path.append("../yellow/business")
sys.path.append("../db")
sys.path.append("../mako")
sys.path.append("../markupsafe")

from usermanager import *
from home import *
import webapp2
from YellowAPI import *
import json as simplejson
from mako.template import Template

class SearchPageHandler(webapp2.RequestHandler):
	def get(self, id):
		#validate the user credentials
		usercookie = self.request.cookies.get('user_id', '0')
		cookieValidator = AuthenticationManager()
		
		valid_cookie = cookieValidator.validate_cookie(usercookie)
		
		if valid_cookie:
			path = os.path.join(os.path.dirname(__file__), '../pages/searchpage.html')
			template = Template(filename=path)
			response = template.render(tripid=int(id))
			self.response.out.write(response)
		
	def post(self, id):
		#validate the user credentials
		usercookie = self.request.cookies.get('user_id', '0')
		cookieValidator = AuthenticationManager()
		
		valid_cookie = cookieValidator.validate_cookie(usercookie)
		
		if valid_cookie:
			user_id = usercookie.split('|')[0]
			keywords	= self.request.get('searchtext')
			location = self.request.get('searchlocation')
			tripid	= self.request.get('tripid')
			
			yellowAPI 	= YellowAPI('qzd5mb8s9nwdtgptzqcrz2mk', 'RoundTripGo', True, 'JSON', [])
			results 		= yellowAPI.find_business(keywords, location, 1, 40, '', 'en')
			
			if results:
				path = os.path.join(os.path.dirname(__file__), '../pages/resultspage.html')
				template = Template(filename=path)
				jsonresult = {'result': simplejson.loads(results)}	
				#logging.error(jsonresult)
				response = template.render(result=jsonresult)
				self.response.out.write(response)
			else:
				self.redirect("/home")
			
		
class SearchResultPageHandler(webapp2.RequestHandler):
	def get(self):
		#validate the user credentials
		usercookie = self.request.cookies.get('user_id', '0')
		cookieValidator = AuthenticationManager()
		
		valid_cookie = cookieValidator.validate_cookie(usercookie)
		
		#if valid_cookie:
		
	def post(self):
		pass