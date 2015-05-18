import random
import pandas.io.data as web
import datetime
import wfvg

if __name__ == '__main__':
    TS = {}
    # Generate 'n' sample time series using a random number generator
    # n = 2  # 10
    # TSlen = 2**11
    # for i in range(1,n+1):
    #     TSname = "TS." + str(int(i))
    #     TS[TSname] = random.sample(range(TSlen*5),TSlen)

    # Retrieve stock time series fron Yahoo Finance (1024 items each)
    start = datetime.datetime(2011, 4, 20)
    end = datetime.datetime(2015, 5, 16)
    TS['TS.YHOO'] = list(web.DataReader("YHOO", 'yahoo', start, end)['Close'].values)

    # Correcting GOOGL time series for stock split
    L = web.DataReader("GOOGL", 'yahoo', start, end)
    L.loc[:'2014-04-02','Close'] = L[:'2014-04-02']['Close']/2
    TS['TS.GOOGL'] = list(L['Close'].values)

    # Correcting AAPL time series for stock split
    L = web.DataReader("AAPL", 'yahoo', start, end)
    L.loc[:'2014-06-06','Close'] = L[:'2014-06-06']['Close']/7
    TS['TS.AAPL'] = list(L['Close'].values)

    TS['TS.MSFT'] = list(web.DataReader("MSFT", 'yahoo', start, end)['Close'].values)
    # Each entry TSwfv[TSname] is an array of vector coefficients
    # Each item TSwfv[TSname][i] in the array is a feature vector (FV)
    # Input to the clustering algorithm is all FVs with the same value of i
    # Example: TSwfv['TS.1'][1], TSwfv['TS.2'][1], TSwfv['TS.3'][1], ...
    TSwfv,TSsse = wfvg.generate_feature_vectors(TS)
