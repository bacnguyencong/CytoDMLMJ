#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 16:41:49 2018

@author: prubbens
"""
from io import StringIO
import matplotlib.pyplot as plt
import re
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import f1_score, confusion_matrix

def report_to_df(report):
    report = re.sub(r" +", " ", report).replace("avg / total", "avg/total").replace("\n ", "\n")
    report_df = pd.read_csv(StringIO("Classes" + report), sep=' ', index_col=0)        
    return(report_df)
    
def print_confusion_matrix(confusion_matrix, class_names, figsize = (10,7), fontsize=14):
    """Prints a confusion matrix, as returned by sklearn.metrics.confusion_matrix, as a heatmap.
    
    Arguments
    ---------
    confusion_matrix: numpy.ndarray
        The numpy.ndarray object returned from a call to sklearn.metrics.confusion_matrix. 
        Similarly constructed ndarrays can also be used.
    class_names: list
        An ordered list of class names, in the order they index the given confusion matrix.
    figsize: tuple
        A 2-long tuple, the first value determining the horizontal size of the ouputted figure,
        the second determining the vertical size. Defaults to (10,7).
    fontsize: int
        Font size for axes labels. Defaults to 14.
        
    Returns
    -------
    matplotlib.figure.Figure
        The resulting confusion matrix figure
    """
    df_cm = pd.DataFrame(
        confusion_matrix, index=class_names, columns=class_names, 
    )
    fig = plt.figure(figsize=figsize)
    try:
        heatmap = sns.heatmap(df_cm, annot=False, fmt="d", vmin=0, vmax=1, cmap='RdBu')
    except ValueError:
        raise ValueError("Confusion matrix values must be integers.")
    heatmap.yaxis.set_ticklabels(heatmap.yaxis.get_ticklabels(),  rotation=0, ha='right', fontsize=fontsize)
    heatmap.xaxis.set_ticklabels(heatmap.xaxis.get_ticklabels(), rotation=45, ha='right', fontsize=fontsize)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    return fig

df_13_E_1 = pd.read_table('Application_2+Dataset_1/output/Euclidean/prediction.txt', sep=',', index_col=None, header=None)
df_32_E_1 = pd.read_table('Application_2+Dataset_2/output/Euclidean/prediction.1.txt', sep=',', index_col=None, header=None)
df_32_E_2 = pd.read_table('Application_2+Dataset_2/output/Euclidean/prediction.2.txt', sep=',', index_col=None, header=None)

df_13_M_1 = pd.read_table('Application_2+Dataset_1/output/DMLMJ/prediction.txt', sep=',', index_col=None, header=None)
df_32_M_1 = pd.read_table('Application_2+Dataset_2/output/DMLMJ/prediction.1.txt', sep=',', index_col=None, header=None)
df_32_M_2 = pd.read_table('Application_2+Dataset_2/output/DMLMJ/prediction.2.txt', sep=',', index_col=None, header=None)

labels_E = pd.read_table('Application_2+Dataset_1/data/population_names_Levine_13dim.txt', index_col=0, header=0)
labels_M = pd.read_table('Application_2+Dataset_2/data/population_names_Levine_32dim.txt', index_col=0, header=0)


names = ['Levine_13_E','Levine_32_E_1','Levine_32_E_2','Levine_13_M','Levine_32_M_1','Levine_32_M_2']
labels = [labels_E,labels_M,labels_M,labels_E,labels_M,labels_M]

df_list = [df_13_E_1,df_32_E_1,df_32_E_2,df_13_M_1,df_32_M_1,df_32_M_2]
i = 0
f1 = np.zeros(len(df_list))
for df in df_list: 
    cf = confusion_matrix(df.loc[:,1],df.loc[:,0])
    #print_confusion_matrix(cf, labels[i] )
    print_confusion_matrix(cf / cf.astype(np.float).sum(axis=1, keepdims=True), labels[i], fontsize=10 )
    plt.savefig(names[i]+'_cf.png', dpi=300)
    f1[i] = f1_score(df.loc[:,0],df.loc[:,1], average='macro')
    i+=1

f1 = pd.Series(f1, index=names)
f1.to_csv('f1_score_avg.csv')