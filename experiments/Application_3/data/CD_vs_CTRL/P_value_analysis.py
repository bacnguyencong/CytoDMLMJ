#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 11:44:32 2018

@author: prubbens
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

df_E = pd.read_csv('P_vals/P_vals_E_PhenoGraph_id1.csv', index_col=0, header=0)
df_E['Method'] = 'Euclidean'
df_M_id1 = pd.read_csv('P_vals/P_vals_M_PhenoGraph_id1.csv', index_col=0, header=0)
df_M_id1['Method'] = 'DMLMJ(id 1)'
df_M_id9 = pd.read_csv('P_vals/P_vals_M_PhenoGraph_id9.csv', index_col=0, header=0)
df_M_id9['Method'] = 'DMLMJ(id 9)'
df_M_id14 = pd.read_csv('P_vals/P_vals_M_PhenoGraph_id14.csv', index_col=0, header=0)
df_M_id14['Method'] = 'DMLMJ(id 14)'
df_M_id19 = pd.read_csv('P_vals/P_vals_M_PhenoGraph_id19.csv', index_col=0, header=0)
df_M_id19['Method'] = 'DMLMJ(id 19)'
df_M_id20 = pd.read_csv('P_vals/P_vals_M_PhenoGraph_id20.csv', index_col=0, header=0)
df_M_id20['Method'] = 'DMLMJ(id 20)'
df_M_id22 = pd.read_csv('P_vals/P_vals_M_PhenoGraph_id22.csv', index_col=0, header=0)
df_M_id22['Method'] = 'DMLMJ(id 22)'

dfs = [df_E,df_M_id1,df_M_id9,df_M_id14,df_M_id19,df_M_id20,df_M_id22]
n_of_clusters = np.zeros(len(dfs))
n_of_sign_clusters = np.zeros(len(dfs))
n_of_not_sign_clusters = np.zeros(len(dfs))

i=0
for dfs_ in dfs: 
    n_of_clusters[i] = dfs_.shape[0]
    i+=1

i=0
df = pd.concat(dfs,axis=0)
for dfs_ in dfs: 
    dfs_ = dfs_[dfs_.Q <= 0.05]
    n_of_sign_clusters[i] = dfs_.shape[0]
    n_of_not_sign_clusters = n_of_clusters[i] - n_of_sign_clusters[i]
    i+=1

df_bar = pd.DataFrame({'Number of clusters':n_of_clusters,'Number of significant clusters':n_of_sign_clusters,'Not significant':n_of_not_sign_clusters, 'Method':df.Method.unique()}, index=df.Method.unique())
g = sns.catplot(x='Method', y='Q', data=df, kind='swarm', color='dimgray', aspect=1.5)
g.set_xlabels(fontsize=18)
g.set_ylabels(fontsize=18)
plt.savefig('Swarmplot_Pvals.png', dpi=300, bbox_tight=True)

g = sns.catplot(x='Method', y='Number of clusters', data=df_bar, kind='bar', color='dimgray', aspect=1.5)
g.set_xlabels(fontsize=18)
g.set_ylabels(fontsize=18)
plt.savefig('Number_of_Clusters_metaPhenoGraph.png', dpi=300, bbox_tight=True)

g = sns.catplot(x='Method', y='Number of significant clusters', data=df_bar, kind='bar', color='dimgray', aspect=1.5)
g.set_xlabels(fontsize=18)
g.set_ylabels(fontsize=18)
plt.savefig('Number_of_Significant_Clusters_metaPhenoGraph.png', dpi=300, bbox_tight=True)