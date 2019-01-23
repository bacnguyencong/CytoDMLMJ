#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 10:49:28 2018

@author: prubbens
"""

#import packages
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_style("ticks")

#Import results
df_E = pd.read_csv('output/TSNE/Euclidean_test_TSNE.csv', index_col=0, header=0)
df_E['Method'] = 'Euclidean'
df_M = pd.read_csv('output/TSNE/DMLMJ_test_TSNE.csv', sep=',', index_col=0, header=0)
df_M['Method'] = 'DMLMJ'

#Match integer label with cell population
labels = pd.read_table('attachments/population_names_Levine_13dim.txt', index_col=None, header=0)
for df in [df_E,df_M]:
    for i in labels.label: 
        df.loc[:,'label'].replace(to_replace=i, value=labels.loc[i-1,'population'], inplace=True)     

#Concat files and sort according to cell population
df = pd.concat([df_E,df_M], axis=0)
df.sort_values('label', inplace=True)

#Plot figure and save
plt.figure() 
pal = sns.color_palette('husl',24)
g = sns.lmplot(x='t-SNE 1', y='t-SNE 2', data=df, hue = 'label', col = 'Method', col_order=['Euclidean','DMLMJ'], fit_reg=False, aspect=1.2, palette=pal, legend=True)
g.set_titles(size=20)
g.set_xlabels('t-SNE 1 (a.u.)', fontsize=16)
g.set_ylabels('t-SNE 2 (a.u.)', fontsize=16)
g.set_xticklabels(fontsize=14) #rotation=-90, ha='left'
g.set_yticklabels(fontsize=14) #rotation=-90, ha='left'
plt.savefig('TSNE_test.eps',bbox_inches='tight', dpi=500)
plt.show()
