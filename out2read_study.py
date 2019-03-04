#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import string
import pandas as pd
import numpy as np
import html
# import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib_venn import venn3, venn3_circles
pd.set_option("max_columns", 30)
out1columns=[("Original Text","",""),
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
("Argument(s) 2","SpatialArgument #2","string"),("Argument(s) 2","SpatialArgument #2","index"),
("Claim ID","",""),("Z Label","",""),("Y Label","","")]
# '''
# Reading the pickled pandas dataframe
# '''
# df1=pd.read_pickle("df1.pkl")
# print(df1)
# '''
# Removing index column and Counting Argument(s) 2
# '''
# df2=df1.loc(axis=1)[slice(None),slice(None),["string",""]]
# argument2ind=np.array(df2['Argument(s) 2'].count(axis=1).tolist())
# '''
# Indices where the Argument(s) 2 are zero, one or many
# '''
# zeroind=np.where(argument2ind==0)[0]
# oneind=np.where(argument2ind==1)[0]
# manyind=np.where(argument2ind>1)[0]
# zerolist=df1.iloc[zeroind]["Original Text"].unique().tolist()
# onelist=df1.iloc[oneind]["Original Text"].unique().tolist()
# manylist=df1.iloc[manyind]["Original Text"].unique().tolist()
# '''
# # Plotting the venn for distribution and overlap of Argument 2 Distribution
# # '''
# # venn3([set(zerolist), set(onelist), set(manylist)], set_labels = ('Zero "Argument 2" (Total 856)','One "Argument 2" (Total 6509)', 'Many "Argument 2" (Total 3236)'))
# # plt.title('Comparison of Claim Extractions (Total 7692)\n')
# # plt.show()
# # venn3([set(zeroind), set(oneind), set(manyind)], set_labels = ('Zero "Argument 2"', 'Simple "Argument 2"', 'Complex "Argument 2"'))
# # plt.title('Comparison of Total Extractions Total 17826\n')
# # plt.show()
# '''
# Writing the three different extractions in csv and readable format
# '''
# df1[df1["Original Text"].isin(zerolist)].to_csv("outzero.csv")
# df1[df1["Original Text"].isin(onelist)].to_csv("outone.csv")
# df1[df1["Original Text"].isin(manylist)].to_csv("outmany.csv")
# file=open("out.txt","rb")
# data=file.read().decode()
# data=data.split("\n\n")
# wfile1=open("outzero.txt","wb")
# wfile2=open("outone.txt","wb")
# wfile3=open("outmany.txt","wb")
# print(len(zerolist))
# print(len(onelist))
# print(len(manylist))
# for line in data:
# 	line=line.replace('""','"')
# 	temp=line.split("\n")[0][1:-1]
# 	line=(line+"\n\n").encode()
# 	if temp in zerolist:
# 		zerolist.remove(temp)
# 		wfile1.write(line)
# 	if temp in onelist:
# 		onelist.remove(temp)
# 		wfile2.write(line)
# 	if temp in manylist:
# 		manylist.remove(temp)
# 		wfile3.write(line)
'''
Analyzing Outone
Z Label:0 Reject, 1 Modify , 2 Yes but better extraction, 3 best extraction, 4 best but not simple
Y label (coref resolution): 1 could be automated, 2 need info from claimreview database (the claimant)
'''
out1index=pd.MultiIndex.from_tuples(out1columns,names=["category","type(Argument 2)","datatype"])
out1=pd.read_csv("outone.csv",index_col=0)
out1.columns=out1index
out1=out1.loc(axis=1)[slice(None),slice(None),["string",""]]
out1=out1[out1["Z Label"]==3]
out1arg2ind=np.array(out1['Context'].count(axis=1).tolist())
manyind=np.where(out1arg2ind>0)[0]
zeroind=np.where(out1arg2ind==0)[0]
print(len(manyind)/len(zeroind))
'''
Going from the multilevel column header for "Argument(s) 2":
												"Argument(s) 2"
														|
Level1:type(Argument 2)	<<SimpleArgument #1>>..<<SimpleArgument #n>> <<TemporalArgument #1>>..<<SimpleArgument #n>> <<SpatialArgument #1>>..<<SpatialArgument #n>>
							 ___|___		 		 ___|___	 			 ___|___		 		 ___|___	 			 ___|___		 		 ___|___			 
						     |     |	  	 		 |     |	  	 		 |     |	  	 		 |     |	  	 		 |     |	  	 		 |     |
Level2:datatype			   string index    		   string index    		   string index    		   string index    		   string index    		   string index
to
single level column header by picking the single non-null value in each row
'''
def func(x):
    if x.first_valid_index() is None:
        return None
    else:
        return x[x.first_valid_index()]
print(out1["Argument(s) 2"].shape)
temp=pd.Series(out1["Argument(s) 2"].apply(func, axis=1))
out1=out1.drop("Argument(s) 2", axis=1)
print(out1)
out1.columns=["Original Text","Confidence","Context","Argument 1","Relation","Claim ID","Z Label","Y Label"]
print(temp.shape)
out1["Argument(s) 2"]=temp
out1.to_csv("simpleout1.csv")
# '''
# Counting Context
# '''
# contextind=np.where(df1['Context'])[0]
# contextlist=df1.iloc[contextind]["Original Text"].unique().tolist()
# one_arg2_contextind=list(set(oneind).intersection(set(contextind)))
# one_arg2_contextlist=set(df1.iloc[one_arg2_contextind]["Original Text"].unique().tolist())
# print(len(contextlist))
# print(len(onelist))
# print(len(one_arg2_contextlist))








# print(df1.xs("",axis=1,level="datatype") and df1.xs("string",axis=1,level="datatype"))
#@@@@@@To detect where Simple Argument #4 is not zero
# print(df2[df2["Argument(s) 2"]["SpatialArgument #2"]["string"]!="-"])
# print(df2[df2["Argument(s) 2"]["SimpleArgument #2"]["string"]!="-"])
# print(df2[df2["Argument(s) 2"]["TemporalArgument #2"]["string"]!="-"])
# print(df2[(df2["Argument(s) 2"]["SimpleArgument #4"]["string"]!="-") | (df2["Argument(s) 2"]["SimpleArgument #3"]["string"]!="-") | (df2["Argument(s) 2"]["SimpleArgument #2"]["string"]!="-")])
# print(df2[(df2["Argument(s) 2"]["TemporalArgument #3"]["string"]!="-") | (df2["Argument(s) 2"]["TemporalArgument #2"]["string"]!="-")])
# print(df2[df2["Argument(s) 2"]["SpatialArgument #2"]["string"]!="-"])
# df2[df2["Argument(s) 2"]["TemporalArgument #3"]["string"]!="-"].to_csv("Dftemporal3.csv")
# print(df2.shape)