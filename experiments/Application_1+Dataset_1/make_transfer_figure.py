import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def make_figure(file1, file2, ylim=(40,100)):
    
    df1 = pd.read_csv('output/' + file1 + '.txt', header=None)
    df1.columns = ['Euclidean', 'partial T-DMLMJ']
    df1 = df1[['partial T-DMLMJ']]
    
    df2 = pd.DataFrame([i  for j in range(10) for i in range(2,11)], columns=['T'])
    
    df = pd.concat([df2, df1], axis=1)
    data = pd.DataFrame([], columns=['T', 'Accuracy (%)', 'Method'])
    for name in list(df1.columns):
        types = pd.DataFrame([name]*90, columns=['Method'])
        tmp = pd.concat([df[['T', name]], types], axis=1)
        tmp.columns = ['T', 'Accuracy (%)', 'Method']
        data = data.append(tmp, ignore_index=True)

    df2 = pd.read_csv('output/' + file2 + '.txt', header=None)
    df2.columns = ['Euclidean', 'T-DMLMJ']

    G = pd.DataFrame([i  for j in range(10) for i in range(2,11)], columns=['T'])
    df = pd.concat([G, df2.iloc[:, [1]]], axis=1)

    df.columns = ['T', 'T-DMLMJ']
    
    for name in ['T-DMLMJ']:
        types = pd.DataFrame([name]*90, columns=['Method'])
        tmp = pd.concat([df[['T', name]], types], axis=1)
        tmp.columns = ['T', 'Accuracy (%)', 'Method']
        data = data.append(tmp, ignore_index=True)        
        
    
    ax=sns.factorplot(kind='box',
                   y='Accuracy (%)',
                   x='T',
                   hue='Method',
                   data=data,
                   palette=sns.color_palette("colorblind")[1:5:2],
                   linewidth=0.7,
                   size=4,        
                   aspect=1.2,    
                   legend =True,
                   legend_out=False)
    ax.set(ylim=ylim)
    ax.despine(offset=10, trim=True)
    plt.savefig('output/transfer.png', format='png',bbox_inches='tight', dpi=500)


if __name__ == '__main__':
    make_figure('asinh_partialsupervised', 'asinh_unsupervised', (40, 80))

