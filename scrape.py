import urllib2
import requests
from bs4 import BeautifulSoup
import json

class Recipe(object):
	title = ''
	information = list()
	ingredientList = list()
	instructionList = list()

	def __init__ (self, ttle, info, ingreds, instructs):
		self.title = ttle
		self.information = info
		self.ingredientList = ingreds
		self.instructionList = instructs

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Recipe): 
            return { 'Title' : obj.title, 
            'Information' : obj.information, 
            'Ingredients' : obj.ingredientList,
            'Instructions' : obj.instructionList }
        return json.JSONEncoder.default(self, obj)

#url = raw_input('Enter url: ')
url = 'http://www.myrecipes.com/recipe/pork-peanut-stir-fry'
sauce = requests.get(url)
html = sauce.content
soup = BeautifulSoup(html, 'lxml')

rawTitle = soup.title.text
title = ''
for x in xrange(0,len(rawTitle) - 1):
	if rawTitle[x] == '|':
		break
	else:
		title += rawTitle[x]
# print title + '\n'

information = list()
for spans in soup.find_all('span', class_='recipe-meta__text'):
	information.append(spans.text)
# for info in information:
# 	print info

divList = soup.find('div', attrs={'class':'recipe-list titled-list'})
listIngred = list()
for divItem in divList.find_all('li'):
	listIngred.append(divItem.text.strip())

# print '\nIngredients:'

# for listItem in listIngred:
# 	print '\t' + listItem

olList = soup.find('ol', attrs={'class': 'recipe-instructions__list custom-list custom-list--lg custom-list--branded custom-list--serif'})
listIndstructions = list()
for olItem in olList.find_all('p'):
	listIndstructions.append(olItem.text.strip())

# print '\nIntructions:'
# for instruction in listIndstructions:
# 	print instruction + '\n'


recipe = Recipe(title, information, listIngred, listIndstructions)
print json.dumps(recipe, cls=MyEncoder)
print 'Completed.'