import math
import pandas as pa
from dbase import *


def get_funda_ratios(sym):
	
	frame = get_funda(sym)
	frame  = frame.drop(columns = 'id')

	ind = ['current_ratio','acid-test_ratio','cash_ratio','operating_cash_flow',
	'debt_ratio','debt_to_equity','interest_coverage_ratio','gross_profit_margin',
	'net_profit_margin', 'operating_profit_margin','return_on_equity','return_on_assets']


	r_frame = pa.DataFrame(index = ind, columns = frame.columns)

	r_frame.loc['current_ratio'] = frame.iloc[28] / frame.iloc[40]

	r_frame.loc['acid-test_ratio'] = frame.iloc[28] - frame.iloc[26] / frame.iloc[40]

	r_frame.loc['cash_ratio'] = frame.iloc[23] / frame.iloc[40]

	r_frame.loc['operating_cash_flow'] = frame.iloc[64] / frame.iloc[40]


	r_frame.loc['debt_ratio'] = frame.iloc[46] / frame.iloc[36]

	r_frame.loc['debt_to_equity'] = frame.iloc[46] / frame.iloc[55]

	r_frame.loc['interest_coverage_ratio'] = frame.iloc[8] / frame.iloc[11]


	#r_frame.loc['gross_profit_margin'] = frame.iloc[20] / frame.iloc[36]

	#r_frame.loc['net_profit_margin'] = frame.iloc[] / frame.iloc[]

	#r_frame.loc['operating_profit_margin'] = frame.iloc[] / frame.iloc[]

	#r_frame.loc['return_on_equity'] = frame.iloc[] / frame.iloc[]

	#r_frame.loc['return_on_assets'] = frame.iloc[] / frame.iloc[]


	#r_frame.loc[''] = frame.iloc[] / frame.iloc[]

	#r_frame.loc[''] = frame.iloc[]

	print(r_frame)

	#fundas_to_db(r_frame, sym)

