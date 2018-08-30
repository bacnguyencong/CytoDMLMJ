#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 16:49:12 2018

@author: prubbens
"""

#Import packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_style("ticks")

#Read in output
v_I1_M = pd.read_csv('output/Phenograph_results_paper/v_patient1_M_k=30.csv', index_col=0, header=None)
v_I1_M.loc[:,'D'] = np.arange(1,33)
v_I1_M['ID'] = '1'
v_I1_M['method'] = 'DMLMJ'
v_I1_TM = pd.read_csv('output/Phenograph_results_paper/v_patient1_TM_k=30.csv', index_col=0, header=None)
v_I1_TM.loc[:,'D'] = np.arange(1,33)
v_I1_TM['ID'] = '1'
v_I1_TM['method'] = 'T-DMLMJ'
v_I2_M = pd.read_csv('output/Phenograph_results_paper/v_patient2_M_k=30.csv', index_col=0, header=None)
v_I2_M.loc[:,'D'] = np.arange(1,33)
v_I2_M['ID'] = '2'
v_I2_M['method'] = 'DMLMJ'
v_I2_TM = pd.read_csv('output/Phenograph_results_paper/v_patient2_TM_k=30.csv', index_col=0, header=None)
v_I2_TM.loc[:,'D'] = np.arange(1,33)
v_I2_TM['ID'] = '2'
v_I2_TM['method'] = 'T-DMLMJ'

v = pd.concat([v_I1_M,v_I1_TM,v_I2_M,v_I2_TM], axis=0)
v.rename(index=str, columns={1: "V-measure"}, inplace=True)

#Plot figure: 
plt.figure() 
pal = sns.color_palette('husl',2)
g = sns.lmplot(x='D', y='V-measure', data=v, hue = 'method', col = 'ID', fit_reg=False, aspect=1, palette=pal, legend=True)
g.set_titles(size=20)
g.set_xlabels(fontsize=16)
g.set_ylabels(fontsize=16)
g.set_xticklabels(fontsize=14) #rotation=-90, ha='left'
g.set_yticklabels(fontsize=14) #rotation=-90, ha='left'
plt.savefig('V_CyTOF.eps',bbox_inches='tight', dpi=500)
plt.show()