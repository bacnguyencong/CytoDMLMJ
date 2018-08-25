# Application 1: Synthetic microbial communities
## Dataset 1: In Silico Bacterial Communities
The data can be found in the folder ``experiments/Application_1+Dataset_1/data/``.
The results can be found in the folder ``experiments/Application_1+Dataset_1/output/``
### Usage
within the Malab console, go to ``experiments/Application_1+Dataset_1/`` by
```matlab
cd experiments/Application_1+Dataset_1/
```
##### 1. To reproduce the results on raw data
Within the Malab console, run the following command
```matlab
runExps(0)
```
In the folder ``output``, the following files will be generated
- ``supervised.txt``:
- ``partialsupervised.txt``:
- ``unsupervised.txt``:

##### 2. To reproduce the results on transformed data
Within the Malab console, run the following command
```matlab
runExps(1)
```
In the folder ``output``, the following files will be generated
- ``asinh_supervised.txt``:
- ``asinh_partialsupervised.txt``:
- ``asinh_unsupervised.txt``: