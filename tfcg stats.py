import numpy as np 
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
degreelist=np.asarray(pd.read_csv("degree.csv")['degree'])
degreefreq=np.asarray([float(0) for i in range(max(degreelist)+1)])
for degree in degreelist:
	degreefreq[degree]+=1
degreeprob=degreefreq/sum(degreefreq)
plt.figure()	
plt.plot(range(0,max(degreelist)+1),degreeprob)
plt.xlabel('Degree')
plt.ylabel('Probability')
plt.title('Degree Distribution')
plt.show()