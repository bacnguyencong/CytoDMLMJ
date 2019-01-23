import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def make_full_figure(data_name, fig_name, num=1, trans=False, ylim=(40,100), show=True):
    df1 = pd.read_csv('output/' + data_name + '.txt', header=None);
    df1.columns = ['Euclidean', 'DMLMJ']
    
    df2 = pd.DataFrame([i  for j in range(10) for i in range(2,11)], columns=['S'])
    df = pd.concat([df2, df1], axis=1)
    data = pd.DataFrame([], columns=['S', 'Accuracy (%)', 'Method'])
    for name in list(df1.columns):
        types = pd.DataFrame([name]*90, columns=['Method'])
        tmp = pd.concat([df[['S', name]], types], axis=1)
        tmp.columns = ['S', 'Accuracy (%)', 'Method']
        data = data.append(tmp, ignore_index=True)        
    if show:
        ax=sns.factorplot(kind='box',
                       y='Accuracy (%)',
                       x='S',
                       hue='Method',
                       data=data,
                       palette=sns.color_palette("colorblind")[0:3:2],
                       linewidth=0.7,
                       size=4,
                       aspect=1,
                       legend_out=False)
        ax.set(ylim=ylim)
        ax.despine(offset=10, trim=True)        
    return data

def make_join_figure(file1, file2, num=1, ylim=(40,100)):
    df1 = make_full_figure(file1, file1 + '_raw', num, False, ylim, False)
    df2 = make_full_figure(file2, file2 + '_asinh', num, True, ylim, False)
    df1['Input'] = ['raw' for i in range(len(df1))]
    df2['Input'] = ['asinh(x)' for i in range(len(df1))]
    df = pd.concat([df1, df2])
    df = df.reset_index(drop=True)

    g = sns.factorplot(
          kind='box',
          y='Accuracy (%)',
          x='S',
          hue='Method',
          col='Input',
          data=df,
          palette=sns.color_palette("colorblind")[0:3:2],
          linewidth=0.7,
          size=4,
          aspect=1)
    axes = g.axes.flatten()
    axes[0].set_title("raw")
    axes[1].set_title("asinh(x)")
    
    g.set(ylim=ylim)
    g.despine(offset=10, trim=True)
    plt.savefig('output/output.png', format='png',bbox_inches='tight', dpi=500)

if __name__ == '__main__':
    make_join_figure('supervised', 'asinh_supervised', 1, (40, 100))

