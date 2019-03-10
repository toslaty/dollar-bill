import pandas as pa
import math
import datetime as dt 
from datetime import datetime


def corr_stocks(stocka,stockb,start,end):
	
	name1 = stocka	
	name2 = stockb

	startd = datetime.strptime(start,"%Y-%m-%d")
	endd = datetime.strptime(end, "%Y-%m-%d")

	fr1 = pa.read_csv(stocka+'.csv',parse_dates= True, index_col = 0)
	fr1.drop(['Volume', 'Close', 'High', 'Low', 'Open'], 1, inplace = True)
	fr1.rename(columns={"Adj Close" : name1}, inplace = True)
	
	fr2 = pa.read_csv(stockb+'.csv', parse_dates = True, index_col = 0)
	fr2.drop(['Volume', 'Close', 'High', 'Low', 'Open'], 1, inplace = True)
	fr2.rename(columns={"Adj Close" : name2}, inplace = True)

	rng1 = fr1.loc[startd : endd]
	rng2 = fr2.loc[startd : endd]

	ind = pa.concat([rng1,rng2], axis = 1)


	mathemagic(ind)


def mathemagic(ind):
	
	summ1 = ind[ind.columns[0]].sum()

	summ2 = ind[ind.columns[1]].sum(skipna = True)

	summ3 = (ind[ind.columns[0]] * ind[ind.columns[1]]).sum()

	summ4 = (ind[ind.columns[0]] * ind[ind.columns[0]]).sum()

	summ5 = (ind[ind.columns[1]] * ind[ind.columns[1]]).sum()

	t = float(len(ind.index))

	corr1 = t * summ3 - (summ1 * summ2) 

	corr2 = math.sqrt((t * summ4 - math.pow(summ1,2)) *(t * summ5 -math.pow(summ2,2)))

	correlation = corr1 / corr2

	print(correlation)