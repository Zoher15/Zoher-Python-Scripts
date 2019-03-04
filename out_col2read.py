#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import namedtuple
import html
import re
import string
import pandas as pd
import numpy as np
import json
from pprint import pprint
'''
Basic raw read from the txt output file of Open IE 5.0 
'''
dfcolumns=["Confidence","Context","Argument 1","Relation","Argument(s) 2","Original Text"]
df=pd.read_csv("out_col.txt",sep='\t',names=dfcolumns)
print(df)
pprint(df.to_json(orient='split'))