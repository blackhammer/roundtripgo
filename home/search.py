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

class SearchPageHandler(webapp2.RequestHandler):
	def get(self):
		#validate the user credentials
		usercookie = self.request.cookies.get('user_id', '0')
		cookieValidator = AuthenticationManager()
		
		valid_cookie = cookieValidator.validate_cookie(usercookie)
		
		#if valid_cookie:
		
	def post(self):
		pass
		
class SearchResultPageHandler(webapp2.RequestHandler):
	def get(self):
		#validate the user credentials
		usercookie = self.request.cookies.get('user_id', '0')
		cookieValidator = AuthenticationManager()
		
		valid_cookie = cookieValidator.validate_cookie(usercookie)
		
		#if valid_cookie:
		
	def post(self):
		pass