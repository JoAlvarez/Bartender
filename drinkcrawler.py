#webcrawler to get mix drinks
import urllib2

#globals
ROOT = "http://www.drinksmixer.com"
OUTPUT = "mixes.txt"
## ----------for drink info---------------
GLASS =['div class="recipeStats"', 'title="', '"']
DESCRIP = ['div class="summary RecipeDirections"', '>','<']
INGER = ['span class="name"','.html">','<' ]
AMT = ['span class="amount"','amount">', '<']
NAME = ['class="fn recipe_title"', '>', '<']
DIRECTIONS = ['div class="RecipeDirections instructions', '">','<']
DRINKS = ['<table cellspacing="1" cellpadding="0" border="0" width="98%"><tr><td width="50%"><div class="l1a">','<a href="','"']

def getInfo(page, searchInfo): #get specific data from a drink page
	info = ''
	startLink = page.find(searchInfo[0])
	if(startLink < 0):
		return info
	startQuote = page.find(searchInfo[1], startLink)
	endQuote = page.find(searchInfo[2] , startQuote + len(searchInfo[1]))
	return page[startQuote + len(searchInfo[1]) : endQuote]
	
def getIngr(page, amount, name): #get ingrediants from drink page
	content = page
	ingr = ''
	recipe = []
	startLink = content.find(amount[0])
	while True:
		ingr = getInfo(content, AMT)
		if( ingr != ''):
			ingr = ingr + ' ' + getInfo(content, INGER)
			content = content[content.find(AMT[0]) + 1 : ]
			recipe.append(ingr)
		else:
			break
		
	return recipe
	
def getDrink(page): #get needed info from drink page
	drink = []
	drink.append(getInfo(page, NAME))
	drink.append(getInfo(page, GLASS))
	drink.append(getInfo(page, DESCRIP))
	drink.append(getIngr(page, AMT, INGER))
	drink.append(getInfo(page, DIRECTIONS))
	return drink

def getDrinkPage(page): #get drinks from a page e.g. cat/y/z
	drink = []
	tableStart = page.find(DRINKS[0]) #get to the start of the table for drinks
	tableEnd = page.find("</a><br></div></tr></table>") #know when to stop looking for drinks
	startLink = ''
	endLink = ''
	while True:
		startLink = page.find(DRINKS[1], tableStart)		
		if (startLink > tableEnd):
			break
		else:
			endLink = page.find(DRINKS[2], startLink + len(DRINKS[1]))
			drinkPage = urllib2.urlopen(ROOT + page[startLink + len(DRINKS[1]) : endLink] )
			drinkContents = drinkPage.read()
			drink.append(getDrink(drinkContents))
			tableStart = endLink
	return drink		

def getPages(page, pageNum, drinks): #travel from cat/X/n where n  = [0,...,N]
	#find max pages to cat
	maxPageFinder = getInfo(page, ['<div class="fl4"', '>','<'])
	maxPageDash = maxPageFinder.find('/')
	maxPage = maxPageFinder[maxPageDash+1:]
	#iterate through each page finding drink info
	if pageNum > int(float(maxPage)):
		return
	else:
		drinks.append(getDrinkPage(page))
	    #get new page
		
		getPages(newpage, pageNum+1, drinks)

def getDrinks(page): #travel through each cat, cat/n/ where n = [0,...,N]
	drink = []
	
def printInfo(mylist):
	file = open(OUTPUT, 'w')
	for item in mylist:
		 file.write("%s\n" % item)
	
c = urllib2.urlopen('http://www.drinksmixer.com/cat/1/2/')
contents = c.read()
thisList = getPages(contents)
#printInfo( thisList)
