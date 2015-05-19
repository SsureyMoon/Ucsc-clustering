import random
import pandas.io.data as web
import datetime
import wfvg
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import cluster

if __name__ == '__main__':
    TS = {}
    TSpct = {}
    symbols = ['YHOO','GOOGL','AAPL','MSFT','BIDU','IBM','EBAY','ORCL','CSCO',
    'SAP','VZ','T','CMCSA','AMX','QCOM','NOK','AMZN','WMT','COST','TGT','CVX',
    'TOT','BP','XOM','E','COP','APA','GS','MS','BK','CS','SMFG','DB','RY','CS',
    'BCS','SAN','BNPQY','NKE','DECK']
    stock_split = {}
    stock_split['GOOGL'] = ('2014-04-02',2)
    stock_split['AAPL'] = ('2014-06-06',7)
    stock_split['AMX'] = ('2011-06-30',2)
    stock_split['NKE'] = ('2012-12-25',2)

    start = datetime.datetime(2011, 4, 20)
    end = datetime.datetime(2015, 5, 16)

    for ticker in symbols:
        key = "TS."+ticker
        print "Retrieving {0} ...".format(ticker)
        L = web.DataReader(ticker, 'yahoo', start, end)
        # Correct stock splits
        if ticker in stock_split:
            L.loc[:stock_split[ticker][0],'Close'] = L[:stock_split[ticker][0]]['Close']/stock_split[ticker][1]
        TS[key] = list(L['Close'].values)

    # Generate normalized time series
    for TSname in TS:
        TSpct[TSname] = [0]
        for i in range(1,len(TS[TSname])):
            TSpct[TSname].append(TS[TSname][i]/TS[TSname][0])


    # Each entry TSwfv[TSname] is an array of vector coefficients
    # Each item TSwfv[TSname][i] in the array is a feature vector (FV)
    # Input to the clustering algorithm is all FVs with the same value of i
    # Example: TSwfv['TS.1'][1], TSwfv['TS.2'][1], TSwfv['TS.3'][1], ...

    TSwfv,TSsse,TSrec = wfvg.generate_feature_vectors(TSpct)

    # Clustering with Kmeans
    # Retrieve the L4 coefficients for all time series
    dataset = [ TSwfv[k][1] for k,v in TSwfv.iteritems() ]
    datasetnames = [k for k,v in TSwfv.iteritems()]
    model = KMeans(n_clusters=8).fit(dataset)
    TScL4 = dict(zip(datasetnames, model.labels_))
    print TScL4
    for i in range(min(model.labels_),max(model.labels_)+1):
        print "[Kmeans] Cluster", i
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for k in [key for key,val in TScL4.iteritems() if TScL4[key]==i]:
            ax.plot(TSrec[k][1],label=k+' L4 ')
        plt.legend(prop={'size':6},loc=0)
        plt.savefig('Cluster'+str(i)+'-kmeans.pdf',edgecolor='b', format='pdf')

    # Clustering with Spectral Clustering
    spectral = cluster.SpectralClustering(n_clusters=8,
                                          eigen_solver='arpack',
                                          affinity="nearest_neighbors")
    model = spectral.fit(dataset)
    TSspecdenL4 = dict(zip(datasetnames, model.labels_))
    print TSspecdenL4
    for i in range(min(model.labels_),max(model.labels_)+1):
        print "[Spectral density] Cluster", i
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for k in [key for key,val in TSspecdenL4.iteritems() if TSspecdenL4[key]==i]:
            ax.plot(TSrec[k][1],label=k+' L4 ')
        plt.legend(prop={'size':6},loc=0)
        plt.savefig('Cluster'+str(i)+'-sd.pdf',edgecolor='b', format='pdf')
