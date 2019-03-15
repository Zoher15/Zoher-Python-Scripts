import requests
import re
from pprint import pprint
import pandas as pd 
import uncurl
from rdflib import Graph
import time
import xml.sax
import pdb
import numpy as np

url="http://wit.istc.cnr.it/stlab-tools/fred"
header={"Accept":"application/rdf+xml","Authorization":"Bearer 56a28f54-7918-3fdd-9d6f-850f13bd4041"}
graph = Graph()
# graph.parse("2484.rdf",format='application/rdf+xml')
# graph.serialize(destination='cl_db.rdf', format='application/rdf+xml')
try:
	errorclaimid=list(np.load("Error500_claimID.npy"))
except FileNotFoundError:
	errorclaimid=[]
try:
	graph.parse("claimreviews_db.rdf",format='application/rdf+xml')
except FileNotFoundError:
	pass

def fred_annotate(row):
	text=row['claim_text']
	claimid=row['claimID']
	filename=str(claimid)+".rdf"
	data={'text':text,'semantic-subgraph':True}
	r=requests.get(url,params=data,headers=header)
	f = open(filename, "w")
	f.write("<?xml version='1.0' encoding='UTF-8'?>\n"+r.text)
	return(r.status_code,r.text,filename)

data=pd.read_csv("claimreviews_db.csv",index_col=0)
data=data.loc[data['fact_checkerID']>1].reset_index(drop=True)
start=time.time()
start2=time.time()
daysec=86400
minsec=60
init=0
for i in range(init,len(data)):
	dif=abs(time.time()-start)
	diff=abs(daysec-dif)
	# if (i-init+1)%1500==0 and diff>0:
	# 	print("Sleeping for ",round(diff))
	# 	time.sleep(diff)
	# 	start=time.time()
	# 	start2=time.time()
	while True:
		try:
			dif=abs(time.time()-start)
			dif2=abs(time.time()-start2)
			diff=abs(daysec-dif)
			claimID=data.iloc[i]['claimID']
			print("Index:",i,"Claim ID:",claimID," DayLim2Go:",round(diff),"MinLim2Go:",round(min(abs(minsec-dif2),60)))
			rcode,rtext,filename=fred_annotate(data.iloc[i])
			if "You have exceeded your quota" not in rtext and "Runtime Error" not in rtext and "Service Unavailable" not in rtext:
				if rcode in range(100,500) and rtext:
					graph.parse(filename,format='application/rdf+xml')
					graph.serialize(destination='claimreviews_db.rdf', format='application/rdf+xml')
				else:
					errorclaimid.append(filename.strip(".rdf"))
					np.save("Error500_claimID.npy",errorclaimid)
				break
			else:
				diff2=min(abs(minsec-dif2),60)
				print("Sleeping for ",round(diff2))
				time.sleep(abs(diff2))
				start2=time.time()
		except xml.sax._exceptions.SAXParseException:
			print("Exception Occurred")
			errorclaimid.append(claimID)
			break