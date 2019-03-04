# -*- coding: utf-8 -*-
import pandas as pd
import settings
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import pdb
import html
import matplotlib.pyplot as plt
import re
from flair.data import Sentence
from flair.models import SequenceTagger
'''
Read data from sql table directly using read_sql_query. As it prevents errors in data
'''
engine=create_engine(URL(**settings.DATABASE),connect_args={'charset':'utf8'})
data=pd.read_sql_query("SELECT * from claim cl inner join claim_review cr on cl.claimID=cr.claimID where fact_checkerID<6",con=engine)
data['claim_text']=data['claim_text'].apply(html.unescape)
data['claim_text']=data['claim_text'].apply(lambda x: x.replace("’","'").replace("‘","'").replace("”","'").replace("“","'").replace("\"","'").replace("—","-").replace("–","-").replace("…"," ").replace("\xa0"," ").replace("","").replace("[","").replace("]",""))
'''
Dropping dirty rows
'''
drop_rows = [i for i, x in enumerate(data['claim_text'].apply(lambda x:len(x.split())).tolist()) if x==1]
data=data.drop(index=drop_rows)
'''
Function to replace Quotes and wrap all string uniformly. Also clean html tags
'''
def cleanre(row):
	s=row['claim_text']
	'''
	re to wrap with double quotes uniformly
	'''
	if not re.search(r"^\".*\"$",s):#if already wrapped by double quotes, ignore
		if re.search(r"^'(.*)'$",s):#if wrapped by single quotes replace with double quotes
			s=re.sub(r"^'(.*)'$",r'"\1"',s)
		else:
			s=re.sub(r"(.*)",r'"\1"',s)#else if totally unwrapped wrap with double quotes
	clean=re.compile(r"<.*?>")#clean html tags
	s=re.sub(clean,"",s)
	# while True:
	# 	if not re.search(r"(.*\s'.*\w)(')(\w.*)",s):
	# 		break
	# 	else:
	# 		clean2=re.compile(r"(.*\s'.*\w)(')(\w.*)")
	# 		s=re.sub(clean2,r"\1\3",s)
	row['claim_text']=s
	return row
data=data.apply(cleanre,axis=1)
data.to_csv("claimreview_db.csv",header=True)
data.to_csv("claimtext_db.txt",index=None,header=None,columns=["claim_text"])







# def is_ascii(s):
# 	cdict={}
# 	for c in s:
# 		if ord(c)>128:
# 			try:
# 				cdict[c]+=1
# 			except KeyError:
# 				cdict[c]=1
# 	return cdict

# f=open("in.txt","r")
# print(is_ascii(f.read()))

