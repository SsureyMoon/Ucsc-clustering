import random
import pandas.io.data as web
import datetime
import wfvg

if __name__ == '__main__':
    TS = {}
    TSpct = {}
    symbols = ['YHOO',
    'GOOGL',
    'AAPL',
    'MSFT',
    'BIDU',
    'IBM',
    'EBAY',
    'ORCL',
    'CSCO',
    'SAP',
    'VZ',
    'T',
    'CMCSA',
    'AMX',
    'QCOM',
    'NOK',
    'AMZN',
    'WMT',
    'COST',
    'TGT',
    'CVX',
    'TOT',
    'BP',
    'XOM',
    'E',
    'COP',
    'APA',
    'GS',
    'MS',
    'BK',
    'CS',
    'SMFG',
    'DB',
    'RY',
    'CS',
    'BCS',
    'SAN',
    'BNPQY']
    stock_split = {}
    stock_split['GOOGL'] = ('2014-04-02',2)
    stock_split['AAPL'] = ('2014-06-06',7)
    # TO DO: Check splits for AMX, COP, NOK 

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

    # TSwfv,TSsse = wfvg.generate_feature_vectors(TS)
    TSwfv,TSsse = wfvg.generate_feature_vectors(TSpct)
