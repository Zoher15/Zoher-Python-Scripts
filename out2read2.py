#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import namedtuple
import re
import string
import pandas as pd
Context = namedtuple('Context', 'string index')
SimpleArgument = namedtuple('SimpleArgument', 'string index')
TemporalArgument = namedtuple('TemporalArgument', 'string index')
SpatialArgument = namedtuple('SpatialArgument', 'string index')
Relation = namedtuple('Relation', 'string index')
# file=open("out2.txt","rb")
# yas=file.readlines()[1].split('\t')[-1]
# # print(re.split(r'\t',yas))
# yas=yas.replace("SimpleArgument(","SimpleArgument('").replace("Context(","Context('").replace("Relation(","Relation('").replace(",List([","',((")
# a=eval(yas)
# nametype=type(a).__name__
# print()
columnsss=[("SimpleArgument","string"),("SimpleArgument","index"),
("TemporalArgument","string"),("TemporalArgument","index"),
("SpatialArgument","string"),("SpatialArgument","index")]

def col2string(field):
	if field!=0:
		field=field.replace('"','')
		field=field.replace('SimpleArgument(','SimpleArgument("').replace('Context(','Context("').replace('Relation(','Relation("').replace(',List','",').replace("[","(").replace("{","").replace("}","")
		return eval(field).string
	else:
		return ""
def col2index(field):
	if field!=0:
		field=field.replace('"','')
		field=field.replace('SimpleArgument(','SimpleArgument("').replace('Context(','Context("').replace('Relation(','Relation("').replace(',List','",').replace("[","(").replace("{","").replace("}","")
		return eval(field).index
	else:
		return ""
#To check how many temporal/spatial/simple argument can exist
def col2split(field):
	# data=pd.DataFrame(-,None,)
	i=0
	if field!=0:
		field=field.split("; ")
		for f in field:
			if re.match(r'^TemporalArgument',f):
				i+=1
		if i==3:
			print(field)
	return i



columnames=["Confidence","Context","Argument 1","Relation","Argument(s) 2","Original Text"]
df=pd.read_csv("out2.txt",sep='\t',header=None,names=columnames)
df=df.fillna(0)

columnss=[("Confidence","",""),
("Context","","string"),("Context","","index"),
("Argument 1","","string"),("Argument 1","","index"),
("Relation","","string"),("Relation","","index"),
("Argument(s) 2","SimpleArgument #1","string"),("Argument(s) 2","SimpleArgument #1","index"),
("Argument(s) 2","SimpleArgument #2","string"),("Argument(s) 2","SimpleArgument #2","index"),
("Argument(s) 2","SimpleArgument #3","string"),("Argument(s) 2","SimpleArgument #3","index"),
("Argument(s) 2","SimpleArgument #4","string"),("Argument(s) 2","SimpleArgument #4","index"),
("Argument(s) 2","TemporalArgument","string"),("Argument(s) 2","TemporalArgument","index"),
("Argument(s) 2","SpatialArgument","string"),("Argument(s) 2","SpatialArgument","index"),
("Original Text","","")]
index2=pd.MultiIndex.from_tuples(columnss)
df2=pd.DataFrame('-',range(len(df)),index2)
df2.loc[:,'Confidence']=df['Confidence'].apply(float)		
df2.loc[:,('Argument 1',"","string")]=df.loc[:,'Argument 1'].apply(col2string)
df2.loc[:,('Argument 1',"","index")]=df.loc[:,'Argument 1'].apply(col2index)
df2.loc[:,('Context',"","string")]=df.loc[:,'Context'].apply(col2string)
df2.loc[:,('Context',"","index")]=df.loc[:,'Context'].apply(col2index)
df2.loc[:,('Relation',"","string")]=df.loc[:,'Relation'].apply(col2string)
df2.loc[:,('Relation',"","index")]=df.loc[:,'Relation'].apply(col2index)
df2.loc[:,'Original Text']=df.loc[:,'Original Text']

print(max(df["Argument(s) 2"].apply(col2split)))
# df2.to_csv("Df2.csv")
#SpatialArgument
#TemporalArgument

