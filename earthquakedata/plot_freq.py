from __future__ import division
from datetime import datetime

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import pandas
from pyproj import Proj
import re
import random


import sys
sys.path.insert(0, '../')
from demo.wfvg import generate_feature_vectors
from task4.evalPerformace import get_silhouette_score

output_map_dir = 'output_map_plot/'

# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# resolution = 'c' means use crude resolution coastlines.




lon_list = range(-177, 180, 6)
lonUTM_list = range(1,61)
lonZip = dict(zip(lonUTM_list, lon_list))

lat_list = range(-76, 84, 8)
latUTM_list = ['C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']
latZip = dict(zip(latUTM_list, lat_list))

def UTM2LL(utm):

    lonUTM = re.search('[0-9]+$', utm).group(0)
    latUTM = re.search('^[A-Z]', utm).group(0)

    lon = lonZip[int(lonUTM)]
    lat = latZip[latUTM]

    return lon, lat



TS ={}

with open('quakes/quakes2010-2014.csv') as file:
    for line in file.readlines():
        aline = line.strip().split(' ')
        if aline[1] in TS:
            TS[aline[1]].append([aline[0], int(aline[2])])
        else:
            TS[aline[1]] = [[aline[0], int(aline[2])]]


if __name__=='__main__':
    print UTM2LL('N1') #-177, 4
    print UTM2LL('F30') #-3, -52

    # get only recent 1024
    sample_keys = random.sample(TS.keys(), 10)

    plt.figure()
    plt.title('# of Earthquake/day')
    for enum, key in enumerate(sample_keys):
        plt.subplot(10, 1, enum+1)
        plt.ylabel(key)
        pd = pandas.DataFrame(np.array(TS[key]))
        pd[0] = pandas.to_datetime(pd[0])
        pd[1] = pd[1].astype(int)
        min_pd = min(pd[1])
        max_pd = max(pd[1])
        plt.yticks(np.arange(min_pd, max_pd, int(max_pd/3)+1))
        plt.plot(pd[0].tolist(), pd[1].tolist())
    plt.show()

    # get only recent 1024