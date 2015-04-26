# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import pdb
import urllib
import json
from django.utils.safestring import SafeString

def home(request):
	return render(request, 'D3/home.html', {})

def d3_visual(request):
	url = "http://localhost:8983/solr/collection1/select?q=*&rows=2&wt=json&indent=true"
	response = urllib.urlopen(url);
	data = json.loads(response.read())
	#print json.dumps(data['response'], indent=4)
	#return render(request, 'D3/d3_visual.html', {'data':SafeString(data)})
	response = data["response"]
	docs = response["docs"]
	for each in docs:
		print each["id"]
		print each["title"][0]
		print each["content_type"][0]
		#print each["content"]
	return HttpResponse(json.dumps(docs), content_type="application/json")

def banana_visual(request):
	return render(request, 'D3/banana_visual.html', {})

def facetview_visual(request):
	return render(request, 'D3/facetview_visual.html', {})
