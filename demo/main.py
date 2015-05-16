import random
import wfvg

if __name__ == '__main__':
    # Generate 'n' sample time series using a random number generator
    n = 2  # 10
    TSlen = 2**11
    TS = {}
    for i in range(1,n+1):
        TSname = "TS." + str(int(i))
        TS[TSname] = random.sample(range(TSlen*5),TSlen)

    # Each entry TSwfv[TSname] is an array of vector coefficients
    # Each item TSwfv[TSname][i] in the array is a feature vector (FV)
    # Input to the clustering algorithm is all FVs with the same value of i
    # Example: TSwfv['TS.1'][1], TSwfv['TS.2'][1], TSwfv['TS.3'][1], ...
    TSwfv,TSsse = wfvg.generate_feature_vectors(TS)
