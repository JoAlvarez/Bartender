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
#
# Need to change this function so that it returns either the position in page after info is found, or all of page after info found
#
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

def getPages(page, catNum): #travel from cat/X/n where n  = [0,...,N]
	#find max pages to cat
	drinks = []
	maxPageFinder = getInfo(page, ['<div class="fl4"', '>','<'])
	maxPageDash = maxPageFinder.find('/')
	maxPage = int(float( maxPageFinder[maxPageDash+1:] ) )
	pageNum = 0
	#iterate through each page finding drink info
	while True:
		if pageNum >= maxPage:
			break
		else:
			print "...working on page", pageNum +1
			drinkLink = urllib2.urlopen(ROOT + '/cat/' + str(catNum)+'/'+str(pageNum + 1))
			drinkPage = drinkLink.read()
			drinks.append( getDrinkPage(drinkPage) )
			pageNum = pageNum + 1
	return drinks

def getDrinks(page): #travel through each cat, cat/n/ where n = [0,...,N]
	drink = []
	maxCat = 8
	currentCat = 0
	while True:
		if currentCat >= maxCat:
			break
		elif currentCat == 4:
			currentCat = currentCat + 1
		else:
			print "working on cat: ", currentCat+1
			drinkLink = urllib2.urlopen(ROOT+ '/cat/' + str(currentCat + 1))
			drinkPage = drinkLink.read()
			drink.append( getPages(drinkPage, currentCat + 1) )
			currentCat = currentCat + 1
	return drink
	
def printInfo(mylist):
	file = open(OUTPUT, 'w')
	for itema in mylist:
		for itemb in itema:
			for itemc in itemb:
				file.write("%s\n" % itemc)
	
c = urllib2.urlopen(ROOT)
contents = c.read()
thisList = getDrinks(contents)
printInfo( thisList)
