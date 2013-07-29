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

from google.appengine.api import memcache

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
			
			yellowAPI 	= YellowAPI('qzd5mb8s9nwdtgptzqcrz2mk', user_id, True, 'JSON', [])
			results 		= yellowAPI.find_business(keywords, location, 1, 15, '', 'en')
			
			if results:
				#put results in cache
				
				path = os.path.join(os.path.dirname(__file__), '../pages/resultspage.html')
				template = Template(filename=path)
				jsonresult = {'result': simplejson.loads(results)}	
				#logging.error(jsonresult)
				response = template.render(tripid=int(id),result=jsonresult)
				self.response.out.write(response)
			else:
				self.redirect("/home")
			
		
class SearchResultPageHandler(webapp2.RequestHandler):
	#display the search results from cache
	def get(self, id):
		#validate the user credentials
		usercookie = self.request.cookies.get('user_id', '0')
		cookieValidator = AuthenticationManager()
		
		valid_cookie = cookieValidator.validate_cookie(usercookie)
		
		if valid_cookie:
			user_id = usercookie.split('|')[0]
			
		
	def post(self):
		pass
		
class SearchResultDetailsPageHandler(webapp2.RequestHandler):		
	def get(self, id):
		#validate the user credentials
		usercookie = self.request.cookies.get('user_id', '0')
		cookieValidator = AuthenticationManager()
		
		valid_cookie = cookieValidator.validate_cookie(usercookie)
		
		if valid_cookie:
			user_id 	= usercookie.split('|')[0]
			bus_id 	= self.request.get('bus_id')
			prov 		= self.request.get('prov')
			city 		= self.request.get('city')
			bus_name = self.request.get('bus_name')
			path_qs  = self.request.path_qs

			# Fetch merchant details
			yellowAPI 	= YellowAPI('qzd5mb8s9nwdtgptzqcrz2mk', user_id, True, 'JSON', [])
			results = yellowAPI.get_business_details(prov, city, bus_name, int(bus_id), 'en')
			
			if results:
				path = os.path.join(os.path.dirname(__file__), '../pages/resultsdetails.html')
				template = Template(filename=path)
				jsonresult = {'result': simplejson.loads(results)}				
				response = template.render(tripid=int(id), busid=bus_id, busname=bus_name, targeturl=path_qs, result=jsonresult)
				self.response.out.write(response)			
			else:
				self.redirect("/home")
				
				
	def post(self):
		pass