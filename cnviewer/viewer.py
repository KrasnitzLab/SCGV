'''
Created on Dec 2, 2016

@author: lubo
'''

import matplotlib.pyplot as plt


from utils.loader import load_df
from scipy.cluster.hierarchy import linkage, dendrogram


def main():
    seg_filename = 'tests/data/sample.YL2671P11.5k.seg.quantal.primary.txt'
    df = load_df(seg_filename)

    assert df is not None

    data = df.ix[:, 3:].values

    lmat = linkage(data.transpose(), method="ward")

    fig = plt.figure(0, figsize=(12, 8))
    fig.suptitle(seg_filename, fontsize=10)

    ax_dendro = fig.add_axes([0.1, 0.75, 0.8, 0.2], frame_on=True)
    Z = dendrogram(lmat)
    
    plt.show()

if __name__ == '__main__':
    main()
