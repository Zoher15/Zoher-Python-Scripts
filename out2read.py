#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import namedtuple
import html
import re
import string
import pandas as pd
import numpy as np
pd.set_option("max_columns", 30)
'''
The tool used is OpenIE 5.0. After following the installation instructions, pass the text file of choice to the system.
If the file contains quotes ' " ', wrap each text within double quotes to avoid the system from raising any exceptions or errors.
Use the simple mode of the system to output extractions that are readable and use the tabbed one to create extractions that can be read by Pandas
'''

'''
The machine readable format of OpenIE 5.0 is similar to named tuples so I am using the same data structure from the collections package. However it does have some differences.
The biggest one being that the text enclosed within the tuples is not within quotes, which throws errors in python. 
This is addressed by creating a not so elegant "replace" chain
'''
Context = namedtuple('Context', 'string index')
SimpleArgument = namedtuple('SimpleArgument', 'string index')
TemporalArgument = namedtuple('TemporalArgument', 'string index')
SpatialArgument = namedtuple('SpatialArgument', 'string index')
Relation = namedtuple('Relation', 'string index')
'''
Using the named tuple structure to extract the string enclosed.
Performing a chain of "replace" commands to make the output format compatible with python i.e enclosing string within ""
'''
def col2re(field):
	if field!=0:
		field=field.replace('"','').replace("[","(").replace("{","(").replace("}",")")
		cleanre=re.compile(r"^(.*Argument|Relation|Context)\((.*),List\(([\w\s,\(\)]*)\)\).*$")
		field2=re.sub(cleanre,r'\1("\2",(\3))',field)
		temp=eval(field2)
		return temp.string,temp.index
	else:
		return ""
'''
Splitting the <Argument(s) 2> Column
'''
def col2split(field):
	global argument2
	data=pd.DataFrame('-',range(1),argument2index)
	i=j=k=0
	if field!=0:
		field=field.split("); ")
		if len(field)>1:
			field[:-1]=[field[fi]+")" for fi in range(len(field)-1)]
		for f in field:
			if re.match(r'^SimpleArgument',f):
				i+=1
				if i==1:
					data.loc[0,('SimpleArgument #1','string')]=col2string(f)
					data.loc[0,('SimpleArgument #1','index')]=col2index(f)
				elif i==2:
					data.loc[0,('SimpleArgument #2','string')]=col2string(f)
					data.loc[0,('SimpleArgument #2','index')]=col2index(f)
				elif i==3:
					data.loc[0,('SimpleArgument #3','string')]=col2string(f)
					data.loc[0,('SimpleArgument #3','index')]=col2index(f)
				elif i==4:
					data.loc[0,('SimpleArgument #4','string')]=col2string(f)
					data.loc[0,('SimpleArgument #4','index')]=col2index(f)
			elif re.match(r'^TemporalArgument',f):
				j+=1
				if j==1:
					data.loc[0,('TemporalArgument #1','string')]=col2string(f)
					data.loc[0,('TemporalArgument #1','index')]=col2index(f)
				elif j==2:
					data.loc[0,('TemporalArgument #2','string')]=col2string(f)
					data.loc[0,('TemporalArgument #2','index')]=col2index(f)
				elif j==3:
					data.loc[0,('TemporalArgument #3','string')]=col2string(f)
					data.loc[0,('TemporalArgument #3','index')]=col2index(f)
			elif re.match(r'^SpatialArgument',f):
				k+=1
				if k==1:
					data.loc[0,('SpatialArgument #1','string')]=col2string(f)
					data.loc[0,('SpatialArgument #1','index')]=col2index(f)
				elif k==2:
					data.loc[0,('SpatialArgument #2','string')]=col2string(f)
					data.loc[0,('SpatialArgument #2','index')]=col2index(f)
	argument2=argument2.append(data,ignore_index=True)
