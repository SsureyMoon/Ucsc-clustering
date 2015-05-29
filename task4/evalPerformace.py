from __future__ import division
import pandas.io.data as web
import datetime
import sys
import pickle
import matplotlib.pyplot as plt
import pywt
import numpy as np
from sklearn import preprocessing, cluster
from sklearn.cluster import KMeans, DBSCAN
from sklearn.neighbors import kneighbors_graph
from sklearn import metrics

wavelettype = 'haar'

sys.path.insert(0, '../')
from demo.wfvg import generate_feature_vectors

download = False


def two_means(number_of_cluster, connectivity):
    return cluster.MiniBatchKMeans(n_clusters=number_of_cluster)

def affinity_propagation(number_of_cluster, connectivity):
    return cluster.AffinityPropagation(damping=.9, preference=-200)

def ward(number_of_cluster, connectivity):
    return cluster.AgglomerativeClustering(n_clusters=number_of_cluster, linkage='ward',
                                       connectivity=connectivity)

def spectral(number_of_cluster, connectivity):
    return cluster.SpectralClustering(n_clusters=number_of_cluster,
                                      eigen_solver='arpack',
                                      affinity="nearest_neighbors")

def average_linkage(number_of_cluster, connectivity):
    return cluster.AgglomerativeClustering(
            linkage="average", affinity="cityblock", n_clusters=number_of_cluster,
            connectivity=connectivity)

def birch(number_of_cluster, connectivity):
    return cluster.Birch(n_clusters=number_of_cluster)

def dbscan(number_of_cluster, connectivity):
    return cluster.DBSCAN(eps=0.35, min_samples=1)

def get_silhouette_score(algorithm_name, dataX, level=4, number_of_cluster=8):
    index = int(level/2-1)
    if index < 0:
        index = 0

    dataset_for_cluster = [ dataX[k][index] for k,v in dataX.iteritems() ]
    datasetnames = [k for k,v in dataX.iteritems()]

    #min_max_scaler = preprocessing.MinMaxScaler()
    #min_max_scaler.fit_transform(dataset_for_cluster)
    #scaled_dataset = preprocessing.normalize(dataset_for_cluster)

    dataset_for_plot = [ dataX[k][4] for k,v in dataX.iteritems()]

    X = np.array(dataset_for_cluster)
    # estimate bandwidth for mean shift
    bandwidth = cluster.estimate_bandwidth(X, quantile=0.3)
    # connectivity matrix for structured Ward
    connectivity = kneighbors_graph(X, n_neighbors=number_of_cluster, include_self=False)
    # make connectivity symmetric
    connectivity = 0.5 * (connectivity + connectivity.T)

    # create clustering estimators


    clustering_algorithms = {
        'MiniBatchKMeans':two_means, 'AffinityPropagation':affinity_propagation,
        'SpectralClustering':spectral, 'Ward':ward, 'AgglomerativeClustering':average_linkage,
        'Birch':birch, 'DBSCAN': dbscan
    }


    algorithm = clustering_algorithms[algorithm_name](number_of_cluster, connectivity)
    if algorithm_name == 'DBSCAN' and level == 10:
        min_max_scaler = preprocessing.MinMaxScaler()
        scaledX = min_max_scaler.fit_transform(X) #make maximum length between 0 and 1
        algorithm.fit(scaledX)
    else:
        algorithm.fit(X)

    ds = dict(zip(datasetnames, algorithm.labels_))
    if len(set(algorithm.labels_)) > 1 and len(set(algorithm.labels_))<len(algorithm.labels_):
        score = metrics.silhouette_score(X, algorithm.labels_, metric='euclidean')
    else:
        score = 0.00

    return {'score': score, 'ds':ds}





