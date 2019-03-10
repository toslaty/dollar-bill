from sqlalchemy import create_engine
from sqlalchemy import VARCHAR
from sqlalchemy_utils import database_exists, create_database
import pandas as pa



engine = create_engine('mysql://phpmyadmin:Datenbanken@localhost/company_fundamentals', pool_recycle= 3600) 
engine2 = create_engine('mysql://phpmyadmin:Datenbanken@localhost/company_daily', pool_recycle= 3600)


def frame_to_db(frame,symbol):

	if not database_exists(engine.url):
			create_database(engine.url, encoding= 'utf8')
		

	connection = engine.connect()

	frame.reset_index(inplace = True)
	frame.to_sql(symbol, con = engine, if_exists='replace', index=True, index_label = 'None')


def prices_to_db(frame, symbol):
	
	if not database_exists(engine2.url):
		create_database(engine2.url, encoding = 'utf8')

	connection = engine2.connect()

	frame.reset_index(inplace =True)
	frame.to_sql(symbol, con = engine2, if_exists='replace', index = True)


#def get_funda(sym):
	#frame = pa.Dataframe()

#def get_prices(sym):  

