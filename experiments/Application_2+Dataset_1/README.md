# Application 2: Mass Cytometry
DMLMJ was evaluated for CyTOF data.
### Dataset 1: 13-dimensional CyTOF Data
Data originate from one healthy individual, in which bone marrow mast cells (BMMCs) were analyzed using a 13-color panel. Cell populations were labeled after manual gating using all markers; all markers were used for data analysis. This dataset as processed by [1] is publicly available on FlowRepository (ID:FR-FCM-ZZPH).

The data can be found in the folder ``experiments/Application_2+Dataset_1/data/``.
The results can be found in the folder ``experiments/Application_2+Dataset_1/output/``
### Usage
#### 1. Run experiments
within the Malab console, go to ``experiments/Application_2+Dataset_1/`` by
```matlab
cd experiments/Application_2+Dataset_1/
```
and run the command
```matlab
runExps()
```
The ``output`` folder contains two folders ``Euclidean`` and ``DMLMJ``, which are the output files of `k`-NN classifier using the Euclidean and DMLMJ, respectively. 
- ``train.txt``:  The training data set (the last column corresponds to the labels). For DMLMJ, the data are transformed using the learned transformation ``L``. The number of variables is reduced as determined by cross-validation. 
- ``test.txt``: The test data set (the last column corresponds to the labels). For DMLMJ, the data are transformed using the learned transformation ``L``. The number of variables is reduced as determined by cross-validation. 
- ``prediction.txt``: A file contains two columns that represent the predicted labels and the true labels, respectively.
- ``train_all.txt``: The training data set after applying the linear transformation learned by DMLMJ (all variables are kept).
- ``test_all.txt``: The test data set after applying the linear transformation learned by DMLMJ (all variables are kept).

#### 2. t-SNE
This script can also be accessed via the file [tsne.py](). 
```python
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
```

### Visualizing t-SNE Results 
This script can also be accessed via the file [plot_tsne.py](). 
```python 
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
plt.savefig('Figures/TSNE_E_test.eps',bbox_inches='tight', dpi=500)
plt.show()
```
### References
[1] Weber, L.M., and Robinson, M.D., "Comparison of clustering methods for high‐dimensional single‐cell flow and mass cytometry data". Cytometry Part A 89A: 1084-1096, 2016. 