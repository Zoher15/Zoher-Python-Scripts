import extruct
import requests
from pprint import pprint
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
# import settings
claimdf=pd.DataFrame()
#r=requests.get('https://www.snopes.com/julia-roberts-say-michelle-obama-isnt-fit-clean-melania-trumps-toilet/')
r=requests.get('http://www.politifact.com/truth-o-meter/article/2017/aug/22/fact-checking-president-donald-trumps-campaign-ral/')
data=extruct.extract(r.text,r.url)['microdata']
selected=[properties for properties in data if properties['type']=='http://schema.org/ClaimReview']
#pprint(selected)
claimdict=[]
for elements in selected:
	claimdict.append(elements['properties'])

def dict_to_series(dictt):
	for key in dictt:
		if type(dictt[key])==list:
			dictt[key]=dictt[key][0]
	return pd.io.json.json_normalize(dictt)

claimdf=claimdf.append(pd.concat(map(dict_to_series,claimdict),ignore_index=True),ignore_index=True)
r=requests.get('https://www.snopes.com/julia-roberts-say-michelle-obama-isnt-fit-clean-melania-trumps-toilet/')
data=extruct.extract(r.text,r.url)['microdata']
selected=[properties for properties in data if properties['type']=='http://schema.org/ClaimReview']
claimdict=[]
for elements in selected:
	claimdict.append(elements['properties'])
claimdf=claimdf.append(pd.concat(map(dict_to_series,claimdict),ignore_index=True),ignore_index=True)
# engine=create_engine(URL(**settings.DATABASE),connect_args={'charset':'utf8'})	
# claimdf.to_sql('claim',engine, if_exists='replace')
claimdf.to_csv('yo.csv', encoding='utf-8')