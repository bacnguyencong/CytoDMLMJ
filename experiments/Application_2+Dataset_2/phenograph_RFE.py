#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 16:41:49 2018

@author: prubbens
"""
# Import packages
import numpy as np
import pandas as pd
import phenograph
from sklearn.metrics import v_measure_score, adjusted_rand_score

# Import DMLMJ ('df') and T-DMLMJ ('df_T') transformed data for patient 1'''
#df = pd.read_table('output/DMLMJ/test_all.1.txt', sep=',', index_col=None, header=None)
#df_T = pd.read_table('output/DMLMJ/test_all.2.1.txt', sep=',', index_col=None, header=None)

# Import DMLMJ ('df') and T-DMLMJ ('df_T') transformed data for patient 2'''
df = pd.read_table('output/DMLMJ/test_all.2.txt', sep=',', index_col=None, header=None)
df_T = pd.read_table('output/DMLMJ/test_all.2.1.txt', sep=',', index_col=None, header=None)

'''Variables to use, leave cell population label out'''
features = list(df.columns)[:-1]
features_T = list(df_T.columns)[:-1]

target = df.iloc[:,-1]
target_T = df_T.iloc[:,-1]

# Hyperparameter k of the PhenoGraph algorithm'''
k_ = 30

# Arrays to store performance measures; ari: Adjusted Rand Index, v: V-measure'''
ari = np.zeros(len(features))
ari_T = np.zeros(len(features_T))
v = np.zeros(len(features))
v_T = np.zeros(len(features_T))

# Cluster while incrementally adding a variable'''
for i in features: 
    communities_M, graph_M, Q_M = phenograph.cluster(df.loc[:,0:i], k=k_, primary_metric='Euclidean')
    communities_TM, graph_TM, Q_TM= phenograph.cluster(df_T.loc[:,0:i], k=k_, primary_metric='Euclidean')
    ari[i] = adjusted_rand_score(target,communities_M)
    ari_T[i] = adjusted_rand_score(target_T,communities_TM)
    v[i] = v_measure_score(target,communities_M)
    v_T[i] = v_measure_score(target_T,communities_TM)

ari = pd.Series(ari, index=features)
ari_T = pd.Series(ari_T, index=features_T)
v = pd.Series(v, index=features)
v_T = pd.Series(v_T, index=features_T)

#Save results for individual 1: 
#ari.to_csv('output/PhenoGraph_results/ari_patient1_DMLMJ_k=' + str(k_) + '.csv')
#ari_T.to_csv('output/PhenoGraph_results/ari_patient1_TDMLMJ_k=' + str(k_) + '.csv')
#v.to_csv('output/PhenoGraph_results/v_patient1_DMLMJ_k=' + str(k_) + '.csv')
#v_T.to_csv('output/PhenoGraph_results/v_patient1_TDMLMJ_k=' + str(k_) + '.csv')

#Save results for individual 2: 
ari.to_csv('output/PhenoGraph_results/ari_patient2_DMLMJ_k=' + str(k_) + '.csv')
ari_T.to_csv('output/PhenoGraph_results/ari_patient2_TDMLMJ_k=' + str(k_) + '.csv')
v.to_csv('output/PhenoGraph_results/v_patient2_DMLMJ_k=' + str(k_) + '.csv')
v_T.to_csv('output/PhenoGraph_results/v_patient2_TDMLMJ_k=' + str(k_) + '.csv')