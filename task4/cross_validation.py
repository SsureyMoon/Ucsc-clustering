import pandas.io.data as web
import datetime
import sys
import matplotlib.pyplot as plt
import pywt
import numpy as np
from sklearn.cluster import KMeans

wavelettype = 'haar'

sys.path.insert(0, '../')

from demo.wfvg import generate_feature_vectors


def get_recent_power_of_two(arr):
    length = len(arr)
    i = 0
    power_of_two = 1
    while (2**i) <= length:
        i += 1
    power_of_two = 2**(i-1)
    return arr[(len(arr)-power_of_two):]


TS={}

start = datetime.datetime(2011, 4, 20)
end = datetime.datetime(2015, 5, 16)
TS['TS.YHOO'] = get_recent_power_of_two(list(web.DataReader("YHOO", 'yahoo', start, end)['Close'].values))
TS['TS.GOOGL'] = get_recent_power_of_two(list(web.DataReader("GOOGL", 'yahoo', start, end)['Close'].values))
TS['TS.AAPL'] = get_recent_power_of_two(list(web.DataReader("AAPL", 'yahoo', start, end)['Close'].values))
TS['TS.MSFT'] = get_recent_power_of_two(list(web.DataReader("MSFT", 'yahoo', start, end)['Close'].values))

TSwfv,TSsse = generate_feature_vectors(TS)



dataset = np.array([TSwfv['TS.YHOO'][0], TSwfv['TS.GOOGL'][0], TSwfv['TS.AAPL'][0], TSwfv['TS.MSFT'][0]])


model = KMeans(init='k-means++', n_clusters=2, n_init=4).fit(dataset)
labels = model.labels_

print labels



"""input_file_path = "../data/cv_test/"
with open(input_file_path+"data1", "r") as file:

    line = file.readline()
    line_trimed = list()
    while line:
        line_trimed.append(float(line.replace("\n", "")))
        line = file.readline()

    input = get_recent_power_of_two(line_trimed)
    TS = {}
    TS["orig"] = input
    TSwfv,TSsse  = generate_feature_vectors(TS)
    print TSwfv["orig"]
    TSrec = pywt.waverec(TSwfv["orig"],wavelettype)
    #TSrecL6 = pywt.waverec(c,wavelettype)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(TS["orig"],label="orig")
    ax.plot(TSrec,label="decoded")
    plt.legend()
    plt.show()"""