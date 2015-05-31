from __future__ import division
import sys
sys.path.insert(0, '../')
from demo.wfvg import generate_feature_vectors
from task4.evalPerformace import get_silhouette_score

import numpy as np


output_dir = '/Users/kathynorman/Documents/Clustering/Data/output_plot/'

TS ={}

with open('quakes/quakes2010-2014.csv') as file:
    for line in file.readlines():
        aline = line.strip().split(' ')
        if aline[1] in TS:
            TS[aline[1]].append(int(aline[2]))
        else:
            TS[aline[1]] = [int(aline[2]),]


# get only recent 1024
TSpct = {}
for key in TS:
    TSpct[key] = TS[key][len(TS[key])-1024:len(TS[key])]

TSwfv,TSsse,TSrec = generate_feature_vectors(TSpct)

np.random.seed(0)
clustering_names = [
    'MiniBatchKMeans', 'AffinityPropagation',
    'SpectralClustering', 'Ward', 'AgglomerativeClustering',
    'Birch', 'DBSCAN']

 # Retrieve the L4 coefficients for all time series
'''score_dict={}
for al in clustering_names:
    score_dict[al] = []'''

#example
score = get_silhouette_score('MiniBatchKMeans', TSwfv, 4, 8)['score']
ds = get_silhouette_score('MiniBatchKMeans', TSwfv, 4, 50)['ds']


colors = ['b', 'r', 'k', 'g', 'c', 'm', 'y']
#getting score dict according to level of feature extraction
number_of_cluster_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]
level_list = [2, 4, 6, 8, 10]
'''for number in number_of_cluster_list:
    plt.figure()
    plt.hold(True)
    plt.axis([1.5, 10.5, -0.5, 1.5])
    for enum, name in enumerate(clustering_names):
        score_list = []
        for level in level_list:
             score_list.append(get_silhouette_score(name, TSwfv, level, number))
        plt.plot(level_list, score_list, colors[enum], label=name)
        plt.plot(level_list, score_list, colors[enum]+'o')

    plt.title('number_of_cluster='+str(number))
    plt.legend(loc=0, prop={'size':6})
    plt.ylabel('silhouette_score')
    plt.xlabel('feature_extraction level')
    plt.savefig(output_dir+'silhouette_score_plot_per_level_(clusters='+str(number)+').pdf',edgecolor='b', format='pdf')



for le in level_list:
    plt.figure()
    plt.hold(True)
    plt.axis([1.5, 10.5, -0.5, 1.5])
    colors = ['b', 'r', 'k', 'g', 'c', 'm', 'y']
    #getting score dict according to level of feature extraction
    number_of_cluster_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    for enum, name in enumerate(clustering_names):
        score_list = []
        for number in number_of_cluster_list:
            score_list.append(get_silhouette_score(name, TSwfv, le, number))
        plt.plot(number_of_cluster_list, score_list, colors[enum], label=name)
        plt.plot(number_of_cluster_list, score_list, colors[enum]+'o')

    plt.title('level='+str(le))
    plt.legend(loc=0, prop={'size':6})
    plt.ylabel('silhouette_score')
    plt.xlabel('number_of_cluster')
    plt.savefig(output_dir+'silhouette_score_plot_per_number_of_cluster(level='+str(le)+').pdf',edgecolor='b', format='pdf')
'''
