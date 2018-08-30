#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 16:41:49 2018

@author: prubbens
"""
# Import packaes
import numpy as np
import pandas as pd
import phenograph
from sklearn.metrics import v_measure_score, adjusted_rand_score

np.random.seed(27)

#Read in data'''
df = pd.read_table('output/Euclidean/test.1.txt', sep=',', index_col=None, header=None)

# Variables to use, leave cell population label out'''
features = list(df.columns)[:-1]

# Last column contains cell population labels'''
target = df.iloc[:,-1]

# k to check for PhenoGraph algorithm'''
possible_k = [15,30,45,60]

# Arrays to store performance measures; ari: Adjusted Rand Index, v: V-measure'''
ari = np.zeros(len(possible_k))
v = np.zeros(len(possible_k))

i=0
for k_ in possible_k: 
    communities, graph, Q = phenograph.cluster(df.loc[:,features], k=k_, primary_metric='Euclidean')
    ari[i] = adjusted_rand_score(target,communities)
    v[i] = v_measure_score(target,communities)
    i+=1

ari = pd.Series(ari, index=possible_k)
v = pd.Series(v, index=possible_k)

ari.to_csv('output/PhenoGraph_results/ari_patient2_M_k.csv')
v.to_csv('output/PhenoGraph_results/v_patient2_M_k.csv')