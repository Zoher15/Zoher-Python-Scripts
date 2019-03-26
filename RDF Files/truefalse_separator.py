import pandas as pd
import re
from rdflib import Graph
import numpy as np

data=pd.read_csv("claimreviews_db.csv",index_col=0)
data=data.loc[data['fact_checkerID']>1].reset_index(drop=True)
trueregex=re.compile('(?i)true.*|correct.*')
falseregex=re.compile('(?i)false.*')
trueind=data['rating_name'].apply(trueregex.match).apply(lambda x:x!=None)
trueclaims=list(data.loc[trueind]['claimID'])
falseind=data['rating_name'].apply(falseregex.match).apply(lambda x:x!=None)
falseclaims=list(data.loc[falseind]['claimID'])
graph = Graph()
truerror=[]
falserror=[]
for t in trueclaims:
	filename=str(t)+".rdf"
	try:
		graph.parse(filename,format='application/rdf+xml')
	except:
		truerror.append(t)
graph.serialize(destination='truegraph.rdf', format='application/rdf+xml')
print("True Total:",len(trueclaims))
print("True Errors:",len(truerror))
print("True Delta:",len(trueclaims)-len(truerror))

graph = Graph()

for f in falseclaims:
	filename=str(f)+".rdf"
	try:
		graph.parse(filename,format='application/rdf+xml')
	except:
		falserror.append(f)
graph.serialize(destination='falsegraph.rdf', format='application/rdf+xml')
print("False Total:",len(falseclaims))
print("False Errors:",len(falserror))
print("False Delta:",len(falseclaims)-len(falserror))

np.save("truerror_claimID.npy",truerror)
np.save("falserror_claimID.npy",truerror)
# data=np.load("Error500_claimID.npy")
# print(len(data))