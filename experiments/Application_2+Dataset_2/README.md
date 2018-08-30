# Application 2: Mass Cytometry
DMLMJ was evaluated for CyTOF data.
### Dataset 2: 32-dimensional CyTOF Data
Data originate from two healthy individuals, in which bone marrow mast cells (BMMCs) were analyzed using a 32-color panel. Cell populations were labeled after manual gating using all markers; all markers were used for data analysis. This dataset as processed by [1] is publicly available on [FlowRepository (ID: ID: FR-FCM-ZZPH)](https://flowrepository.org/experiments/817). 

The data can be found in the folder ``experiments/Application_2+Dataset_2/data/``.
The results can be found in the folder ``experiments/Application_2+Dataset_2/output/``
### Usage
#### 1. Run experiments
within the Malab console, go to ``experiments/Application_2+Dataset_2/`` by
```matlab
cd experiments/Application_2+Dataset_2/
```
and run the command
```matlab
runExps()
```
The ``output`` folder contains two folders ``Euclidean`` and ``DMLMJ``, which are the output files of `k`-NN classifier using the Euclidean and DMLMJ, respectively. 
- ``train.1.txt``:  The training data set (the last column corresponds to the labels) of patient ID1. For DMLMJ, the data are transformed using the learned transformation ``L``.
- ``train.2.txt``:  The training data set (the last column corresponds to the labels) of patient ID2. For DMLMJ, the data are transformed using the learned transformation ``L``.
- ``test.1.txt``: The test data set (the last column corresponds to the labels) of patient ID1. For DMLMJ, the data are transformed using the learned transformation ``L``.
- ``test.2.txt``: The test data set (the last column corresponds to the labels) of patient ID2. For DMLMJ, the data are transformed using the learned transformation ``L``.
- ``prediction.1.txt``: A file contains two columns that represent the predicted labels and the true labels, respectively (with patient ID1).
- ``prediction.2.txt``: A file contains two columns that represent the predicted labels and the true labels, respectively (with patient ID2).
- ``train_all.1.txt``: The training data set after applying the linear transformation learned by DMLMJ (all variables are kept, patient ID1).
- ``train_all.2.txt``: The training data set after applying the linear transformation learned by DMLMJ (all variables are kept, patient ID2).
- ``test_all.1.txt``: The test data set after applying the linear transformation learned by DMLMJ (all variables are kept, patient ID1).
- ``test_all.2.txt``: The test data set after applying the linear transformation learned by DMLMJ (all variables are kept, patient ID2).
- ``test.1.2.txt``: Train on the first and test on the second patient.
- ``test.2.1.txt``: Train on the second and test on the first patient.

#### 2. PhenoGraph analysis
PhenoGraph was used to perform cluster analysis and evaluate the influence of DMLMJ. The python implementation of PhenoGraph was used, which can be downloaded and installed from this [repository](https://github.com/jacoblevine/PhenoGraph). The code has also been added to this repository, see directory [phenograph](). 

Variables were incrementally added, in order to determine the optimal number of variables that is needed for clustering. Note that for this analysis, files are used which contain all of the variables (denoted with `_all` in the title). 

```python
# Import packages
import numpy as np
import pandas as pd
import phenograph
from sklearn.metrics import v_measure_score, adjusted_rand_score

# Import DMLMJ ('df') and T-DMLMJ ('df_T') transformed data for patient 1'''
df = pd.read_table('output/DMLMJ/test_all.1.txt', sep=',', index_col=None, header=None)
df_T = pd.read_table('output/DMLMJ/test_all.2.1.txt', sep=',', index_col=None, header=None)

# Import DMLMJ ('df') and T-DMLMJ ('df_T') transformed data for patient 2'''
#df = pd.read_table('output/DMLMJ/test_all.2.txt', sep=',', index_col=None, header=None)
#df_T = pd.read_table('output/DMLMJ/test_all.2.1.txt', sep=',', index_col=None, header=None)

'''Variables to use, leave cell population label out'''
features = list(df.columns)[:-1]
features_T = list(df_T.columns)[:-1]

target = df.iloc[:,-1]
target_T = df_T.iloc[:,-1]

# Hyperparameter k of the PhenoGraph algorithm'''
k_ = 30

# Arrays to store performance measures; ari: Adjusted Rand Index, v: V-measure'''
ari = np.zeros(len(features))
ari_T = np.zeros(len(features_T))
v = np.zeros(len(features))
v_T = np.zeros(len(features_T))

# Cluster while incrementally adding a variable'''
for i in features: 
    communities_M, graph_M, Q_M = phenograph.cluster(df.loc[:,0:i], k=k_, primary_metric='Euclidean')
    communities_TM, graph_TM, Q_TM= phenograph.cluster(df_T.loc[:,0:i], k=k_, primary_metric='Euclidean')
    ari[i] = adjusted_rand_score(target,communities_M)
    ari_T[i] = adjusted_rand_score(target_T,communities_TM)
    v[i] = v_measure_score(target,communities_M)
    v_T[i] = v_measure_score(target_T,communities_TM)

ari = pd.Series(ari, index=features)
ari_T = pd.Series(ari_T, index=features_T)
v = pd.Series(v, index=features)
v_T = pd.Series(v_T, index=features_T)

#Save results for individual 1: 
ari.to_csv('output/PhenoGraph_results/ari_patient1_DMLMJ_k=' + str(k_) + '.csv')
ari_T.to_csv('output/PhenoGraph_results/ari_patient1_TDMLMJ_k=' + str(k_) + '.csv')
v.to_csv('output/PhenoGraph_results/v_patient1_DMLMJ_k=' + str(k_) + '.csv')
v_T.to_csv('output/PhenoGraph_results/v_patient1_TDMLMJ_k=' + str(k_) + '.csv')

#Save results for individual 2: 
#ari.to_csv('output/PhenoGraph_results/ari_patient2_DMLMJ_k=' + str(k_) + '.csv')
#ari_T.to_csv('output/PhenoGraph_results/ari_patient2_TDMLMJ_k=' + str(k_) + '.csv')
#v.to_csv('output/PhenoGraph_results/v_patient2_DMLMJ_k=' + str(k_) + '.csv')
#v_T.to_csv('output/PhenoGraph_results/v_patient2_TDMLMJ_k=' + str(k_) + '.csv')
```

#### 3. Visualization of results
Values reported in Table 1 are gathered from the files in [PhenoGraph_results_paper](). Fig. 5 can be generated using the script [plot_pheno.py](): 

```python
#Import packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_style("ticks")

#Read in output
v_I1_M = pd.read_csv('output/PhenoGraph_results_paper/v_patient1_M_k=30.csv', index_col=0, header=None)
v_I1_M.loc[:,'D'] = np.arange(1,33)
v_I1_M['ID'] = '1'
v_I1_M['method'] = 'DMLMJ'
v_I1_TM = pd.read_csv('output/PhenoGraph_results_paper/v_patient1_TM_k=30.csv', index_col=0, header=None)
v_I1_TM.loc[:,'D'] = np.arange(1,33)
v_I1_TM['ID'] = '1'
v_I1_TM['method'] = 'T-DMLMJ'
v_I2_M = pd.read_csv('output/PhenoGraph_results_paper/v_patient2_M_k=30.csv', index_col=0, header=None)
v_I2_M.loc[:,'D'] = np.arange(1,33)
v_I2_M['ID'] = '2'
v_I2_M['method'] = 'DMLMJ'
v_I2_TM = pd.read_csv('output/PhenoGraph_results_paper/v_patient2_TM_k=30.csv', index_col=0, header=None)
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
```
