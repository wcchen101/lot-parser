import os
from bs4 import BeautifulSoup

targetFolder = 'data' + '/' + '2015-03-18'
htmlFiles, artistAll, targetObj = [], [], {}
for subFile in os.listdir(targetFolder):
	htmlFiles.append(subFile)

for subFile in htmlFiles:
	f = open(targetFolder+ '/' + subFile, 'r')
	soup = BeautifulSoup(f, 'lxml')
	for titleElement in soup.find_all('title'):
		rawTitle = titleElement.text
		refinedTitle = rawTitle.replace('\n', ' ')
		refinedTitle = refinedTitle.strip()
		breakIndex = refinedTitle.index(':')
		title = refinedTitle[:breakIndex]
		work = refinedTitle[breakIndex + 1:].strip()
		targetObj = {
			'artist': title,
			'work': [work]
		}
		artistAll.append(targetObj)
	f.close()

print(artistAll)