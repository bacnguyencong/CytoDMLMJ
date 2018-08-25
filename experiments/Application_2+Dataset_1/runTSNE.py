import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import seaborn as sns

import matplotlib.pyplot as plt
plt.switch_backend('agg')

def scatter(x, colors, name):
    sns.set_context("paper")
    sns.set_style('white')
    colors = colors.astype(np.int)
    # We choose a color palette with seaborn.
    palette = np.array(sns.color_palette("hls", 25))

    # We create a scatter plot.
    f = plt.figure(figsize=(4.5, 4.5))
    ax = plt.subplot(aspect='equal')
    
    labels = np.unique(colors)
    
    for i in labels:
        idx = colors == i
        sc = ax.scatter(x[idx,0], x[idx,1], lw=0, s=20, c=palette[i], 
                    label=str(i))
    #ax.axis('off')
    ax.axis('tight')
    plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
    plt.savefig(name, format='eps', dpi=500, bbox_inches='tight')


dim = 32
for i in range(5, 15):
    print('Running on {}'.format(i))
    df = pd.read_csv('data/DMLMJ/{}train.{}'.format(dim,i), header=None)    

    XTr = df.values[:,:-1]
    YTr = df.values[:,-1]
    X_embedded = TSNE(n_components=2).fit_transform(XTr)
    df = pd.DataFrame()
    df['X'] = X_embedded[:,0]
    df['Y'] = X_embedded[:,1]
    df['L'] = YTr
    df['L'] = df['L'].astype('int')
    scatter(X_embedded, YTr, 'output/tsne_%d_train.%d.eps' % (dim, i))
    df.to_csv('output/tsne_%d_train.%d.txt' % (dim, i), index=False)


