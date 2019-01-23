#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 10:38:07 2018

@author: prubbens
"""

#Import packages
import pandas as pd
from sklearn.manifold import TSNE

#Data in Euclidean (=raw) representation
df_E = pd.read_table('output/Euclidean/test.txt', sep=',', index_col=None, header=None)
#Data transformed using DMLMJ
df_M = pd.read_table('output/DMLMJ/test.txt', sep=',', index_col=None, header=None)
features_E = list(df_E.columns)[:-1]
features_M = list(df_M.columns)[:-1]

#Import t-SNE
tsne = TSNE(n_components=2, perplexity=30.0, early_exaggeration=12.0, learning_rate=200.0, n_iter=1000, n_iter_without_progress=300, min_grad_norm=1e-07, metric='euclidean', init='pca', random_state=27, method='barnes_hut', angle=0.5)

#Perform dimensionality reduction using t-SNE and store dataframe
df_E_tsne = tsne.fit_transform(df_E.loc[:,features_E])
df_E_tsne = pd.DataFrame(df_E_tsne, columns=['t-SNE 1', 't-SNE 2'])
df_E_tsne.loc[:,'label'] = df_E.iloc[:,-1]
df_E_tsne.to_csv('output/TSNE/Euclidean_test_TSNE.csv')

df_M_tsne = tsne.fit_transform(df_M.loc[:,features_M])
df_M_tsne = pd.DataFrame(df_M_tsne, columns=['t-SNE 1', 't-SNE 2'])
df_M_tsne.loc[:,'label'] = df_M.iloc[:,-1]
df_M_tsne.to_csv('output/TSNE/DMLMJ_test_TSNE.csv')