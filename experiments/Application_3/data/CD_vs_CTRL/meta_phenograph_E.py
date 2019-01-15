#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 09:42:57 2018

@author: prubbens
"""
import numpy as np
import pandas as pd
import phenograph
#import seaborn as sns

from scipy import stats
from sklearn.metrics import v_measure_score
from statsmodels.stats.multitest import multipletests

patient_id = [1,9,14,19,20,22][5]
df_E = pd.read_csv('CD_vs_CTRL/Output_TDMLMJ/Euclidean/Euclidean_' + str(patient_id), index_col=None, header=None)
labels = pd.read_csv('CD_vs_CTRL/Labels_test_CD_CTRL_HMIS2.csv', index_col=0, header=0)
for i in np.arange(0,28): 
    labels.ix[np.int(i*10000):np.int((i+1)*10000),'Sample ID'] = i+1

features_E = list(df_E.columns[:-1])
communities_E, graph_E, Q_E = phenograph.cluster(df_E.loc[:,features_E], k=30)
labels['PhenoGraph_E'] = communities_E

ct_E = pd.crosstab(labels.loc[:,'Sample ID'],labels.loc[:,'PhenoGraph_E'], normalize=True)
wrs_E = np.zeros(len(ct_E.columns))
p_wrs_E = np.zeros(len(ct_E.columns))

for cluster in ct_E.columns: 
    wrs_E[cluster], p_wrs_E[cluster] = stats.mannwhitneyu(ct_E.iloc[0:14,cluster],ct_E.iloc[14:,cluster])
    
q_wrs_E = multipletests(p_wrs_E,method='fdr_bh')[1]    

results_E = pd.DataFrame({'WRS':wrs_E,'P':p_wrs_E,'Q':q_wrs_E})

ct_hmis2_E = pd.crosstab(labels.loc[:,'Cell population'],labels.loc[:,'PhenoGraph_E'], normalize=True)
v_E = v_measure_score(labels.loc[:,'Cell population'],labels.loc[:,'PhenoGraph_E'])

labels.to_csv('META_PhenoGraph/Labels_PhenoGraph_results_macro_id' + str(patient_id) + '.csv')
results_E.to_csv('META_PhenoGraph/P_vals_E_PhenoGraph_f1_macro_id' + str(patient_id) + '.csv')