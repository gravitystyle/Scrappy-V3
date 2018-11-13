#! /usr/bin/env python3
# coding: utf-8

from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
from bs4 import BeautifulSoup
import json

def get_proxies():
	url = 'https://free-proxy-list.net/'
	response = requests.get(url)
	parser = fromstring(response.text)
	proxies = set()
	for i in parser.xpath('//tbody/tr')[:10]:
		if i.xpath('.//td[7][contains(text(),"yes")]'):
			proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
			proxies.add(proxy)
	return proxies

def readFile(fileName): #extract a list from a json file -- use to create a list of category and licenses
	with open(fileName,'r') as file:
		data = json.load(file)
	return data

def createUrls(categories, licenses): # create a dictionnary of the research Urls links for Amazon --- Have to be changed for another website
	baseUrl = "https://www.amazon.fr/s/ref=nb_sb_noss_1?__mk_fr_FR=ÅMÅŽÕÑ&url=search-alias%3Daps&field-keywords=" #This is the base use for the Amazon Url
	urls = {}
	wordsToSearch = []
	catLic = []
	for category in categories:
		for license in licenses:
			wordsToSearch = [] #Reinitialize the words to search
			categorySplited = category.lower().split() #Create a list of words from the string of the category
			licenseSplited = license.lower().split() #Create a list of words from the string of the license
			wordsToSearch.extend(categorySplited) #add the list of category words to the words to search
			wordsToSearch.extend(licenseSplited) #add the list of license words to the words to search

			urls[category,license] = baseUrl + "+".join(wordsToSearch)

	return urls



categories = readFile('categories.json')
licenses = readFile('licenses.json')
urls = createUrls(categories,licenses)



# proxies = get_proxies()
# print(proxies)
# proxy_pool = cycle(proxies)


# url = 'https://httpbin.org/ip'
# for i in range(0,len(proxies)):
# 	proxy = next(proxy_pool)
# 	print(proxy)
# 	print("Request #%d"%i)
# 	try:
# 		response = requests.get(url,proxies={"http": proxy, "https": proxy})
# 		print(response.json())
# 	except:
# 		#Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
# 		#We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
# 		print("Skipping. Connnection error")

