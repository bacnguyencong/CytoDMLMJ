# Learning Single-Cell Distances from Cytometry Data
This repository accompanies the manscript "*Learning Single-Cell Distances from Cytometry Data*" by [B. Nguyen](https://github.com/bacnguyencong), [P. Rubbens](https://github.com/prubbens), [F.-M. Kerckhof](https://github.com/FMKerckhof), N. Boon, B. De Baets and W. Waegeman. 

It explores the functionality of distance metric learning through maximization of the Jeffrey divergence (DMLMJ) for different cytometry applications (synthetic microbial ecology and CyTOF). 

## ABSTRACT: 
Data analysis techniques for the automated identification of cell populations are witnessing an increased interest in the field of cytometry. These techniques commonly depend on a distance metric to measure similarities between single cells. In this study, we explore the use of distance metric learning to automatically determine a generalized form of the Euclidean distance metric, the so-called Mahalanobis distance metric. This approach can be used in cases where single-cell labels are available. We evaluate the potential of a learned distance metric in various ways. First, we show that current distance-based methods can be improved upon by implementing an appropriate Mahalanobis distance metric. Then, to evaluate the robustness of such a distance metric, we evaluate the transferability of a Mahalanobis distance metric between samples. In addition, we show that a learned distance metric can be integrated with unsupervised methods, such as clustering or dimensionality reduction. In particular, the approach is illustrated for cytometry data from two different origins, i.e.\ flow cytometry applied to microbial cells and mass cytometry for the analysis of human blood cells. Results indicate that a learned distance metric improves cell population identification. It is a robust property of a specific cytometry setup, meaning that a learned distance metric can be transferred between samples. Therefore, it can provide a useful way to incorporate domain knowledge into a downstream multivariate analysis and address sources of variability to some extent. 

## Structure: 
* Examples and code to reproduce the results can be found in the directory [experiments](https://github.com/bacnguyencong/CytoDMLMJ/tree/master/experiments), per application and dataset (four different directories in total). 
* Figures of the manuscript can be found in [figs](https://github.com/bacnguyencong/CytoDMLMJ/tree/master/figs). 
* Original codes to run `DMLMJ` can be found as well in the directory [algorithms/DMLMJ](https://github.com/bacnguyencong/CytoDMLMJ/tree/master/algorithms/DMLMJ). 

## Datasets:
Four different datasets were used. Links and FlowRepository IDs to original publications are the following: 
* [Rubbens et al. 2017](https://onlinelibrary.wiley.com/doi/abs/10.1002/cyto.a.23284) (FlowRepository ID: FR-FCM-ZY6M),
* [Sgier et al. 2016](https://www.nature.com/articles/ncomms11587) (FlowRepository ID: FR-FCM-ZYLB), 
* [Levine_13dim](http://science.sciencemag.org/content/332/6030/687.long) data used as presented by the benchmark study by [Weber et al. 2016](https://onlinelibrary.wiley.com/doi/abs/10.1002/cyto.a.23030) (FlowRepository ID: FR-FCM-ZZPH),
* [Levine_32dim](https://www.cell.com/cell/abstract/S0092-8674(15)00637-6) data used as presented by the benchmark study by [Weber et al. 2016](https://onlinelibrary.wiley.com/doi/abs/10.1002/cyto.a.23030) (FlowRepository ID: FR-FCM-ZZPH). 

## Example on CyTOF data: 
DMLMJ can be used to find an optimal form of the Mahalanobis distance metric, which is a generalization of the commonly used Euclidean distance metric. The influence of DMLMJ on downstream multivariate analysis using for example t-SNE can be checked. Below an example is given for the Levine_13dim dataset, to which t-SNE was applied in Euclidean (left) and DMLMJ-transformed (right) space. 

<p align="center">
  <img src="./figs/TSNE_13_test.png" width="700"/>
</p>


### Prerequisites
DMLMJ has been tested using MATLAB 2010A and later on Windows and Linux (Mac should be fine).

## Installation of DMLMJ
Download the folder "DMLMJ" into the directory of your choice. Then within MATLAB go to file >> Set path... and add the directory containing "DMLMJ" to the list (if it isn't already). That's it.

## Usage of DMLMJ
First we need to learn a linear transformation from supervised data
```matlab
params = struct();
params.kernel = 0;
params.knn = 5;
params.dim = 10;
>> L = DMLMJ(XTr, YTr, params)
```
### Parameters of DMLMJ
* XTr: Training examples (d x n, where d is the number of features and n is the number of examples)
* YTr: Training labels   (n x 1)
* params (optional): 
   * .kernel (If set to 1, a kerned method is applied, default = 0)
   * .ker    (Kernel type: 'rbf' or 'poly' will be applied, default = 'rbf')
   * .knn    (Number of neighbors, default = 5)
   * .dim    (Desired number of dimensionality, default = cross-validation)

Once we have learned L, we can use it for unsupervised data
```matlab
>> X = L'*X;
```

## Acknowledgements
If you find our study for single-cell data interesting, please consider citing: 
``` bibtex
@Article{Nguyen2018,
  Title       = {Learning Single-Cell Distances from Cytometry Data},
  Author      = {Nguyen, B. and Rubbens, P. and Kerckhof, F.-M. and Boon, N. and De Baets, B. and Waegeman, W. },
  Journal     = {In preparation},
  Year        = {2018},
}
```

DMLMJ has been published as a method as such. If you find the code useful in your research, please consider citing:
``` bibtex
@Article{Nguyen2016,
  Title       = {Supervised distance metric learning through maximization of the {J}effrey divergence},
  Author      = {Bac Nguyen and Carlos Morell and De Baets, Bernard},
  Journal     = {Pattern Recognition},
  Year        = {2017},
  Pages       = {215-225},
  Volume      = {64}
}
```
