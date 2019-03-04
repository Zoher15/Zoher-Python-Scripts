from scrapy.spiders import SitemapSpider
import extruct
import pandas as pd
from scrapy.exceptions import CloseSpider
# from sqlalchemy import create_engine
# from sqlalchemy.engine.url import URL
# import settings
class claimReviewSpider(SitemapSpider):
	name='claimReview-spider'
	claimdf=pd.DataFrame()
	USER_AGENT = 'Indiana-University-Zoher-Kachwala(zkachwal@iu.edu)'
	ROBOTSTXT_OBEY = True
	AUTOTHROTTLE_ENABLED = True
	sitemap_urls=['https://www.metro.se/sitemap.xml']
	
	def parse(self, response):
		if(len(self.claimdf)==100):
			raise CloseSpider('100 crawled')
		data=extruct.extract(response.text,response.url)['microdata']
		selected=[properties for properties in data if properties['type']=='http://schema.org/ClaimReview']
		for elements in selected:
			print "#######################################################################"
			print "#######################################################################"
			print "#######################################################################"
			print "#######################################################################"
			print "#######################################################################"
			print "YOOOOOOOOOOOOOOOOO"
			dictt=elements['properties']
			for key in dictt:
				if type(dictt[key])==list:
					dictt[key]=dictt[key][0]
			self.claimdf=self.claimdf.append(pd.io.json.json_normalize(dictt),ignore_index=True)
			self.claimdf.to_csv('metro.se.csv', encoding='utf-8')
			print "#######################################################################"
			print "#######################################################################"
			print "#######################################################################"
			print "#######################################################################"
			print "#######################################################################"
	#engine=create_engine(URL(**settings.DATABASE),connect_args={'charset':'utf8'})	
	#claimdf.to_sql('claim',engine, if_exists='replace')
	claimdf.to_csv('metro.se.csv', encoding='utf-8')
