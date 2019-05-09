import pandas as pd
import re
from rdflib import Graph
import numpy as np

data=pd.read_csv("claimreviews_db2.csv",index_col=0)
##Dropping non-str rows
filter=list(map(lambda x:type(x)!=str,data['rating_name']))
data.drop(data[filter].index,inplace=True)
# data=data.loc[data['fact_checkerID']>1].reset_index(drop=True)
# print(data.groupby('fact_checkerID').count())
trueregex=re.compile(r'(?i)^true|^correct$|^mostly true$|^geppetto checkmark$')
falseregex=re.compile(r'(?i)^false|^mostly false|^pants on fire$|^four pinocchios$|^no\ |^no:|^distorts the facts|^wrong$')
trueind=data['rating_name'].apply(lambda x:trueregex.match(x)!=None)
trueclaims=list(data.loc[trueind]['claimID'])
falseind=data['rating_name'].apply(falseregex.match).apply(lambda x:x!=None)
falseclaims=list(data.loc[falseind]['claimID'])
# data['label']="0"
# data.loc[trueind,'label']=True
# data.loc[falseind,'label']=False
# data2=data.filter(items=['label', 'claim_text'], axis=1)
# data2=data2[data2['label']!="0"]
# data2.columns=["label","text"]
# data2false=data2[data2['label']==False]
# data2true=data2[data2['label']==True]
# print(len(data2false))
# n=len(data2true)
# print(n)

# data2false=data2false.sample(n=n, random_state=1)
# frames=[data2true,data2false]
# result = pd.concat(frames)
# result.to_csv("claim_classify2.csv",index=None)
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

# file=open("rnn final project.txt","r").readlines()
# # test=list(map(lambda x: re.match(r".*(TEST.*acc )(.*)",x).group(2),file))
# test=[]
# dev=[]
# for x in file:
# 	try:
# 		test.append(float(re.match(r".*(TEST.*acc )(.*)",x).group(2)))
# 	except:
# 		continue
# for x in file:
# 	try:
# 		dev.append(float(re.match(r".*(DEV.*acc )(.*)",x).group(2)))
# 	except:
# 		continue
# print(len(test))
# print(len(dev))
# print(dev)
# print(test)
# plt.plot(test)
# plt.title("Accuracy over Epochs for RNN")
# plt.xlabel("Epochs")
# plt.ylabel("Accuracy")
# plt.axhline(y=0.5,color="red",label="random probability")
# plt.show()
