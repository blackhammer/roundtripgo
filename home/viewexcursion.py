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

class ViewExcursionHandler(webapp2.RequestHandler):
	def get(self, id):
		#validate the user credentials
		usercookie = self.request.cookies.get('user_id', '0')
		cookieValidator = AuthenticationManager()
		
		valid_cookie = cookieValidator.validate_cookie(usercookie)
		
		if valid_cookie:
			user_id = usercookie.split('|')[0]
			datamanager = ExcursionDataManager()
			
			#get the items for this excursion
			items = datamanager.get_trip_items(int(id))
			
			excursion = datamanager.get_trip(int(user_id),int(id))
			
			if excursion:											
				path = os.path.join(os.path.dirname(__file__), '../pages/excursiondetails.html')
				template = Template(filename=path)
				response = template.render(excursiontitle=excursion.Title, tripid=int(id), tripItems=items)
				self.response.out.write(response)
		else:
			self.redirect("/")
		
		
		
	def post(self):
		pass
		