# Mass Cytometry
DMLMJ was evaluated for HMIS-2 data.  
### Dataset 3: HMIS-2
The HMIS-2 dataset, studying the Human Mucosal Immune System (HMIS), originates from 47 individuals, in which peripheral blood mononuclear cells (PBMCs) were analyzed through CyTOF using a 28-color panel. The dataset was originally published in [1]. This data set is publicly available on [FlowRepository (ID:FR-FCM-ZYRM)](https://flowrepository.org/experiments/1910). First we only looked at samples diagnosed with Crohn's Disease (CD, $n = 14$).

The data can be found in the folder ``experiments/CyTOF_HMIS2/data/``.
The results can be found in the folder ``experiments/CyTOF_HMIS2/output/``
### Usage
#### 1. Run experiments
within the Malab console, go to ``experiments/CyTOF_HMIS2/`` by
```matlab
cd experiments/CyTOF_HMIS2/
```
and run the command
```matlab
runExps()
```

Cells were clustered using the Euclidean distance metric or using DMLMJ. These files can be found in ``experiments/CyTOF_HMIS2/output/CD/Euclidean/`` and ``experiments/CyTOF_HMIS2/output/CD/DMLMJ/`` respectively. The latter contains samples denoted by $i.j$, in which $i$ denotes the sample ID which was used for DMLMJ to next quantify distances of cells in sample $j$. Scripts to cluster all samples individually are ``phenograph_E.py` and ``phenograph_DMLMJ.py``. Scripts are also added to visualize figures [4A and B](https://github.com/bacnguyencong/CytoDMLMJ/blob/master/experiments/CyTOF_HMIS2/plot_heatmap.py) and [4C](https://github.com/bacnguyencong/CytoDMLMJ/blob/master/experiments/CyTOF_HMIS2/plot_N_clusters.py).

An example to determine cell populations using PhenoGraph for $i = 3$ and $j = 5$ after DMLMJ, is as follows: 

```python 

import numpy as np
import pandas as pd
import phenograph

from os import listdir
from sklearn.metrics import v_measure_score, adjusted_rand_score

PATH_M = 'output/CD/DMLMJ/CV/'
FILENAMES = sorted(listdir(PATH_M))
k_=30 
ari = np.zeros((14,14))
v = np.zeros((14,14))
n_clusters = np.zeros((14,14))
index = []

i=3
j=5
df = pd.read_table(PATH_M+str(i)+'.'+str(j), sep=',', index_col=None, header=None)
features = list(df.columns)[:-1]
target = df.iloc[:,-1]
communities, graph, Q = phenograph.cluster(df.loc[:,features], k=k_, primary_metric='Euclidean')
ari[i-1,j-1] = adjusted_rand_score(target,communities)
v[i-1,j-1] = v_measure_score(target,communities)
n_clusters[i-1,j-1] = len(np.unique(communities))

ari = pd.DataFrame(ari,index=np.arange(1,15), columns=np.arange(1,15))
v = pd.DataFrame(v,index=np.arange(1,15), columns=np.arange(1,15))
n_clusters = pd.DataFrame(n_clusters,index=np.arange(1,15), columns=np.arange(1,15))

ari.to_csv('output/CD/ARI_k='+str(k_)+'_CV_rerun.csv')
v.to_csv('output/CD/V_k='+str(k_)+'_CV_rerun.csv')
n_clusters.to_csv('output/CD/N_clusters_k='+str(k_)+'_CV_rerun.csv')

### References
[1] [V. van Unen, N. Li, I. Molendijk, M. Temurhan, T. Höllt, A. E., van der Meulen-de Jong, H. W. Verspaget, M. L. Mearin, C. J., Mulder, J. van Bergen, B. P. Lelieveldt, F. Koning. "Mass Cytometry of the Human Mucosal Immune System Identifies Tissue- and Disease-Associated Immune Subsets", Immunity 44 (5) (2016) 1227–1239](https://www.cell.com/immunity/fulltext/S1074-7613(16)30143-1)