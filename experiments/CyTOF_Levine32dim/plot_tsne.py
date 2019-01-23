#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 16:49:12 2018

@author: prubbens
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_style("ticks")

df_32_E = pd.read_csv('output/TSNE/TSNE_32_E.csv', index_col=0)
df_32_E['Method'] = 'Euclidean'
df_32_M = pd.read_csv('output/TSNE/TSNE_32_M.csv', index_col=0)
df_32_M['Method'] = 'DMLMJ'   

labels = pd.read_table('data/population_names_Levine_32dim.txt', index_col=None, header=0)
for df in [df_32_E,df_32_M]:
    for i in labels.label: 
        df.loc[:,'label'].replace(to_replace=i, value=labels.loc[i-1,'population'], inplace=True)

df_32 = pd.concat([df_32_E,df_32_M], axis=0)
df_32.sort_values('label', inplace=True)

plt.figure() 
pal = sns.color_palette('husl',14)
g = sns.lmplot(x='t-SNE 1', y='t-SNE 2', data=df_32, hue = 'label', col = 'Method', col_order=['Euclidean','DMLMJ'], fit_reg=False, aspect=1.2, palette=pal, legend=True)
#g.fig.suptitle('Dataset = Levine et al. (2015) -- DML', size=22)
g.set_titles(size=20)
#g.set_axis_labels('Number of taxa',r'$R^2_{CV}$')
g.set_xlabels('t-SNE 1 (a.u.)', fontsize=16)
g.set_ylabels('t-SNE 2 (a.u.)', fontsize=16)
g.set_xticklabels(fontsize=14) #rotation=-90, ha='left'
g.set_yticklabels(fontsize=14) #rotation=-90, ha='left'
plt.savefig('TSNE_32_test.png',bbox_inches='tight', dpi=500)
#plt.savefig('TSNE_32_test.eps',bbox_inches='tight', dpi=500)
plt.show()
