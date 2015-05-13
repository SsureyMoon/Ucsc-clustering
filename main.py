import numpy as np
import datetime
import pywt
import matplotlib.pyplot as plt
import random

if __name__ == '__main__':
    # Multi-level decomposition
    TS = list()
    for elem in range(0,2048):
        TS.append(random.sample(range(30),1)[0])
    coeffs = pywt.wavedec(TS,'haar',level=2)
    coeffsL2 = [coeffs[0],coeffs[1],[0]*1024]
    ts_recL2 = pywt.waverec(coeffsL2,'haar')

    coeffs = pywt.wavedec(TS,'haar',level=5)
    coeffsL5 = [coeffs[0],coeffs[1],[0]*128,[0]*256,[0]*512,[0]*1024]
    ts_recL5 = pywt.waverec(coeffsL5,'haar')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(TS)
    ax.plot(ts_recL2)
    ax.plot(ts_recL5)
    plt.show()
