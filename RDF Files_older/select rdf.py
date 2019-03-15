#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import settings
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
engine=create_engine(URL(**settings.DATABASE),connect_args={'charset':'utf8'})
data=pd.read_sql_query('SELECT cl.claimID FROM centralifact.claim cl inner join claim_entity ce on cl.claimID=ce.claimID inner join entity e on e.entityID=ce.entityID where e.entity_text like %s',con=engine,params=("Hillary Clinton%",))
print(data['claimID'])

data=pd.read_sql_query('SELECT cl.claimID FROM centralifact.claim cl inner join claim_entity ce on cl.claimID=ce.claimID inner join entity e on e.entityID=ce.entityID where e.entity_text like %s',con=engine,params=("Donald Trump%",))
print(data['claimID'])