'''
Basic raw read from the txt output file of Open IE 5.0 
'''
dfcolumns=["Confidence","Context","Argument 1","Relation","Argument(s) 2","Original Text"]
df=pd.read_csv("out_col.txt",sep='\t',names=dfcolumns)
df=df.fillna(0)
'''
Creating a multilevel column header to create the following hierarchy:
Level1:Category	<Confidence> <Context> <Argument 1> <Relation> <Argument(s) 2> <Original Text>
								|			|			|			|___________________________________________________________________________________________________________________________													
								|			|			|				|		........		|						|		........		|						|		........		|
Level2:type(Argument 2)		    |  		    |  		    |   	<<SimpleArgument #1>>..<<SimpleArgument #n>> <<TemporalArgument #1>>..<<SimpleArgument #n>> <<SpatialArgument #1>>..<<SpatialArgument #n>>
							____|__		____|__		 ___|___		 ___|___		 		 ___|___	 			 ___|___		 		 ___|___	 			 ___|___		 		 ___|___			 
							|     |		|     |	  	 |     |         |     |	  	 		 |     |	  	 		 |     |	  	 		 |     |	  	 		 |     |	  	 		 |     |
Level3:datatype			 string index string index string index    string index    		   string index    		   string index    		   string index    		   string index    		   string index
'''
df1columns=[("Original Text","",""),
("Confidence","",""),
("Context","","string"),("Context","","index"),
("Argument 1","","string"),("Argument 1","","index"),
("Relation","","string"),("Relation","","index"),
("Argument(s) 2","SimpleArgument #1","string"),("Argument(s) 2","SimpleArgument #1","index"),
("Argument(s) 2","SimpleArgument #2","string"),("Argument(s) 2","SimpleArgument #2","index"),
("Argument(s) 2","SimpleArgument #3","string"),("Argument(s) 2","SimpleArgument #3","index"),
("Argument(s) 2","SimpleArgument #4","string"),("Argument(s) 2","SimpleArgument #4","index"),
("Argument(s) 2","TemporalArgument #1","string"),("Argument(s) 2","TemporalArgument #1","index"),
("Argument(s) 2","TemporalArgument #2","string"),("Argument(s) 2","TemporalArgument #2","index"),
("Argument(s) 2","TemporalArgument #3","string"),("Argument(s) 2","TemporalArgument #3","index"),
("Argument(s) 2","SpatialArgument #1","string"),("Argument(s) 2","SpatialArgument #1","index"),
("Argument(s) 2","SpatialArgument #2","string"),("Argument(s) 2","SpatialArgument #2","index"),]
df1index=pd.MultiIndex.from_tuples(df1columns,names=["category","type(Argument 2)","datatype"])
df1=pd.DataFrame('-',range(len(df)),df1index)
'''
Creating a multilevel column header to create the following hierarchy:
Level1:type(Argument 2)	<<SimpleArgument #1>>..<<SimpleArgument #n>> <<TemporalArgument #1>>..<<SimpleArgument #n>> <<SpatialArgument #1>>..<<SpatialArgument #n>>
							 ___|___		 		 ___|___	 			 ___|___		 		 ___|___	 			 ___|___		 		 ___|___			 
						     |     |	  	 		 |     |	  	 		 |     |	  	 		 |     |	  	 		 |     |	  	 		 |     |
Level2:datatype			   string index    		   string index    		   string index    		   string index    		   string index    		   string index
'''
argument2columns=[("SimpleArgument #1","string"),("SimpleArgument #1","index"),
("SimpleArgument #2","string"),("SimpleArgument #2","index"),
("SimpleArgument #3","string"),("SimpleArgument #3","index"),
("SimpleArgument #4","string"),("SimpleArgument #4","index"),
("TemporalArgument #1","string"),("TemporalArgument #1","index"),
("TemporalArgument #2","string"),("TemporalArgument #2","index"),
("TemporalArgument #3","string"),("TemporalArgument #3","index"),
("SpatialArgument #1","string"),("SpatialArgument #1","index"),
("SpatialArgument #2","string"),("SpatialArgument #2","index")]
argument2index=pd.MultiIndex.from_tuples(argument2columns,names=["type(Argument 2)","datatype"])
argument2=pd.DataFrame('-',range(0),argument2index)
'''
Populating the dataframe df1 from the raw data dataframe df by performing transformations and splits
'''
df1.loc[:,'Original Text']=df.loc[:,'Original Text']
df1.loc[:,'Confidence']=df['Confidence'].map(float)
tempre=df.loc[:,'Argument 1'].map(col2re)
df1.loc[:,('Argument 1',"","string")]=tempre.map(lambda x:x[0] if x else np.nan)
df1.loc[:,('Argument 1',"","index")]=tempre.map(lambda x:x[1] if x else np.nan)
tempre=df.loc[:,'Context'].map(col2re)
df1.loc[:,('Context',"","string")]=tempre.map(lambda x:x[0] if x else np.nan)
df1.loc[:,('Context',"","index")]=tempre.map(lambda x:x[1] if x else np.nan)
tempre=df.loc[:,'Relation'].map(col2re)
df1.loc[:,('Relation',"","string")]=tempre.map(lambda x:x[0] if x else np.nan)
df1.loc[:,('Relation',"","index")]=tempre.map(lambda x:x[1] if x else np.nan)
# df['Argument(s) 2'].map(col2split)
# df1['Argument(s) 2']=argument2
df1=df1.apply(html.unescape)
print(df1)
# '''
# Mergin with Claim Id from the Centralifact Database
# '''
# df1=df1.replace('-',np.nan)
# claimsindex=pd.MultiIndex.from_tuples([("Claim Id","",""),("Original Text","","")],names=["category","type(Argument 2)","datatype"])
# claims=pd.read_csv("claimreview_db_spotlight.csv",encoding="utf-8")# can use pd.read_sql_query to get it directly. But working with a specific dataset right now
# claimsdf=pd.DataFrame('-',range(len(claims)),claimsindex)
# claimsdf.loc[:,('Claim Id',"","")]=claims.loc[:,'Claim Id']
# claimsdf.loc[:,('Original Text',"","")]=claims.loc[:,'Original Text']
# claimsdf["Original Text"]=claimsdf["Original Text"].apply(lambda x:'"{}"'.format(x)).apply(html.unescape)
# df1=pd.merge(df1,claimsdf,how='left',on="Original Text")
# '''
# Saving to file
# '''
# df1.to_csv("df1_col.csv")
# df1.to_pickle("df1_col.pkl")


