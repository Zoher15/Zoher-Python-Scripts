import pandas as pd
import re
import numpy as np
import rdflib
from rdflib import BNode, Literal
from rdflib.namespace import RDF
from py2neo import Graph, NodeMatcher, RelationshipMatcher
from itertools import permutations
import csv
import re

g=rdflib.Graph()
graph = Graph("bolt://127.0.0.1:11007",password="1234")
matcher_node = NodeMatcher(graph)
matcher_rel = RelationshipMatcher(graph)
# uris=list(map(lambda x:x['uri'],list(matcher_node.match())))
# np.save("uris.npy",uris)
uris=np.load("uris.npy")
dbpedia_uris=list(map(lambda x:x['uri'],list(matcher_node.match("dbpedia"))))
np.save("dbpedia_uris.npy",uris)
# dbpedia_uris=np.load("dbpedia_uris.npy")
# with open("uris.txt","w") as f:
# 	for uri in uris:
# 		f.write(uri+"\n")
uris_dict={uris[i]:i for i in range(len(uris))}
# tx = graph.begin()
# graph_triples=tx.run("MATCH (n)-[r]-(m) return n,r,m;")
# triple_list=[]
# for triple in graph_triples:
# 	triple_list.append(triple)
# edgelist=[[uris_dict[triple_list[i]['n']['uri']],uris_dict[triple_list[i]['m']['uri']],1] for i in range(len(triple_list))]
# edgelist=np.asarray(edgelist)
# np.save("edgelist.npy",edgelist)
# # edgelist=np.load("edgelist.npy")
# # edgelist=np.matrix(edgelist)
triples_tocheck=np.load("TFCG_entity_triples_dbpedia.npy")
triples_tocheck_ID=np.array([[np.nan,int(uris_dict[t[0]]),np.nan,np.nan,int(uris_dict[t[2]]),np.nan,np.nan] for t in triples_tocheck])
perm=permutations(dbpedia_uris,2)
perms=np.asarray(list(map(lambda x:[np.nan,int(uris_dict[x[0]]),np.nan,np.nan,int(uris_dict[x[1]]),np.nan,np.nan],perm)))
z=0
randomlist=np.random.choice(range(len(perms)),size=4068,replace=False)
false_triples_tocheck_ID=[]
emptylist=[]
for i in randomlist:
	if z<2034:
		if perms[i] in triples_tocheck_ID:
			emptylist.append(i)
		else:
			z+=1
			false_triples_tocheck_ID.append(perms[i])
false_triples_tocheck_ID=np.asarray(false_triples_tocheck_ID)
with open('false_dbpedia_triples.txt',"w") as f:
	for line in false_triples_tocheck_ID:
		f.write("{} {} {} {} {} {} {}\n".format(str(line[0]),str(int(line[1])),str(line[2]),str(line[3]),str(int(line[4])),str(line[5]),str(line[6])))

# triples_tocheck_ID_set=set(list(map(lambda x: str(list(x)),np.array(triples_tocheck_ID))))
# edgelist_set=set(list(map(lambda x: str(list(x)),np.array(edgelist))))
# for i in range(len(triples_tocheck_ID)):

# print(triple_list)
# uris=pd.DataFrame(columns=["uri"])
# uris['uri']=a

# a=list(filter(db_regex.search,a))
# a=set(a)
# b=list(matcher_rel.match(nodes=a))
# print(b)

# np.save("dbpedia_entities_TFCG.npy",a)

# np.savetxt("dbpedia_entities_TFCG.txt",a)
# import csv
# with open("dbpedia_entities_TFCG.csv",'w',encoding='utf-8') as resultFile:
# 	wr = csv.writer(resultFile)
# 	wr.writerow(a)
# a=[]
# with open("dbpedia_entities_TFCG.csv") as csvfile:
# 	read=csv.reader(csvfile)
# 	for row in read:
# 		a+=row
# a=set(a)
# print(type(a))
# print(len(a))

# with open("dbpedia_entities_TFCG.csv",'w') as resultFile:
#     wr = csv.writer(resultFile)
#     wr.writerow(a)
# g.parse("test.ttl", format="turtle")
# a=set(np.load("dbpedia_entities_TFCC.npy"))
# triplelist=[]
# for triple in g:
# 	subject,predicate,obj=triple
# 	print(subject,obj)
# 	triplelist.append(triple)

# print(triplelist)
# print(a)
# np.savetxt("",a)
# np.save("a.npy",a)