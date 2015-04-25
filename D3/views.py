# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import pdb
import urllib
import json

def home(request):
	return render(request, 'D3/home.html', {})

def d3_visual(request):
	url = "http://localhost:8983/solr/collection1/select?q=*&rows=2&wt=json&indent=true"
	response = urllib.urlopen(url);
	data = json.loads(response.read())
	print data
	return render(request, 'D3/d3_visual.html', {'data':data})

def banana_visual(request):
	return render(request, 'D3/banana_visual.html', {})

def facetview_visual(request):
	return render(request, 'D3/facetview_visual.html', {})
