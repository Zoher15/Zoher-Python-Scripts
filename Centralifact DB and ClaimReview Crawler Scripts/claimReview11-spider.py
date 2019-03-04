from scrapy.spiders import SitemapSpider
import extruct
import pandas as pd
from scrapy.exceptions import CloseSpider
from urlparse import urlparse
# from sqlalchemy import create_engine
# from sqlalchemy.engine.url import URL
# import settings
class claimReviewSpider(SitemapSpider):
	name='claimReview-spider'
	claimdf=pd.DataFrame()
	USER_AGENT = 'Indiana-University-Researcher-Zoher-Kachwala(zkachwal@iu.edu)'
	COOKIES_ENABLED = True
	ROBOTSTXT_OBEY = False
	AUTOTHROTTLE_ENABLED = True
	sitemap_urls=['https://pagellapolitica.it/sitemap.xml']
	#sitemap_urls=['https://www.washingtonpost.com/web-sitemap-index.xml,https://www.washingtonpost.com/news-sitemap-index.xml,https://www.washingtonpost.com/video-sitemap.xml,https://www.washingtonpost.com/real-estate/sitemap.xml,https://jobs.washingtonpost.com/sitemapindex.xml,https://www.washingtonpost.com/wp-stat/sitemaps/index.xml']
	def parse(self, response):
		#To limit the crawled claimReview items
		if(len(self.claimdf)==100):
			raise CloseSpider('######################################100 crawled#################################')
		#Extructing microdata or json in RDFA format 
		data=extruct.extract(response.text,response.url)
		#Domain Name
		domain=urlparse(response.url).netloc.strip('www').strip('.com')
		#Selecting Microdata
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
			print "Testing"
			if mode=='micro':
				elements=elements['properties']
			for key in elements:
				if type(elements[key])==list:
					elements[key]=elements[key][0]
			self.claimdf=self.claimdf.append(pd.io.json.json_normalize(elements),ignore_index=True)
			#Overwriting to the csv file after every crawl
			self.claimdf.to_csv(domain+'.csv', encoding='utf-8')
			print "#######################################################################"
			print "#######################################################################"
			print "#######################################################################"
			print "#######################################################################"
			print "#######################################################################"
	#engine=create_engine(URL(**settings.DATABASE),connect_args={'charset':'utf8'})	
	#claimdf.to_sql('claim',engine, if_exists='replace')
	#Writing the final dataframe to CSV
	#claimdf.to_csv(domain+'.csv', encoding='utf-8')
