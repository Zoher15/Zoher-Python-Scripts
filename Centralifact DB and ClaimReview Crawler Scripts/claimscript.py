# filename="claims by factchecker less than 6.txt"
# file=open(filename,"r").readlines()
# print(len(file))
import pandas as pd
import settings
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

engine=create_engine(URL(**settings.DATABASE),connect_args={'charset':'utf8'})
data=pd.read_sql_query('SELECT * from claim cl inner join claim_review cr on cl.claimID=cr.claimID where fact_checkerID<6',con=engine)
# data=data['claim_text']
# print(data)
data.to_csv('claims1.txt', header=None, index=None)