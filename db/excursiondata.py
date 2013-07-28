#!/usr/bin/env python

from google.appengine.ext import db
from google.appengine.api import memcache
from datetime import *
import logging


class ExcursionDataManager():
	def __init__(self):
		pass
		
	#Return the list of trips for a User
	def get_trip_list(self, user_id, update = False):
		key_trips = "user_trips_%s" % user_id 		
		entries = memcache.get(key_trips)
		
		if entries is not None and not update:			
			return entries
		else:			
			entries = db.GqlQuery("SELECT * from Trip WHERE UserId = :1 ORDER BY Created DESC", user_id)													
			entries = list(entries)		
			
			if len(entries) > 0:		
				memcache.set(key_trips, entries)			
								
			return entries
	
	#Get the list of trip items for a given user and trip id
	def get_trip_items(self, tripId, update = False):
		key_trips = "trip_items_%s" % (tripId)		
		
		entries = memcache.get(key_trips)
		
		if entries is not None and not update:						
			return entries
		else:			
			entries = db.GqlQuery("SELECT * from TripItem WHERE TripId = :1 ORDER BY Version DESC", trip_id)			
			entries = list(entries)
						
			if entries.count() > 0:							
				memcache.set(key_trips,entry)
												
			return entries				
			
	def add_trip(self, userid, title, description):
		if userid and title:		
			Trip(UserId = userid, Title = title, Description = description).put()					
			
	def add_trip_item(self, tripid, title, apiId):
		if	tripid and title and apiId:
			TripItem(TripId = tripid, Title = title, ApiId = apiId).put()		
			
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

	