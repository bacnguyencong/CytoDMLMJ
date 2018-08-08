#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 16:41:49 2018

@author: prubbens
"""
import numpy as np
import pandas as pd
import phenograph
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import v_measure_score, adjusted_rand_score

'''Import DMLMJ ('df_32_M') and T-DMLMJ ('df_32_TM') transformed data'''
df_32_M = pd.read_table('Phenograph_clustering/full-output/DMLMJ/full_test.2', sep=',', index_col=None, header=None)
df_32_TM = pd.read_table('Phenograph_clustering/transfer/DMLMJ/test.1.2', sep=',', index_col=None, header=None)

'''Variables to use, leave cell population label out'''
features_M = list(df_32_M.columns)[:-1]
features_TM = list(df_32_TM.columns)[:-1]

target_M = df_32_M.iloc[:,-1]
target_TM = df_32_TM.iloc[:,-1]

'''Hyperparameter k of the PhenoGraph algorithm'''
k_ = 60

'''Arrays to store performance measures; ari: Adjusted Rand Index, v: V-measure'''
ari_M = np.zeros(len(features_M))
ari_TM = np.zeros(len(features_TM))
v_M = np.zeros(len(features_M))
v_TM = np.zeros(len(features_TM))

'''Cluster while incrementally adding a variable'''
for i in features_M: 
    communities_M, graph_M, Q_M = phenograph.cluster(df_32_M.loc[:,0:i], k=k_, primary_metric='Euclidean')
    communities_TM, graph_TM, Q_TM= phenograph.cluster(df_32_TM.loc[:,0:i], k=k_, primary_metric='Euclidean')
    ari_M[i] = adjusted_rand_score(target_M,communities_M)
    ari_TM[i] = adjusted_rand_score(target_TM,communities_TM)
    v_M[i] = v_measure_score(target_M,communities_M)
    v_TM[i] = v_measure_score(target_TM,communities_TM)

ari_M = pd.Series(ari_M, index=features_M)
ari_TM = pd.Series(ari_TM, index=features_M)
v_M = pd.Series(v_M, index=features_M)
v_TM = pd.Series(v_TM, index=features_M)

ari_M.to_csv('050618/Results/Phenograph/ari_patient2_M_k=' + str(k_) + '.csv')
ari_TM.to_csv('050618/Results/Phenograph/ari_patient2_TM_k=' + str(k_) + '.csv')
v_M.to_csv('050618/Results/Phenograph/v_patient2_M_k=' + str(k_) + '.csv')
v_TM.to_csv('050618/Results/Phenograph/v_patient2_TM_k=' + str(k_) + '.csv')