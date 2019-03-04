#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
file=open("out.txt","rb")
data=file.read().decode()
data=data.split("\n\n")
for line in data:
	print(line)
	print("########################")