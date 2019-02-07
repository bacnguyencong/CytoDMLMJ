#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 16:41:49 2018

@author: prubbens
"""
import numpy as np
import pandas as pd
import phenograph

from os import listdir
from sklearn.metrics import v_measure_score, adjusted_rand_score

PATH_M = 'output/CD/DMLMJ/CV/'
FILENAMES = sorted(listdir(PATH_M))
k_=30 
ari = np.zeros((14,14))
v = np.zeros((14,14))
n_clusters = np.zeros((14,14))
index = []

for i in np.arange(1,15): 
    for j in np.arange(1,15): 
        df = pd.read_table(PATH_M+str(i)+'.'+str(j), sep=',', index_col=None, header=None)
        features = list(df.columns)[:-1]
        target = df.iloc[:,-1]
        communities, graph, Q = phenograph.cluster(df.loc[:,features], k=k_, primary_metric='Euclidean')
        ari[i-1,j-1] = adjusted_rand_score(target,communities)
        v[i-1,j-1] = v_measure_score(target,communities)
        n_clusters[i-1,j-1] = len(np.unique(communities))
        print(i, v[i-1,j-1],n_clusters[i-1,j-1])
        
ari = pd.DataFrame(ari,index=np.arange(1,15), columns=np.arange(1,15))
v = pd.DataFrame(v,index=np.arange(1,15), columns=np.arange(1,15))
n_clusters = pd.DataFrame(n_clusters,index=np.arange(1,15), columns=np.arange(1,15))

ari.to_csv('output/CD/ARI_k='+str(k_)+'_CV_rerun.csv')
v.to_csv('output/CD/V_k='+str(k_)+'_CV_rerun.csv')
n_clusters.to_csv('output/CD/N_clusters_k='+str(k_)+'_CV_rerun.csv')