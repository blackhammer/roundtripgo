"""
 Copyright 2011, Yellow Pages Group Co.  All rights reserved.
 Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

 1)	Redistributions of source code must retain a complete copy of this notice, including the copyright notice, this list of conditions and the following disclaimer; and
 2)	Neither the name of the Yellow Pages Group Co., nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT OWNER AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

 Requires: Python 2.3+
 Version: 0.1 (2010-09-15)
"""
import json as simplejson
import urllib2
import urllib
import itertools
import re


class YellowAPI(object):
	"""
	A thin wrapper around urllib2 to perform calls to YellowAPI.  This class
	does not do any processing of the response contents (XML or JSON). 
	"""

	PROD_URL = 'http://api.yellowapi.com'
	TEST_URL = 'http://api.sandbox.yellowapi.com'

	def __init__(self, api_key, uid ,test_mode=False, format='XML', handlers=[]):
		if len(api_key) != 24:
			raise TypeError('api_key should be 24 characters.')
		self.api_key = api_key
		self.uid = uid
		
		if test_mode:
			self.url = self.TEST_URL
		else:
			self.url = self.PROD_URL

		if format not in ['XML', 'JSON']:
			raise TypeError('Format should be XML or JSON')
		self.format = format

		self.opener = urllib2.build_opener(*handlers)
		self.last_url = None
		

	def find_business(self, what, where, page=None, page_len=None, 
			sflag=None, lang=None):
		"""
		Perform the FindBusiness call.
		"""
		url = self._build_url('FindBusiness', what=what, where=where, 
				pg=page, pgLen=page_len, sflag=sflag, lang=lang)
		return self._perform_request(url)

	
	def get_business_details(self, city, prov, bus_name, listing_id, lang=None):
		"""
		Perform the GetBusinessDetails call.
		"""
		kws = {'prov': self.encode_info(prov), 'bus-name': self.encode_info(bus_name), 
				'listingId': listing_id, 'city': self.encode_info(city), 
				'lang': lang
				}
		url = self._build_url('GetBusinessDetails', **kws)
		return self._perform_request(url)


	def find_dealer(self, pid, page=None, page_len=None, lang=None):
		"""
		Perform the FindDealer call.
		"""
		url = self._build_url('FindDealer', pid=pid, pg=page, 
				pgLen=page_len, lang=lang)
		return self._perform_request(url)	
  			

	def get_last_query(self):
		"""
		Used for debugging purposes.  Displays the url string used in the 
		last calls.
		"""
		return self.last_url

	NAME_PATTERN = re.compile('[^A-Za-z0-9]+')
	@staticmethod
	def encode_info(name):
		"""
		Properly encode the business name for subsequent queries.
		"""
		return YellowAPI.NAME_PATTERN.sub('-', name)

	def _build_url(self, method, **kwargs):
		"""
		Build an HTTP url for the request.
		"""
		kwargs.update({'apikey': self.api_key, 'fmt': self.format, 'UID': self.uid})
		params = ["%s=%s" % (k,urllib.quote(str(v))) for (k,v) in itertools.ifilter(
				lambda (k,v): v is not None, kwargs.iteritems())]

		self.last_url = "%s/%s/?%s" % (self.url, method, "&".join(params))
		return self.last_url

	def _perform_request(self, url):
		"""
		Perform the GET Request and handle HTTP response.
		"""
		resp = None
		try:
			resp = self.opener.open(url)
			body = resp.read()
		except urllib2.HTTPError, err:
			if err.code == 400:
				msg = err.read()
				err.msg += "\n" + msg
			raise(err)
		finally:
			if resp:
				resp.close()
		return body