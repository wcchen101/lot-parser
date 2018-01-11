import os
from bs4 import BeautifulSoup
from lxml import html

targetFolder = 'data' +'/' + '2015-03-18'
htmlFiles, artistAll, targetObj = [], [], {}
for subFile in os.listdir(targetFolder):
	htmlFiles.append(subFile)

for subFile in htmlFiles:
	f = open(targetFolder+ '/' + subFile, 'r')
	soup = BeautifulSoup(f, 'lxml')
	divElementArr = []
	worksObj = {
		'title': '',
		'price': 0
	}
	targetObj = {
		'artist': '',
		'works': worksObj
	}
	for titleElement in soup.find_all('title'):
		rawTitle = titleElement.text
		refinedTitle = rawTitle.replace('\n', ' ')
		refinedTitle = refinedTitle.strip()
		breakIndex = refinedTitle.index(':')
		title = refinedTitle[:breakIndex]
		work = refinedTitle[breakIndex + 1:].strip()
		worksObj = {
			'title': work,
			'price': 0
		}
		targetObj = {
			'artist': title,
			'works': worksObj
		}
		artistAll.append(targetObj)

	price = None
	refinedDivArr = []
	for divElement in soup.find_all('div'):
		rawDiv = divElement.text
		refinedDiv = rawDiv.replace('\n', ' ')
		refinedDivArr.append(refinedDiv.strip())

	price = refinedDivArr[1]
	worksObj['price'] = price.strip()
	targetObj['works'] = [worksObj]

	artistAll.append(targetObj)
	f.close()
print(artistAll)