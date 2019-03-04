import requests
import re
from pprint import pprint
import pandas as pd 
open("claimtext.html", 'w').close()
f = open("claimtext.html", "a")
def dbpedia_annotate(row):
	data={'text':row['claim_text'],'confidence':0.5,'support':20}
	header1={"Accept":"application/json"}
	header2={"Accept":"application/xhtml+xml"}
	while True:
		try:
			r1=requests.post("http://model.dbpedia-spotlight.org/en/annotate",data=data,headers=header1)
			try:
				row["dbpedia_annotate"]=eval(r1.text)['Resources']
			except KeyError:
				row["dbpedia_annotate"]=None
			r2=requests.post("http://model.dbpedia-spotlight.org/en/annotate",data=data,headers=header2)
			if not re.search(r">50\d",r2.text):
				f.write("<br />\n"+r2.text)
				break
			print("Z2")
		except SyntaxError:
			print("Z1")
			continue
	return row
# time java -Xmx20g -XX:+UseConcMarkSweepGC -jar openie-assembly.jar --format column claimtext_db.txt out_col.txt
# time java -Xmx20g -XX:+UseConcMarkSweepGC -jar openie-assembly.jar --format simple claimtext_db.txt out_simple.txt
data=pd.read_csv("claimreview_db.csv",index_col=0)
data["dbpedia_annotate"]=""
data=data.apply(dbpedia_annotate,axis=1)
data.to_csv("claimreview_db_spotlight.csv",header=True)

# s="KAMALA HARRIS Says Schools in Berkeley Weren't Integrated When She Was a Kid - But Yearbook Pictures Prove She's Lying."
# data={'text':s.lower(),'confidence':0.5,'support':20}
# header1={"Accept":"application/json"}
# header2={"Accept":"application/xhtml+xml"}
# r1=requests.post("http://model.dbpedia-spotlight.org/en/annotate",data=data,headers=header1)
# r2=requests.post("http://model.dbpedia-spotlight.org/en/annotate",data=data,headers=header2)
# print(r2.text)

