# Application 1: Synthetic microbial communities
## Dataset 1: In Silico Bacterial Communities
The data can be found in the folder ``experiments/Application_1+Dataset_1/data/``.
The results can be found in the folder ``experiments/Application_1+Dataset_1/output/``
### Usage
within the Malab console, go to ``experiments/Application_1+Dataset_1/`` by
```matlab
cd experiments/Application_1+Dataset_1/
```
##### 1. Experiments on the raw data
Within the Malab console, run the following command
```matlab
runExps(0)
```
We report the accuracies of the `k`-NN classifier using the Euclidean and the Mahalanobis distances, respectively, in the folder ``output``. More specifically, the following files will be generated:

- ``supervised.txt``: This corresponds the supervised settings. Each row represents the results with respect to different values of the species richness ``S``, which is increased from 2 to 10.

- ``partialsupervised.txt``: This corresponds the partial transfer DMLMJ settings. DMLMJ was applied at every step using the community that was only partially present in
the target community (10 microbial populations). Each row represents the results with respect to different values of ``T`` (number of microbial populations that was used to perform DMLMJ), which is increased from 2 to 10.
- ``unsupervised.txt``: This corresponds the transfer DMLMJ settings. DMLMJ was applied using microbial populations of which none were part of the target communities. As the target communities contained ten bacterial populations, the remaining populations were used to determine the distance metric through DMLMJ for ``T`` from 2 to 10.

We repeat the experiment 10 times to avoid the effect of randomness (in total 90 rows for each file).
##### 2. Experiments on the transformed data
The results of ``k``-NN classification on data transformed by ``f(x)=asinh(x)``. Within the Malab console, run the following command
```matlab
runExps(1)
```
In the folder ``output``, the following files will be generated
- ``asinh_supervised.txt``: This corresponds the supervised settings.
- ``asinh_partialsupervised.txt``: This corresponds the partial transfer DMLMJ settings.
- ``asinh_unsupervised.txt``: This corresponds the transfer DMLMJ settings.

All files have the same structure as in ``Experiments on the raw data``.

#### 3. Making figures
The python script to make Fig. 1(a) can be found from [here](make_figure.py)