if __name__ == '__main__':
    TS = {}
    TSpct = {}
    symbols = ['YHOO','GOOGL','AAPL','MSFT','BIDU','IBM','EBAY','ORCL','CSCO',
    'SAP','VZ','T','CMCSA','AMX','QCOM','NOK','AMZN','WMT','COST','TGT','CVX',
    'TOT','BP','XOM','E','COP','APA','GS','MS','BK','CS','SMFG','DB','RY','CS',
    'BCS','SAN','BNPQY','NKE','DECK','PCLN','EMC','INTC','AMD','NVDA','TXN',
    'BRCM','ADI','WFM','TFM','INFN','CIEN','CSC','TMO','BSX','TIVO','DISH',
    'SATS','LORL','ORAN','IMASF','IRDM','HRS','GD','BA','LMT','NOC','RTN',
    'TXT','ERJ','UTX','SPR','BDRBF','AAL','DAL','HA','UAL','LUV','JBLU','ALGT',
    'RJET','RCL','CCL','DIS','CBS','FOXA','QVCA','DWA','VIAB','TM',
    'TWX','DISCA','SNI','MSG','PG','ENR','HRG','SPB','KMB','TSLA']
    stock_split = {}
    stock_split['GOOGL'] = ('2014-04-02',2)
    stock_split['AAPL'] = ('2014-06-06',7)
    stock_split['AMX'] = ('2011-06-30',2)
    stock_split['NKE'] = ('2012-12-25',2)
    stock_split['WFM'] = ('2013-05-29',2)

    start = datetime.datetime(2011, 4, 20)
    end = datetime.datetime(2015, 5, 16)

    if download:
        for ticker in symbols:
            key = "TS."+ticker
            print "Retrieving {0} ...".format(ticker)
            L = web.DataReader(ticker, 'yahoo', start, end)
            # Correct stock splits
            if ticker in stock_split:
                L.loc[:stock_split[ticker][0],'Close'] = L[:stock_split[ticker][0]]['Close']/stock_split[ticker][1]
            TS[key] = list(L['Close'].values)
        # Save time series to file
        pickle.dump(TS,open("../demo/savedTS.dat",'wb'))
    else:
        # Retrieve time series from file
        TS = pickle.load(open("../demo/savedTS.dat","rb"))


    TSpct={}
    for TSname in TS:
        TSpct[TSname] = [0]
        for i in range(1,len(TS[TSname])):
            TSpct[TSname].append(TS[TSname][i]/TS[TSname][0])


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
    result = get_silhouette_score('MiniBatchKMeans', TSwfv, 4, 8)




    colors = ['b', 'r', 'k', 'g', 'c', 'm', 'y']
    #getting score dict according to level of feature extraction
    number_of_cluster_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    level_list = [2, 4, 6, 8, 10]
    for number in number_of_cluster_list:
        plt.figure()
        plt.hold(True)
        plt.axis([1.5, 10.5, -0.1, 0.9])
        for enum, name in enumerate(clustering_names):
            score_list = []
            for level in level_list:
                 score_list.append(get_silhouette_score(name, TSwfv, level, number)['score'])
            plt.plot(level_list, score_list, colors[enum], label=name)
            plt.plot(level_list, score_list, colors[enum]+'o')

        plt.title('number_of_cluster='+str(number))
        plt.legend(loc=0, prop={'size':6})
        plt.ylabel('silhouette_score')
        plt.xlabel('feature_extraction level')
        plt.savefig('silhouette_score_plot_per_level_(clusters='+str(number)+').pdf',edgecolor='b', format='pdf')



    for le in level_list:
        plt.figure()
        plt.hold(True)
        plt.axis([1.5, 10.5, -0.1, 0.9])
        colors = ['b', 'r', 'k', 'g', 'c', 'm', 'y']
        #getting score dict according to level of feature extraction
        number_of_cluster_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        for enum, name in enumerate(clustering_names):
            score_list = []
            for number in number_of_cluster_list:
                score_list.append(get_silhouette_score(name, TSwfv, le, number)['score'])
            plt.plot(number_of_cluster_list, score_list, colors[enum], label=name)
            plt.plot(number_of_cluster_list, score_list, colors[enum]+'o')

        plt.title('level='+str(le))
        plt.legend(loc=0, prop={'size':6})
        plt.ylabel('silhouette_score')
        plt.xlabel('number_of_cluster')
        plt.savefig('silhouette_score_plot_per_number_of_cluster(level='+str(le)+').pdf',edgecolor='b', format='pdf')

    #scatter!
    for le in level_list:
        plt.figure()
        plt.hold(True)
        plt.axis([1.5, 10.5, -0.1, 0.9])
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
        plt.legend(bbox_to_anchor=(1.1, 1.1),loc=1)
        plt.ylabel('silhouette_score')
        plt.xlabel('number_of_cluster')
        plt.savefig('silhouette_score_plot_per_number_of_cluster(level='+str(le)+').pdf',edgecolor='b', format='pdf')
