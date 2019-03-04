from scrapy.spiders import SitemapSpider
import extruct
import pandas as pd
# from sqlalchemy import create_engine
# from sqlalchemy.engine.url import URL
# import settings
class claimReviewSpider(SitemapSpider):
	name='claimReview-spider'
	USER_AGENT = 'Indiana-University-Zoher-Kachwala(zkachwal@iu.edu)'
	ROBOTSTXT_OBEY = True
	AUTOTHROTTLE_ENABLED = True
	sitemap_urls=['http://www.politifact.com/sitemap.xml']
	claimdf=pd.DataFrame()
	def parse(self, response):
		if(len(claimdf)==2):
			raise CloseSpider("100 ClaimReview crawled")
		#r=requests.get(response.url)
		data=extruct.extract(response.text,response.url)['microdata']
		selected=[properties for properties in data if properties['type']=='http://schema.org/ClaimReview']
		for elements in selected:
			print "#######################################################################"
			print "#######################################################################"
			print "#######################################################################"
			print "#######################################################################"
			print "#######################################################################"
			dictt=elements['properties']
			for key in dictt:
				if type(dictt[key])==list:
					dictt[key]=dictt[key][0]
			claimdf=claimdf.append(pd.io.json.json_normalize(dictt),ignore_index=True)
			claimdf.to_csv('yo.csv', encoding='utf-8')
			print "#######################################################################"
			print "#######################################################################"
			print "#######################################################################"
			print "#######################################################################"
			print "#######################################################################"
	#engine=create_engine(URL(**settings.DATABASE),connect_args={'charset':'utf8'})	
	#claimdf.to_sql('claim',engine, if_exists='replace')
	claimdf.to_csv('politifact.csv', encoding='utf-8')
