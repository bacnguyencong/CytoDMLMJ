#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 11:41:52 2018

@author: prubbens
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

df_dmlmj_cv = pd.read_csv('output/CD/V_k=30_CV.csv', index_col=0, header=0)
df_e = pd.read_csv('output/CD/V_k=30_E.csv', index_col=0, header=0)
df_e.columns = ['E']
df = pd.concat([df_dmlmj_cv,df_e], axis=1, ignore_index=False)

f, ax = plt.subplots(figsize=(16,16))
pal = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(df, cmap=pal, square=True, annot=True, xticklabels=True, yticklabels=True, linewidths=.5, cbar_kws={"shrink": .5}, ax=ax,  annot_kws={"size": 16})     
ax.tick_params(labelsize=16)
plt.savefig('Heatmap_PhenoGraph_Vmeasure.png', dpi=300, bbox_tight=True)

df_M = pd.DataFrame(np.diag(df_dmlmj_cv))
df_TM = []
for i in np.arange(0,df_dmlmj_cv.shape[0]): 
    for j in np.arange(0,df_dmlmj_cv.shape[1]): 
        if i != j: 
            df_TM.append(df_dmlmj_cv.iloc[i,j])
df_TM = pd.DataFrame(df_TM)

df_e.columns = ['V-measure']
df_e['Method'] = 'Euclidean'
df_M.columns = ['V-measure']
df_M['Method'] = 'DMLMJ'
df_TM.columns = ['V-measure']
df_TM['Method'] = 'T-DMLMJ'
df_ = pd.concat([df_e, df_M, df_TM], axis=0)

g = sns.factorplot(x='Method',y='V-measure',data=df_, kind='box', height=5, aspect=0.75, sharey=True, palette='colorblind',linewidth=2)
g.set_titles(size=20)
g.set_xlabels(fontsize=18)
g.set_ylabels(fontsize=18)
g.set(ylim=(0.5,1))
plt.savefig('V-measure.png',bbox_inches='tight', dpi=500)
