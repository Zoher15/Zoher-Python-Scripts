import extruct
import requests
from pprint import pprint
import pandas as pd
from urlparse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import settings
claimdf=pd.DataFrame()
r=requests.get('https://www.washingtonpost.com/news-politics-sitemap.xml')
#r=requests.get('https://www.correctiv.org/echtjetzt/artikel/2018/02/21/nein-berlin-baut-keine-luxuswohnungen-fur-fluchtlinge/')
#r=requests.get('http://www.dogrulukpayi.com/iddia-kontrolu/recep-tayyip-erdogan/2002-de-yuzde-72-ye-ulasan-kamu-borc-stokunun-milli-gelire-oranini-2016-da-yuzde-28-e-kadar-dusurduk-bu-oranla-avrupa-nin-en-iyi-durumda-olan-ulkeleri-arasindayiz')
#r=requests.get('http://nieuwscheckers.nl/nieuwscheckers/man-geeft-duizenden-euros-uit-om-op-hond-te-lijken/')
#r=requests.get('http://www.weeklystandard.com/fact-check-were-all-russian-facebook-ads-purchased-only-after-the-election/article/2011726')
data=extruct.extract(r.text,r.url)
domain=urlparse(r.url).netloc.strip('www').strip('.com')
print domain
selected=[properties for properties in data['microdata'] if properties['type']=='http://schema.org/ClaimReview']
if selected:
	mode='micro'
else:
	#If micro fails, selecting JSON
	try:
		selected=[properties for properties in data['json-ld'] if properties['@type']=='ClaimReview']
	except KeyError:
		selected=[properties for properties in data['json-ld'][0]['@graph'] if properties['@type']=='ClaimReview']
	mode='json'

for elements in selected:
	print "#######################################################################"
	print "#######################################################################"
	print "#######################################################################"
	print "#######################################################################"
	print "#######################################################################"
	print "YOOOOOOOOOOOOOOOOO"
	if mode=='micro':
				elements=elements['properties']
	for key in elements:
		if type(elements[key])==list:
			elements[key]=elements[key][0]
	claimdf=claimdf.append(pd.io.json.json_normalize(elements),ignore_index=True)
	#Overwriting to the csv file after every crawl
	#claimdf.to_csv(domain+'.csv', encoding='utf-8')
	print "#######################################################################"
	print "#######################################################################"
	print "#######################################################################"
	print "#######################################################################"
	print "#######################################################################"
print claimdf.T
