# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import SafeString
from random import randint
import pdb
import urllib
import json
import csv
import re

stopwords = ['var','fasting','id','log','java','nov','takes','stop',
  'access','tab','please','contact','notices','tab2','item','name','help',
  'wkt','logging','images','sd','using','null', 'a', 'about', 'above', 
  'across', 'after', 'again', 'against', 'all', 'almost', 'alone', 'along', 
  'already', 'also', 'although', 'always', 'among', 'an', 'and', 'another', 
  'any', 'anybody', 'anyone', 'anything', 'anywhere', 'are', 'area', 'areas', 
  'around', 'as', 'ask', 'asked', 'asking', 'asks', 'at', 'away', 'b', 'back', 
  'backed', 'backing', 'backs', 'be', 'became', 'because', 'become', 'becomes',
  'been', 'before', 'began', 'behind', 'being', 'beings', 'best', 'better', 
  'between', 'big', 'both', 'but', 'by', 'c', 'came', 'can', 'cannot', 'case',
  'cases', 'certain', 'certainly', 'clear', 'clearly', 'come', 'could', 'd', 
  'did', 'differ', 'different', 'differently', 'do', 'does', 'done', 'down', 
  'down', 'downed', 'downing', 'downs', 'during', 'e', 'each', 'early', 
  'either', 'end', 'ended', 'ending', 'ends', 'enough', 'even', 'evenly', 
  'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'f', 
  'face', 'faces', 'fact', 'facts', 'far', 'felt', 'few', 'find', 'finds', 
  'first', 'for', 'four', 'from', 'full', 'fully', 'further', 'furthered', 
  'furthering', 'furthers', 'g', 'gave', 'general', 'generally', 'get', 
  'gets', 'give', 'given', 'gives', 'go', 'going', 'good', 'goods', 'got', 
  'great', 'greater', 'greatest', 'group', 'grouped', 'grouping', 'groups', 
  'h', 'had', 'has', 'have', 'having', 'he', 'her', 'here', 'herself', 'high', 
  'high', 'high', 'higher', 'highest', 'him', 'himself', 'his', 'how', 
  'however', 'i', 'if', 'important', 'in', 'interest', 'interested', 
  'interesting', 'interests', 'into', 'is', 'it', 'its', 'itself', 'j', 
  'just', 'k', 'keep', 'keeps', 'kind', 'knew', 'know', 'known', 'knows', 
  'l', 'large', 'largely', 'last', 'later', 'latest', 'least', 'less', 'let', 
  'lets', 'like', 'likely', 'long', 'longer', 'longest', 'm', 'made', 'make', 
  'making', 'man', 'many', 'may', 'me', 'member', 'members', 'men', 'might', 
  'more', 'most', 'mostly', 'mr', 'mrs', 'much', 'must', 'my', 'myself', 'n', 
  'necessary', 'need', 'needed', 'needing', 'needs', 'never', 'new', 'new', 
  'newer', 'newest', 'next', 'no', 'nobody', 'non', 'noone', 'not', 'nothing', 
  'now', 'nowhere', 'number', 'numbers', 'o', 'of', 'off', 'often', 'old', 
  'older', 'oldest', 'on', 'once', 'one', 'only', 'open', 'opened', 'opening', 
  'opens', 'or', 'order', 'ordered', 'ordering', 'orders', 'other', 'others', 
  'our', 'out', 'over', 'p', 'part', 'parted', 'parting', 'parts', 'per', 
  'perhaps', 'place', 'places', 'point', 'pointed', 'pointing', 'points', 
  'possible', 'present', 'presented', 'presenting', 'presents', 'problem', 
  'problems', 'put', 'puts', 'q', 'quite', 'r', 'rather', 'really', 'right', 
  'right', 'room', 'rooms', 's', 'said', 'same', 'saw', 'say', 'says', 
  'second', 'seconds', 'see', 'seem', 'seemed', 'seeming', 'seems', 'sees', 
  'several', 'shall', 'she', 'should', 'show', 'showed', 'showing', 'shows', 
  'side', 'sides', 'since', 'small', 'smaller', 'smallest', 'so', 'some',
  'somebody', 'someone', 'something', 'somewhere', 'state', 'states', 
  'still', 'still', 'such', 'sure', 't', 'take', 'taken', 'than', 'that', 
  'the', 'their', 'them', 'then', 'there', 'therefore', 'these', 'they', 
  'thing', 'things', 'think', 'thinks', 'this', 'those', 'though', 'thought', 
  'thoughts', 'three', 'through', 'thus', 'to', 'today', 'together', 'too', 
  'took', 'toward', 'turn', 'turned', 'turning', 'turns', 'two', 'u', 'under', 
  'until', 'up', 'upon', 'us', 'use', 'used', 'uses', 'v', 'very', 'w', 'want', 
  'wanted', 'wanting', 'wants', 'was', 'way', 'ways', 'we', 'well', 'wells', 
  'went', 'were', 'what', 'when', 'where', 'whether', 'which', 'while', 'who', 
  'whole', 'whose', 'why', 'will', 'with', 'within', 'without', 'work', 
  'worked', 'working', 'works', 'would', 'x', 'y', 'year', 'years', 'yet', 
  'you', 'young', 'younger', 'youngest', 'your', 'yours', 'z']

