#!/usr/bin/env python

from google.appengine.ext import db
from google.appengine.api import memcache
from datetime import *
import logging


class RoundTripDataManager():
	def __init__(self):
		pass
		
	#Return the list of trips for a User
	def trip_list(self, user_id, update = False):
		key_trips = "user_trips_%s" % user_id 		
		entries = memcache.get(key_trips)
		
		if entries is not None and not update:			
			return entries
		else:			
			entries = db.GqlQuery("SELECT * from Trip WHERE UserId = :1 ORDER BY Created DESC", user_id)			
							
			entries = list(entries)			
			memcache.set(key_trips, entries)			
								
			return entries
	
	#Get the list of trip items for a given user and trip id
	def get_trip_items(self, tripId, update = False):
		key_trips = "trip_items_%s" % (tripId)		
		
		entry = memcache.get(key_trips)
		
		if entry is not None and not update:						
			return entry
		else:			
			entry = db.GqlQuery("SELECT * from TripItem WHERE TripId = :1 ORDER BY Version DESC",pagename)
			#entry = list(entry)						
			if entry.count() >= 1:
				entry = entry[0]
				lastupdated = datetime.now()
				memcache.set(key_post,entry)
				memcache.set(key_time,lastupdated)
				return entry, lastupdated
			else:
				return None, None
				
	def get_page_version(self, pagename, version):
		key_post_version = "version_post_%s_%s" % (pagename, version)
		key_version_time = "version_post_time%s_%s" % (pagename, version)
				
		#logging.error("page: %s,version: %s" % (pagename, version))
		entry = memcache.get(key_post_version)
		
		if entry is not None:
			#logging.error("cacheHit")
			lastupdated = memcache.get(key_version_time)
			return entry, lastupdated
		else:
			entry = db.GqlQuery("SELECT * FROM WikiPage WHERE PageName=:1 AND Version=:2",pagename, int(version))
			#logging.error("gqlQueried")
			if entry is not None and entry.count()>0:
				entry = entry[0]
				lastupdated = datetime.now()
				memcache.set(key_post_version, entry)
				memcache.set(key_version_time, lastupdated)
				return entry, lastupdated
			else:
				return None, None
			
			
	def add_page(self, pagename, content):		
		version = self.page_exists(pagename)
		if version is None:
			newpost = WikiPage(PageName = pagename, Content = content,Version = 1)
			newpost.put()
		else:
			newpage = WikiPage(PageName = pagename, Content = content, Version = version+1)
			newpage.put()			
	
	def page_exists(self, pagename):
		pages, lastupdated = self.page_list()		
		for page in pages:
			if page.PageName == pagename:					
				return page.Version
		return None
			
			
class Trip(db.Model):
	UserId		= db.IntegerProperty(required=True)
	Title			= db.StringProperty(required=True)
	Description = db.TextProperty(required=True)
	Created 		= db.DateTimeProperty(auto_now_add = True)
	

class TripItem(db.Model):
	TripId	= db.StringProperty(required=True)	#Trip this item is associated with
	Title		= db.StringProperty(required=True)	#Name of place, event, etc
	ApiId		= db.IntegerProperty(required=True)	#Business Id (YellowApi)
	Created 	= db.DateTimeProperty(auto_now_add = True)
	#Add other properties that we would be allowed to save...

	