import os
import requests
import datetime as dt
from datetime import datetime
import pandas as pa
import pandas_datareader as web 
import bs4 as bs
import re
import string
from dbase import *
from knoema_req import *


def scrape_wiki_sp500():

	req = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

	soup = bs.BeautifulSoup(req.text, 'html5lib')
	table = soup.find('table', {'class' : 'wikitable sortable'})
	symbols = []

	for row in table.findAll('tr')[1:] :
		symbol = row.findAll('td')[1].text
		symbols.append(symbol)

	return symbols


def get_newest():

	companies = scrape_wiki_sp500()
	for i in companies:
		print('tryin '+i)
		get_special(i)
		print(i)


def table_stuff(req):

	supp = bs.BeautifulSoup(req.text, 'html5lib')
	tables = supp.findAll('table')

	outputs = []

	for table in tables:
		for row in table.findAll('tr'):
			for cell in row.findAll('td'):
				if(len(row) < 2):
					pass
				else:
					first = cell.text
					outputs.append(first)

	return outputs				


def check_chars(list):

	numbers =[]
	regex = re.compile('[a-z]+')
	for i in list[5::]:
		if not(regex.search(i)):
			numbers.append(i)	

	return numbers		


def data_to_frame(cols, nlist,clist):

	frame = pa.DataFrame(index = clist[5::5], columns = cols)

	for x in range(4):
		frame[cols[x]] = pa.Series(nlist[x::4], index = clist[5::5])

	return frame

# Splits the string so we get the columns for the fundamental data
def splitter(rev):

	cols = []

	if(len(rev) < 5):
		for w in rev:
			wort = w.split('/')
			print(wort)
			cols.append(wort[2])
	else:
		print('REWORK FOR ONLY 3 COLUMNS')		
	print(rev)
	return cols

#kills comma in number cats everything to int64 and times 1000 because numbers o yahoo in thousands
def real_numbers(alldata):

	for col in alldata.columns[1:]:

		alldata[col] = alldata[col].replace(',' , '', regex = True)
		alldata[col] = alldata[col].astype('int64', errors = 'ignore')
		alldata[col] = alldata[col] * 1000

	return alldata


# Gets the fundamental data for the given symbol from yahoo with the hardcoded addresses below
def get_special(symbol):

	symbol = symbol

	url = 'https://finance.yahoo.com/quote/'+symbol+'/key-statistics?p='+symbol
	url2 = 'https://finance.yahoo.com/quote/'+symbol+'/financials?p='+symbol
	url3 = 'https://finance.yahoo.com/quote/'+symbol+'/balance-sheet?p='+symbol
	url4 = 'https://finance.yahoo.com/quote/'+symbol+'/cash-flow?p='+symbol

	x = requests.get(url)
	y = requests.get(url2)
	z = requests.get(url3)
	c = requests.get(url4)

	stats = table_stuff(x)
	revenue = table_stuff(y)
	balance = table_stuff(z)
	cflow = table_stuff(c)

	if(len(revenue) > 5):

		cols = splitter(revenue[1:5]) 

		rnumbers = check_chars(revenue)
		bnumbers = check_chars(balance)
		cfnumbers= check_chars(cflow)

		sframe = pa.Series(stats[1::2],index = [stats[::2]])

		rframe = data_to_frame(cols, rnumbers,revenue)
		bframe = data_to_frame(cols, bnumbers, balance)
		cfframe = data_to_frame(cols, cfnumbers, cflow)

		frames = [rframe,bframe,cfframe]

		alldata = pa.concat(frames, axis = 0)
		alldata.reset_index(inplace = True)
		alldata.replace('-', 0,inplace = True)
		real_numbers(alldata)
		#alldata = alldata.set_index('index')

		frame_to_db(alldata, symbol)

	else:

		print('No data available\n')
		empty = pa.DataFrame(columns = [0,0,0])
		frame_to_db(empty, symbol)


#gets the price from knoema for sym
def git_prices(sym, start, end):

	df = get_stock_us(sym,start,end)

	cols1 = df.columns.names
	cols1 = cols1[:4]

	df.columns = ['Close', 'High', 'Low', 'Open', 'Volume']

	prices_to_db(df ,sym)



	

