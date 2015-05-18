import random
import pandas.io.data as web
import datetime
import wfvg

if __name__ == '__main__':
    TS = {}
    TSpct = {}

    start = datetime.datetime(2011, 4, 20)
    end = datetime.datetime(2015, 5, 16)
    # Retrieve YHOO
    TS['TS.YHOO'] = list(web.DataReader("YHOO", 'yahoo', start, end)['Close'].values)

    # Retrieve GOOGL
    L = web.DataReader("GOOGL", 'yahoo', start, end)
    # Correcting for stock split
    L.loc[:'2014-04-02','Close'] = L[:'2014-04-02']['Close']/2
    TS['TS.GOOGL'] = list(L['Close'].values)

    # Retrieve AAPL
    L = web.DataReader("AAPL", 'yahoo', start, end)
    # Correcting for stock split
    L.loc[:'2014-06-06','Close'] = L[:'2014-06-06']['Close']/7
    TS['TS.AAPL'] = list(L['Close'].values)

    # Retrieve MSFT
    TS['TS.MSFT'] = list(web.DataReader("MSFT", 'yahoo', start, end)['Close'].values)


    # Generate normalized time series
    for TSname in TS:
        TSpct[TSname] = [0]
        for i in range(1,len(TS[TSname])):
            TSpct[TSname].append(TS[TSname][i]/TS[TSname][0])

    # TS['TS.YHOO.pct'] = [0]
    # for i in range(1,len(TS['TS.YHOO'])):
    #     TS['TS.YHOO.pct'].append(TS['TS.YHOO'][i]/TS['TS.YHOO'][0])
    # # Generate normalized time series
    # TS['TS.GOOGL.pct'] = [0]
    # for i in range(1,len(TS['TS.GOOGL'])):
    #     TS['TS.GOOGL.pct'].append(TS['TS.GOOGL'][i]/TS['TS.GOOGL'][0])
    # # Generate normalized time series
    # TS['TS.AAPL.pct'] = [0]
    # for i in range(1,len(TS['TS.AAPL'])):
    #     TS['TS.AAPL.pct'].append(TS['TS.AAPL'][i]/TS['TS.AAPL'][0])
    # # Generate normalized time series
    # TS['TS.MSFT.pct'] = [0]
    # for i in range(1,len(TS['TS.MSFT'])):
    #     TS['TS.MSFT.pct'].append(TS['TS.MSFT'][i]/TS['TS.MSFT'][0])

    # Each entry TSwfv[TSname] is an array of vector coefficients
    # Each item TSwfv[TSname][i] in the array is a feature vector (FV)
    # Input to the clustering algorithm is all FVs with the same value of i
    # Example: TSwfv['TS.1'][1], TSwfv['TS.2'][1], TSwfv['TS.3'][1], ...

    # TSwfv,TSsse = wfvg.generate_feature_vectors(TS)
    TSwfv,TSsse = wfvg.generate_feature_vectors(TSpct)
