from bs4 import BeautifulSoup
import requests

source=requests.get('http://www.iitg.ac.in/kvk/').text
soup=BeautifulSoup(source,'lxml')
table=soup.find('table')

for p in soup.find_all('p'):
	try:
		info = p.text
		info1=info.split('\n')
		print(info1)
	except Exception as e:
		raise e 	
# name=table.strong.text
# print(table.prettify())
# print(name)
# print(designation)