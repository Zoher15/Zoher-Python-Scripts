# -*- coding: utf-8 -*-
"""tfcg_scripts.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gAjA8WAekyNP1NpGyf-2hPaZZs257rED
"""
import numpy as np
from sklearn import metrics
from sklearn import metrics
import numpy as np
import pandas as pd
df=pd.read_csv("tfcg_u_degree_true.csv")
df2=pd.read_csv("false_tfcg_u_degree_true.csv")
logdf=pd.read_csv("tfcg_u_logdegree_true.csv")
logdf2=pd.read_csv("false_tfcg_u_logdegree_true.csv")
df['label']=1
df2['label']=0
logdf['label']=1
logdf2['label']=0
finaldf=pd.concat([df,df2],ignore_index=True)
finallogdf=pd.concat([logdf,logdf2],ignore_index=True)
a=list(finaldf.sort_values(by=['simil']).index)
alog=list(finallogdf.sort_values(by=['simil']).index)
print(a==alog)
# y1=finaldf['simil']
# y1=np.asarray(y1)

# y1

# scores1=np.asarray(finaldf['simil'])

# scores=np.asarray(finaldf['simil'])

# logscores=np.asarray(finallogdf['simil'])

# scores

# logscores

# y=np.asarray(finaldf['label'])

# logy=np.asarray(finallogdf['label'])

# fpr, tpr, thresholds = metrics.roc_curve(y, scores,pos_label=1)

# logfpr, logtpr, logthresholds = metrics.roc_curve(logy,logscores,pos_label=1)

# fpr

# logfpr

# import matplotlib.pyplot as plt

# fpr

# fpr.shape

# plt.figure()

# y

# np.save("y.npy",y)

# np.save("logy.npy",logy)

# np.save("scores.npy",scores)

# np.save("logscores.npy",logscores)

# y

# logy

# scores