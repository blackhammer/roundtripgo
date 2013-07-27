# Create your views here.
import json as simplejson
import urllib
from django.template import Context, loader
from django.http import HttpResponse
from YellowAPI import YellowAPI

yellowAPI = YellowAPI('TODO: Insert your API key here', 'PythonLesPacApp', True, 'JSON', [])

def index(request):
	t = loader.get_template('index.html')
	c = Context()
	
	return HttpResponse(t.render(c))

def search(request):
	# Get the field value from the search form
	what = request.GET.get('what', '')
	where = request.GET.get('where', '')
	
	# Fetch search results
	result = yellowAPI.find_business(what, where, 1, 40, '', 'en')
	
	t = loader.get_template('listing.html')
	c = Context({
		'result': simplejson.loads(result)	# Parse the result as a JSON Object
	})
	
	return HttpResponse(t.render(c))
	
def details(request, id):
	prov = request.GET.get('prov', '')
	city = request.GET.get('city', '')
	bus_name = request.GET.get('bus_name', '')

	# Fetch merchant details
	result = yellowAPI.get_business_details(prov, city, bus_name, id, 'en')
	
	t = loader.get_template('details.html')
	c = Context({
		'result': simplejson.loads(result)	# Parse the result as a JSON Object
	})
	
	return HttpResponse(t.render(c))

def urlencode(data):
   return urllib.urlencode(data)