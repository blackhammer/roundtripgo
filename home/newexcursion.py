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
		title	= self.request.get('title')
		desc 	= self.request.get('description')
		user_id = int(self.request.get('userid'))
		
		if title and user_id:
			datamanager = ExcursionDataManager()
			datamanager.add_trip(user_id, title, desc)
			
			#refresh cache
			datamanager.get_trip_list(user_id, True)
			self.redirect("/home")
			