# Application 2: Mass Cytometry
DMLMJ was evaluated for CyTOF data.
### Dataset 1: 13-dimensional CyTOF Data
Data originate from one healthy individual, in which bone marrow mast cells (BMMCs) were analyzed using a 13-color panel. Cell populations were labeled after manual gating using all markers; all markers were used for data analysis. This dataset as processed by [1] is publicly available on FlowRepository (ID:FR-FCM-ZZPH).

The data can be found in the folder ``experiments/Application_2+Dataset_1/data/``.
The results can be found in the folder ``experiments/Application_2+Dataset_1/output/``
### Usage
within the Malab console, go to ``experiments/Application_2+Dataset_1/`` by
```matlab
cd experiments/Application_2+Dataset_1/
```
and run the command
```matlab
runExps()
```
### References
[1] Weber, Lukas M., and Mark D. Robinson. "Comparison of clustering methods for high‐dimensional single‐cell flow and mass cytometry data." Cytometry Part A 89.12 (2016): 1084-1096.