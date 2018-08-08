#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 16:41:49 2018

@author: prubbens
"""
import numpy as np
import pandas as pd
from sklearn.manifold import TSNE

np.random.seed(27)

df_13_E = pd.read_csv('Data/Application 2: CyTOF/Original/Levine_13dim/Levine_13dim_test_strat.csv', sep=',', index_col=0, header=0)
df_13_M = pd.read_table('Data/Application 2: CyTOF/DMLMJ/Levine_13dim/test.1', sep=',', index_col=None, header=None)
features_E = list(df_13_E.columns)[:-1]
features_M = list(df_13_M.columns)[:-1]

tsne = TSNE(n_components=2, perplexity=30.0, early_exaggeration=12.0, learning_rate=200.0, n_iter=1000, n_iter_without_progress=300, min_grad_norm=1e-07, metric='euclidean', init='pca', random_state=27, method='barnes_hut', angle=0.5)

df_13_E_tsne = tsne.fit_transform(df_13_E.loc[:,features_E])
df_13_E_tsne = pd.DataFrame(df_13_E_tsne, columns=['t-SNE 1', 't-SNE 2'])
df_13_E_tsne.loc[:,'label'] = df_13_E.iloc[:,-1]

df_13_M_tsne = tsne.fit_transform(df_13_M.loc[:,features_M])
df_13_M_tsne = pd.DataFrame(df_13_M_tsne, columns=['t-SNE 1', 't-SNE 2'])
df_13_M_tsne.loc[:,'label'] = df_13_M.iloc[:,-1]

#df_13_E_tsne.to_csv('TSNE_13_E_test_perp30.csv')
#df_13_M_tsne.to_csv('TSNE_13_M_all_test_perp30.csv')