def home(request):
	return render(request, 'D3/home.html', {})

def d3_visual(request):
	
	# Set query here
	if "query" not in request.GET:
		query = "*"
	elif request.GET["query"] == "":
		query = "*"
	else:
		query = request.GET["query"]

	query_string = ""
	for each in query:
		if each == " ":
			query_string += "+"
		else:
			query_string += each

	# Query SOLR
	url = "http://localhost:9999/solr/collection1/select?q="+query_string+"&rows=50&wt=json&indent=true"
	print "URL: ", url
	response = urllib.urlopen(url);
	data = json.loads(response.read())
	
	# never used
	response = data["response"]
	
	# docs contains the array of JSON documents
	docs = response["docs"]
	
	# used for word cloud
	wc_data = []

	# used for pie chart
	pie_dict = {}

	# used for map data
	map_data = []

	# used for time data
	time_data = []

	# points and co-ordinates
	count = 0
	point_data = []

	for each in docs:
		#if "title" not in each:
		#	continue

		ID, title, cType, cLen, content = "", "", "", 0, "" 
		date, time, lat, lon = "", "", str(randint(60,90)), str(randint(-90,180))

		if "id" in each:
			ID = each["id"]

		if "title" in each:
			title = each["title"][0]

		if "content_type" in each:
			cType = each["content_type"][0]

		if "content" in each:
			content = each["content"][0]
			cLen = len(content)
			print "CLEN:", cLen

		if "date_created" in each:
			date = each["date_created"]

		#
		# Build map data json
		#
		if "clavin_latitude" in each:
			lat_len = min(len(each["clavin_latitude"]),15)
			print "LATITUDE: ", lat_len
			for i in range(lat_len):
				lat = each["clavin_latitude"][i]
				if "clavin_longitude" in each and i<len(each["clavin_longitude"]):
					lon = each["clavin_longitude"][i]
				map_data += [{
								'ID':ID, 
								#'title':each["title"][0], 
								'cType':cType, 
								'content_length':cLen,
								'latitude':lat, 
								'longitude':lon,
								'radius': 6,
								'fillKey': 'RUS'
							}]
				point_data += [[count,lat,lon]]
				count += 1

		else:
			map_data += [{
							'ID':ID, 
							#'title':each["title"][0], 
							'cType':cType, 
							'content_length':cLen,
							'latitude':lat, 
							'longitude':lon,
							'radius': 6,
							'fillKey': 'RUS'
						}]
			
		#
		# Build time data json
		#
		if not date:
			yr = str(randint(2005,2015))
			dy = str(randint(1,30))
			mn = str(randint(1,12))
			hr = str(randint(0,24))
			mi = str(randint(0,60))
			sc = str(randint(0,60))
			date = yr+"-"+mn+"-"+dy+" "+hr+":"+mi+":"+sc

		time_data += [ {"dtg": date} ]

		# 
		# Build vocab for word cloud
		#
		each_content = []	
		if len(wc_data) < 100:
			for word in re.split(' |\r|\n|\t|/',content):
				if len(word)>1 and (65<=ord(word[0])<=90 or 97<=ord(word[0])<122) and (65<=ord(word[-2])<=90 or 97<=ord(word[-2])<122):
					if word[-1] in ['.',':',',',')']:
						word = word[:-1]
					if "," in word or "." in word or ";" in word or ":" in word or str("\\") in word:
						continue
					try:
						word = str(word.lower())
						if word in stopwords:
							continue
						if len(each_content) < 100:
							each_content.append(word)
					except:
						continue
		wc_data += each_content
		if cType in pie_dict:
			pie_dict[cType] += 1
		else:
			pie_dict[cType] = 1
	
	# creating pie chart file
	f = open("./D3/static/D3/pie.csv","w")
	f.write("age,population\n")
	for each in pie_dict:
		f.write(str(each) + "," + str(pie_dict[each]) + "\n")
	f.close()

	# Creating bar chart file
	f = open("./D3/static/D3/bar.tsv","w")
	f.write("letter\tfrequency\n")
	i = 0
	for each in docs:
		if i>100:
			break
		i += 1
		f.write( str(i) + "\t" + str(min(5500,len(each["content"][0]))) + "\n")
	f.close()

	# creating time series file
	f = open('./D3/static/D3/timeSeries.json', 'w')
	json.dump(time_data, f)
	f.close()

	# creating force graph file
	f = open('./D3/static/D3/forcegraph.json', 'w')
	f.close()

	print "WC LEN", len(wc_data)
	return HttpResponse(json.dumps({"map_data":map_data, "word_cloud_data":wc_data}), content_type="application/json")

def banana_visual(request):
	return render(request, 'D3/banana_visual.html', {})

def facetview_visual(request):
	return render(request, 'D3/facetview_visual.html', {})
