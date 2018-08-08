#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 16:41:49 2018

@author: prubbens
"""
import numpy as np
import pandas as pd
import phenograph
from sklearn.metrics import v_measure_score, adjusted_rand_score

np.random.seed(27)

'''Read in data'''
df = pd.read_table('Phenograph_cluster/full-output/DMLMJ/test.2', sep=',', index_col=None, header=None)

'''Variables to use, leave cell population label out'''
features = list(df.columns)[:-1]

'''Last column contains cell population labels'''
target = df.iloc[:,-1]

'''k to check for PhenoGraph algorithm'''
possible_k = [15,30,45,60]

'''Arrays to store performance measures; ari: Adjusted Rand Index, v: V-measure'''
ari_M = np.zeros(len(possible_k))
v_M = np.zeros(len(possible_k))

i=0
for k_ in possible_k: 
    communities, graph, Q = phenograph.cluster(df.loc[:,features], k=k_, primary_metric='Euclidean')
    ari_M[i] = adjusted_rand_score(target,communities)
    v_M[i] = v_measure_score(target,communities)
    i+=1

ari_M = pd.Series(ari_M, index=possible_k)
v_M = pd.Series(v_M, index=possible_k)

ari_M.to_csv('Phenograph_cluster/Results/Phenograph/ari_patient2_M_k.csv')
v_M.to_csv('Phenograph_cluster/Results/Phenograph/v_patient2_M_k.csv')
