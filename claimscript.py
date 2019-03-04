#!/usr/bin/python
# -*- coding: utf-8 -*-
# filename="claims by factchecker less than 6.txt"
# file=open(filename,"r").readlines()
# print(len(file))
import pandas as pd
import settings
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
engine=create_engine(URL(**settings.DATABASE),connect_args={'charset':'utf8'})
data=pd.read_sql_query('SELECT claim_text from claim cl inner join claim_review cr on cl.claimID=cr.claimID where fact_checkerID<6',con=engine,encoding="utf-8")
print(data.iloc[6347])
data.to_csv('claims.txt', header=None, index=None,encoding="utf-8")