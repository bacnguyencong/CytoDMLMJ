# Application 2: Mass Cytometry
DMLMJ was evaluated for CyTOF data.
### Dataset 2: 32-dimensional CyTOF Data
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
#### 2. t-SNE
Use the following code for t-SNE
```python
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
# write python code here...
```