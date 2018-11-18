#! /usr/bin/env python3
# coding: utf-8

from lxml.html import fromstring
import requests
from itertools import cycle
import traceback
from bs4 import BeautifulSoup
import json
import pickle
import csv


# get a set of proxies
def get_proxies():
	url = 'https://free-proxy-list.net/'
	response = requests.get(url)
	#add a try expect in case I cannot connect to the server
	parser = fromstring(response.text)
	proxies = set()
	print(type(proxies))
	for i in parser.xpath('//tbody/tr')[:20]:
		if i.xpath('.//td[7][contains(text(),"yes")]'):
			proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
			proxies.add(proxy)
	return proxies

# Test the different proxies
def selectWorkingProxies(proxies):
	proxy_pool = cycle(proxies)
	url = 'https://httpbin.org/ip'
	proxieslist = set()
	for i in range(0,len(proxies)):
		proxy = next(proxy_pool)
		# print('type(proxy): ',type(proxy))
		print(proxy)
		print("Request #%d"%i)
		try:
			response = requests.get(url,proxies={"http": proxy, "https": proxy})
			print(response.json())
			proxieslist.add(proxy)
		except:
			#Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
			#We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
			print("Skipping. Connnection error")
	return proxieslist

	# i=0
	# while len(proxies) > 0:
	# 	proxy = proxies[0]
	# 	print("Request #%d"%i)
	# 	i+=1
	# 	try:
	# 		response = requests.get(url,proxies={"http": proxy, "https": proxy})
	# 		print(response.json())
	# 		del proxies[0]
	# 		return proxy #, proxies
	# 	except:
	# 		#Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
	# 		#We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
	# 		print("Skipping. Connnection error")
	# 		del proxies[0]





def readFile(fileName): #extract a list from a json file -- use to create a list of category and licenses
	with open(fileName,'r') as file:
		data = json.load(file)
	return data

# create a dictionnary of the research Urls links for Amazon --- Have to be changed for another website
def createUrls(categories, licenses): 
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


def exportInJson(fileName, data): # export the data in a json file
	with open(fileName,'w') as f:
		f.write(json.dumps(data))

# export the data in a json file
def saveUrlDictionary(fileName, data): 
	with open(fileName, 'wb') as f:
		pickle.dump(data, f)

# Get the data back
def importUrlDictionary(fileName):
	with open(fileName, 'rb') as f:
		data = pickle.load(f)
	return data

# Send a request to the website and collect the data needed
def collectWebData(url):
	response = requests.get(url).text #Add the proxy here: proxies={"http": proxy, "https": proxy}
	soup = BeautifulSoup(response,'html.parser')
	topDynamicContent = soup.find(id='topDynamicContent')
	if len(topDynamicContent.contents) == 1: #If the lenght of the id top dynamic contempt is equal to 1 => the research do not contain anything
		print('no result found')
		return 0
	elif len(topDynamicContent.contents) > 1: #If this tag contain more thant one thing => the research have results
		webData = soup.find(id='s-result-count')
		return webData.contents[0]

# transform the text got on the website into a number
def cleanText(text): 
	if type(text) is int:
		return text
	else:
		numberList = [s for s in text.split() if s.isdigit()] #create a list of strings of the digit contained into the text
		return int(''.join(numberList)) #add the digit together and transgorm it into an int





proxies = get_proxies()
print(proxies)
for i in range(1,10):
	print('#####Boucle: ',i)
	workingproxies = selectWorkingProxies(proxies)
	print(workingproxies)
	workingproxies.clear()

# proxies = get_proxies()
# print('type(proxies): ',type(proxies))
# print(proxies)
# proxy_pool = cycle(proxies)
# print('type(proxy_pool): ', type(proxy_pool))
# print('proxy_pool: ', proxy_pool)

# url = 'https://httpbin.org/ip'
# for i in range(0,len(proxies)):
# 	proxy = next(proxy_pool)
# 	print('type(proxy): ',type(proxy))
# 	print(proxy)
# 	print("Request #%d"%i)
# 	try:
# 		response = requests.get(url,proxies={"http": proxy, "https": proxy})
# 		print(response.json())
# 	except:
# 		#Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
# 		#We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
# 		print("Skipping. Connnection error")


# if __name__=='__main__':
# 	urls = importUrlDictionary('urllist.binary') # import the list of urls
# 	result = []
# 	for catLic,url in urls.items():
# 		refNumber = cleanText(collectWebData(url))
# 		result = []
# 		result.extend(catLic)
# 		result.append(url)
# 		result.append(str(refNumber))
# 		with open('results.csv','a',newline='') as f:
# 			writer = csv.writer(f, delimiter=',')
# 			writer.writerow(result)


##Exception raisong during a request
# try:
# 	r = requests.get('http://www.google.com/nothere')
# 	r.raise_for_status()
# except requests.exceptions.HTTPError as err:
# 	print(err)
# 	print('change IP')
# except requests.exceptions.RequestException as err:
# 	print(err)
# 	print('pass to another url')

