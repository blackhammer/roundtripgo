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
#

import sys
sys.path.append("./signup")
sys.path.append("./yellow/business")
sys.path.append("./db")
sys.path.append("./home")  

import webapp2
import os  
from home import *
from search import *
from newexcursion import *
from viewexcursion import *
from signup.signup import *
from signup.login import *



class MainHandler(webapp2.RequestHandler):
	def get(self):
		usercookie = self.request.cookies.get('user_id', '0')
		cookieValidator = AuthenticationManager()
		
		valid_cookie = cookieValidator.validate_cookie(usercookie)
		
		if valid_cookie:
			self.redirect("/home")
		else:
			template = self.load_template()
			self.response.out.write(template)

	def load_template(self):		
		path = os.path.join(os.path.dirname(__file__), './pages/default.html')
		template = Template(filename=path)
		
		return template.render()
    

                              
PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/home', HomeHandler),
										 ('/newexcursion', NewExcursionHandler),
										 ('/viewexcursion/(\d+)', ViewExcursionHandler),
										 ('/search', SearchPageHandler),
										 ('/results', SearchResultPageHandler),
										 ('/signup', SignUpHandler),										 
                               ('/login', LoginHandler),
                               ('/logout', LogoutHandler),                               
                               ('/', MainHandler),
                               ],
                              debug=True)
