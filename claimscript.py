#!/usr/bin/python
# -*- coding: utf-8 -*-
# filename="claims by factchecker less than 6.txt"
# file=open(filename,"r").readlines()
# print(len(file))
import pandas as pd
import settings
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import html
import requests
import numpy as np
import re
import pdb

def titleornot(sentence):
	title_regex=re.compile(r'((\ ([.,\/#!$%\^&\*;:{}=\-_`~()])*)[A-Z])')
	hits=len(re.findall(title_regex,sentence))
	splitlength=float(len(sentence.split()))
	if hits>0:
		return hits/splitlength
	else:
		return 0

def true_case(sentence):
	#activate stanford server first using this in the corenlp directory: java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -annotators "tokenize,ssplit,truecase" -truecase.overwriteText -port 9000 -timeout 30000
	r=requests.post('http://localhost:9000',data=sentence.encode('utf-8')).json()['sentences'][0]['tokens']
	r=sorted(r,key=lambda k:k['index'])
	#combining the json from the post request
	converted_sent="".join([rs['truecaseText']+rs['after'] for rs in r])
	return converted_sent

engine=create_engine(URL(**settings.DATABASE),connect_args={'charset':'utf8'})
data=pd.read_sql_query('SELECT * from claim2 cl inner join claim_review2 cr on cl.claimID=cr.claimID where fact_checkerID<6',con=engine)
##Dropping non-str rows
filter=list(map(lambda x:type(x)!=str,data['claim_text']))
data.drop(data[filter].index,inplace=True)
#dropping fields with duplicate over claimID,claim_text,fact_checkerID
data.drop_duplicates(subset=['claimID','claim_text','fact_checkerID'],inplace=True)
#selecting claims that are titled in their claim_text
titled_claims_index=[i for i in list(data.index) if titleornot(data.loc[i,'claim_text'])>0.55]
#converting to truecase
data.loc[titled_claims_index,'claim_text']=data.loc[titled_claims_index,'claim_text'].apply(true_case)
print(len(data))
data.to_csv('claimreviews_db2.csv',encoding="utf-8")