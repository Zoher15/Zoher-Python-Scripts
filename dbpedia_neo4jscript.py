import pandas as pd
import re
import numpy as np
import rdflib
from rdflib import BNode, Literal
from rdflib.namespace import RDF
from py2neo import Graph, NodeMatcher

g=rdflib.Graph()

# graph = Graph("bolt://127.0.0.1:7687",password="1234")
# matcher = NodeMatcher(graph)
# a=list(matcher.match("dbpedia"))
# a=list(map(lambda x:x['uri'],a))
# np.save("dbpedia_entities_TFCC.npy",a)
g.parse("test.ttl", format="turtle")
a=np.load("dbpedia_entities_TFCC.npy")
triplelist=[]
for triple in g:
	subject,predicate,obj=triple
	print(subject,obj)
	triplelist.append(triple)

print(triplelist)
