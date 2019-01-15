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
df_M = pd.read_csv('Output_TDMLMJ/DMLMJ/DMLMJ_' + str(patient_id), index_col=None, header=None)
labels = pd.read_csv('Labels_test_CD_CTRL_HMIS2.csv', index_col=0, header=0)
for i in np.arange(0,28): 
    labels.ix[np.int(i*10000):np.int((i+1)*10000),'Sample ID'] = i+1

features_M = list(df_M.columns[:-1])

communities_M, graph_M, Q_M = phenograph.cluster(df_M.loc[:,features_M], k=30)

labels['PhenoGraph_M'] = communities_M

ct_M = pd.crosstab(labels.loc[:,'Sample ID'],labels.loc[:,'PhenoGraph_M'], normalize=True)

wrs_M = np.zeros(len(ct_M.columns))
p_wrs_M = np.zeros(len(ct_M.columns))

for cluster in ct_M.columns: 
    wrs_M[cluster], p_wrs_M[cluster] = stats.mannwhitneyu(ct_M.iloc[0:14,cluster],ct_M.iloc[14:,cluster])
    
q_wrs_M = multipletests(p_wrs_M,method='fdr_bh')[1]    

results_M = pd.DataFrame({'WRS':wrs_M,'P':p_wrs_M,'Q':q_wrs_M})

ct_hmis2_M = pd.crosstab(labels.loc[:,'Cell population'],labels.loc[:,'PhenoGraph_M'], normalize=True)
v_M = v_measure_score(labels.loc[:,'Cell population'],labels.loc[:,'PhenoGraph_M'])

labels.to_csv('META_PhenoGraph/Labels_PhenoGraph_results_macro_id' + str(patient_id) + '.csv')
results_M.to_csv('META_PhenoGraph/P_vals_M_PhenoGraph_f1_macro_id' + str(patient_id) + '.csv')