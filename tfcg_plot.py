import numpy as np 
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn import metrics
y=np.load("y.npy")
scores=np.load("scores.npy")
fpr, tpr, thresholds = metrics.roc_curve(y, scores, pos_label=1)
print(metrics.auc(fpr,tpr))
logy=np.load("logy.npy")
logscores=np.load("logscores.npy")
logfpr, logtpr, logthresholds = metrics.roc_curve(logy, logscores, pos_label=1)
print(metrics.auc(logfpr,logtpr))
print(scores)
print(logscores)
plt.figure()
lw = 2
plt.plot(logfpr, logtpr, color='darkorange',lw=lw, label='ROC curve (area = %0.2f)' % metrics.auc(fpr,tpr))
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc="lower right")
plt.title('ROC TFCG using Log Degree')
plt.show()
