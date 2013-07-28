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
			userid = usercookie.split('|')[0]
			user = User.get_by_id(int(userid))
			if user:						
				path = os.path.join(os.path.dirname(__file__), '../pages/createexcursion.html')
				template = Template(filename=path)
				response = template.render(username=user.UserName)
				self.response.out.write(response)
		
	def post(self):
		username	= self.request.get('username')
		passwd 	= self.request.get('password')