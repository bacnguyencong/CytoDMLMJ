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
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import v_measure_score, accuracy_score
from sklearn.model_selection import LeaveOneOut
from statsmodels.stats.multitest import multipletests

patient_id = [1,9,14,19,20,22][0]
df_E = pd.read_csv('Output_TDMLMJ/Euclidean/Euclidean_' + str(patient_id), index_col=None, header=None)
labels = pd.read_csv('Labels_test_CD_CTRL_HMIS2.csv', index_col=0, header=0)
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

labels = np.concatenate((np.zeros(14),np.ones(14)),axis=None)
lda = LinearDiscriminantAnalysis()
loo = LeaveOneOut()
test_fold_predictions = []

for train_index, test_index in loo.split(ct_E):
    X_train, X_test = ct_E.iloc[train_index,:], ct_E.iloc[test_index,:]
    y_train, y_test = labels[train_index], labels[test_index]
    lda.fit(X_train, y_train)
    test_fold_predictions.append(lda.predict(X_test))
    
acc = accuracy_score(labels,test_fold_predictions)

#labels.to_csv('META_PhenoGraph/Labels_PhenoGraph_results_macro_id' + str(patient_id) + '.csv')
#results_E.to_csv('META_PhenoGraph/P_vals_E_PhenoGraph_f1_macro_id' + str(patient_id) + '.csv')