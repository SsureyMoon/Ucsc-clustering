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
        'Birch']

     # Retrieve the L4 coefficients for all time series
    score_dict={}
    for al in clustering_names:
        score_dict[al] = []

    for level in range(0,5):
        dataset_for_cluster = [ TSwfv[k][level] for k,v in TSwfv.iteritems() ]
        datasetnames = [k for k,v in TSwfv.iteritems()]
        min_max_scaler = preprocessing.MinMaxScaler()
        scaled_dataset = dataset_for_cluster
            #min_max_scaler.fit_transform(dataset_for_cluster)
        #scaled_dataset = preprocessing.normalize(dataset_for_cluster)

        dataset_for_plot = [ TSwfv[k][4] for k,v in TSwfv.iteritems() ]
        scaled_dataset_for_plot = min_max_scaler.fit_transform(dataset_for_plot)


        X = np.array(scaled_dataset)
        # estimate bandwidth for mean shift
        bandwidth = cluster.estimate_bandwidth(X, quantile=0.3)
        # connectivity matrix for structured Ward
        connectivity = kneighbors_graph(X, n_neighbors=10, include_self=False)
        # make connectivity symmetric
        connectivity = 0.5 * (connectivity + connectivity.T)

        # create clustering estimators
        two_means = cluster.MiniBatchKMeans(n_clusters=8)
        ward = cluster.AgglomerativeClustering(n_clusters=8, linkage='ward',
                                               connectivity=connectivity)
        spectral = cluster.SpectralClustering(n_clusters=8,
                                              eigen_solver='arpack',
                                              affinity="nearest_neighbors")
        # dbscan = cluster.DBSCAN(eps=.2)
        affinity_propagation = cluster.AffinityPropagation(damping=.9,
                                                           preference=-200)

        average_linkage = cluster.AgglomerativeClustering(
            linkage="average", affinity="cityblock", n_clusters=8,
            connectivity=connectivity)

        dbscan = DBSCAN(eps=0.5, min_samples=1)

        birch = cluster.Birch(n_clusters=8)
        clustering_algorithms = [
            two_means, affinity_propagation, spectral, ward, average_linkage,
            birch]





        for name, algorithm in zip(clustering_names, clustering_algorithms):
            algorithm.fit(X)
            ds = dict(zip(datasetnames, algorithm.labels_))
            if len(set(algorithm.labels_)) > 1:
                score = metrics.silhouette_score(X, algorithm.labels_, metric='euclidean')
            else:
                score = 0
            score_dict[name].append(score)

    plt.figure()
    plt.hold(True)
    plt.axis([1.5, 10.5, -0.1, 0.7])
    level_list = [2, 4, 6, 8, 10]
    colors = ['b', 'r', 'k', 'g', 'c', 'm']
    for enum, key in enumerate(score_dict):
        plt.plot(level_list, score_dict[key], colors[enum], label=key)
        plt.plot(level_list, score_dict[key], colors[enum]+'o')
    plt.legend(bbox_to_anchor=(1.1, 1.1),loc=1)
    plt.ylabel('silhouette_score')
    plt.xlabel('feature_extraction level')
    plt.savefig('silhouette_score_plot.pdf',edgecolor='b', format='pdf')

