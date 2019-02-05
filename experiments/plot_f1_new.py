#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 16:41:49 2018

@author: prubbens
"""
from io import StringIO
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("ticks")

def report_to_df(report):
    report = re.sub(r" +", " ", report).replace("avg / total", "avg/total").replace("\n ", "\n")
    report_df = pd.read_csv(StringIO("Classes" + report), sep=' ', index_col=0)        
    return(report_df)

df_13_E = pd.read_table('CyTOF_Levine13dim/output/Classification_report/Levine_13_E_cr.csv', sep=',', index_col=None, header=0)
df_13_E['Method'] = 'Euclidean'
df_13_E['Dataset'] = 'Levine_13dim'
mean_13_E = df_13_E.iloc[:-1,:].mean()
df_32_E = pd.read_table('CyTOF_Levine32dim/output/Classification_report/cr_E.csv', sep=',', index_col=None, header=0)
df_32_E['Method'] = 'Euclidean'
df_32_E['Dataset'] = 'Levine_32dim'
mean_32_E = df_32_E.iloc[:-1,:].mean()
df_hmis_E = pd.read_csv('CyTOF_HMIS2/data/Classification_report/cr_M.csv', index_col=0, header=0)
df_hmis_E['Method'] = 'Euclidean'
df_hmis_E['Dataset'] = 'HMIS-2'
mean_hmis_E = df_hmis_E.iloc[:-1,:].mean()

df_13_M = pd.read_table('CyTOF_Levine13dim/output/Classification_report/Levine_13_M_cr.csv', sep=',', index_col=None, header=0)
df_13_M['Method'] = 'DMLMJ'
df_13_M['Dataset'] = 'Levine_13dim'
mean_13_M = df_13_M.iloc[:-1,:].mean()
df_32_M = pd.read_table('CyTOF_Levine32dim/output/Classification_report/cr_M.csv', sep=',', index_col=None, header=0)
df_32_M['Method'] = 'DMLMJ'
df_32_M['Dataset'] = 'Levine_32dim'
mean_32_M = df_32_M.iloc[:-1,:].mean()
df_hmis_M = pd.read_csv('CyTOF_HMIS2/data/Classification_report/cr_M.csv', index_col=0, header=0)
df_hmis_M['Method'] = 'DMLMJ'
df_hmis_M['Dataset'] = 'HMIS-2'
mean_hmis_M = df_hmis_M.iloc[:-1,:].mean()

df = pd.concat([df_13_E,df_32_E,df_hmis_E,df_13_M,df_32_M,df_hmis_M], axis=0)
df.rename(index=str, columns={'f1-score': 'F1-score'}, inplace=True)
plt.figure() 
pal = sns.color_palette('colorblind')#[0:3:2]
g = sns.factorplot(x='Dataset', y='F1-score', data=df, hue='Method', kind='box', aspect=1.4, palette=pal)
g.set_titles(size=18)
g.set_xlabels(fontsize=16)
g.set_ylabels('F1-score', fontsize=16)
pal = sns.color_palette('cubehelix')[0:1]
plt.savefig('f1_score_class_husl.png',bbox_inches='tight', dpi=500)
plt.savefig('f1_score_class_husl.eps',bbox_inches='tight', dpi=500)
plt.show()