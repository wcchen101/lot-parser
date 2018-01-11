import os
from bs4 import BeautifulSoup
from lxml import html

targetFolder = '2017-12-20'
def parseHTML():
	htmlFiles, artistAll, targetObj = [], {}, {}
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
			'works': None
		}
		artist = ''
		for titleElement in soup.find_all('title'):
			rawTitle = titleElement.text
			refinedTitle = rawTitle.replace('\n', ' ')
			refinedTitle = refinedTitle.strip()
			breakIndex = refinedTitle.index(':')
			artist = refinedTitle[:breakIndex]
			work = refinedTitle[breakIndex + 1:].strip()
			targetObj = {
				'artist': artist,
				'works': None
			}
			worksObj = {
				'title': work,
				'price': 0
			}

		price = None
		refinedSpanArr = []
		for spanElement in soup.find_all('span'):
			rawSpan = spanElement.text
			refinedSpan = rawSpan.replace('\n', ' ')
			refinedSpanArr.append(refinedSpan.strip())

		currency = refinedSpanArr[0].upper()
		price = refinedSpanArr[1]
		worksObj['currency'] = currency
		if worksObj['currency'] == 'GBP':
			priceNum = str(round(parseStrNumToNum(price) * 1.34, 2))
			floatBreakIndex = priceNum.index('.')
			worksObj['price'] = parseNumToWrittenNum(priceNum[:floatBreakIndex]) + '.' + priceNum[floatBreakIndex + 1:]
			worksObj['currency'] = 'USD'
		else:
			worksObj['price'] = price
		targetObj['works'] = [worksObj]

		breakIdnex = 0
		try:
			if artist.index('(') and artist.index('(') != 0:
				breakIndex = artist.index('(')
				artist = artist[:breakIndex].strip()

		except ValueError:
			print('There is a ValueError')

		if artist in artistAll:
			artistAll[artist]['works'].append(worksObj)
		else:
			artistAll[artist] = targetObj

		f.close()
	resultObj = calculateArtistValue(artistAll)
	print(resultObj)

def calculateArtistValue(artistAllObj):
	resultObj = artistAllObj
	for artist in artistAllObj.keys():
		artistTotalValue = 0 
		artistObj = artistAllObj[artist]
		for work in artistObj['works']:
			priceNum = parseStrNumToNum(work['price'])

			artistTotalValue += priceNum
		print(artistTotalValue)
		artistTotalValue = str(artistTotalValue)
		floatBreakIndex = artistTotalValue.index('.')
		artistTotalValue = parseNumToWrittenNum(artistTotalValue[:floatBreakIndex]) + '.' + artistTotalValue[floatBreakIndex + 1:]
		resultObj[artist]['totalValue'] = artistTotalValue
	return resultObj


def parseStrNumToNum(strNum):
	result = []
	for num in strNum:
		if num == ',':
			continue
		result.append(num)
	resultNum = ''.join(result)
	return float(resultNum)

def parseNumToWrittenNum(num):
	result = []
	num = num[::-1] #reverse
	count = 0
	for n in num:
		if count != 0 and count % 3 == 0:
			result.append(',')
		result.append(n)
		count += 1

	resultStr = ''.join(result)
	return resultStr[::-1] #reverse again

if __name__ == '__main__':
	parseHTML()