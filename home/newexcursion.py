#!/usr/bin/env python

import sys
import os
import re
import hashlib
import random
import string

sys.path.append("../yellow/business")
sys.path.append("../db")
sys.path.append("../mako")
sys.path.append("../markupsafe")

from usermanager import *
from home import *
import webapp2
from mako.template import Template

class NewExcursionHandler(webapp2.RequestHandler):
	def get(self):
		usercookie = self.request.cookies.get('user_id', '0')
		cookieValidator = AuthenticationManager()
		
		valid_cookie = cookieValidator.validate_cookie(usercookie)
		
		if valid_cookie:
			user_id = usercookie.split('|')[0]
			user = User.get_by_id(int(user_id))
			if user:						
				path = os.path.join(os.path.dirname(__file__), '../pages/createexcursion.html')
				template = Template(filename=path)
				response = template.render(username=user.UserName, userid=user_id)
				self.response.out.write(response)
		
	def post(self):
		usercookie = self.request.cookies.get('user_id', '0')
		cookieValidator = AuthenticationManager()
		
		valid_cookie = cookieValidator.validate_cookie(usercookie)
		
		if valid_cookie:
			user_id = usercookie.split('|')[0]
			title	= self.request.get('title')
			desc 	= self.request.get('description')
			
		
			if title and user_id:
				datamanager = ExcursionDataManager()
				datamanager.add_trip(int(user_id), title, desc)
			
				#refresh cache
				datamanager.get_trip_list(int(user_id), True)
				self.redirect("/home")

class AddExcursionHandler(webapp2.RequestHandler):
	def get(self, id):
		usercookie = self.request.cookies.get('user_id', '0')
		cookieValidator = AuthenticationManager()
		
		valid_cookie = cookieValidator.validate_cookie(usercookie)
		
		if valid_cookie:
			user_id 	= usercookie.split('|')[0]
			tripid	= int(id)
			busid		= int(self.request.get('bus_id'))
			busname 	= self.request.get('bus_name')
			
			if busid and busname and tripid:
				datamanager = ExcursionDataManager()
				datamanager.add_trip_item(tripid, busname, busid)
			
				#refresh cache
				datamanager.get_trip_items(tripid, True)
				self.redirect("/results/%s" % tripid)
	
	def post(self):
		pass
			