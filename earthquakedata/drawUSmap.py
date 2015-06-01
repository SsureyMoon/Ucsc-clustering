from __future__ import division

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from pyproj import Proj
import re


import sys
sys.path.insert(0, '../')
from demo.wfvg import generate_feature_vectors
from task4.evalPerformace import get_silhouette_score

output_map_dir = 'output_US_map_plot/'

# llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
# are the lat/lon values of the lower left and upper right corners
# of the map.
# resolution = 'c' means use crude resolution coastlines.


UTM_US = ['R13', 'R14', 'R15', 'R16',
          'S10', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16', 'S17', 'S18',
          'T10', 'T11', 'T12', 'T13', 'T14', 'T15', 'T16', 'T17', 'T18', 'T19']

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
            TS[aline[1]].append(int(aline[2]))
        else:
            TS[aline[1]] = [int(aline[2]),]


if __name__=='__main__':
    print UTM2LL('N1') #-177, 4
    print UTM2LL('F30') #-3, -52

    # get only recent 1024
    TSpct = {}
    for key in TS:
        #get US only
        if key in UTM_US:
            TSpct[key] = TS[key][len(TS[key])-1024:len(TS[key])]
        else:
            pass

    # get only recent 1024
    TSpct2010 = {}
    for key in TS:
        TSpct2010[key] = TS[key][0:256]

    TSpct2014 = {}
    for key in TS:
        TSpct2014[key] = TS[key][(365*4):(365*4+256)]

    TSwfv,TSsse,TSrec = generate_feature_vectors(TSpct)
    (TSwfv2010,a,b) = generate_feature_vectors(TSpct2010)
    (TSwfv2014,a,b) = generate_feature_vectors(TSpct2014)

    np.random.seed(0)
    clustering_names = [
        'MiniBatchKMeans', 'AffinityPropagation',
        'SpectralClustering', 'Ward', 'AgglomerativeClustering',
        'Birch', 'DBSCAN']

     # Retrieve the L4 coefficients for all time series
    '''score_dict={}
    for al in clustering_names:
        score_dict[al] = []'''
    applied_algo=['MiniBatchKMeans', 'SpectralClustering', 'Ward', 'Birch']
    #example
    #score = get_silhouette_score('MiniBatchKMeans', TSwfv, 4, 8)['score']
    plt.figure()
    for enum, cname in enumerate(applied_algo):
        level = 8
        number_of_cluster = 4
        algorithm = cname
        ds2010 = get_silhouette_score(algorithm, TSwfv2010, level, number_of_cluster)['ds']
        ds2014 = get_silhouette_score(algorithm, TSwfv2014, level, number_of_cluster)['ds']

        colors = ['b', 'r', 'k', 'g', 'c', 'm', 'y', '0.75']
        #getting score dict according to level of feature extraction
        number_of_cluster_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]
        level_list = [2, 4, 6, 8, 10]

        if max(map(int, ds2010.values())) < number_of_cluster:
            print 'drawing', cname
            plt.figure()
            m = Basemap(projection='cyl',llcrnrlat=24,urcrnrlat=56,\
                        llcrnrlon=-132,urcrnrlon=-66,resolution='c')

            m.fillcontinents(color='gray',lake_color='None')
            # draw parallels and meridians.
            m.drawmapboundary(fill_color='aqua')

            plt.title("Earthquake cluster map 2010 using "+cname)
            for utm in ds2010:
                label = ds2010[utm]
                lon, lat = UTM2LL(utm)
                x,y = m(lon, lat)
                m.plot(x, y, colors[int(label)]+'o')


            plt.savefig(output_map_dir+'US_map_'+algorithm+'(year=2010,level='+str(level)+',number_of_cluster='+str(number_of_cluster)+').pdf',edgecolor='b', format='pdf')


            plt.figure()
            m = Basemap(projection='cyl',llcrnrlat=24,urcrnrlat=56,\
                        llcrnrlon=-132,urcrnrlon=-66,resolution='c')

            m.fillcontinents(color='gray',lake_color='None')
            # draw parallels and meridians.
            m.drawmapboundary(fill_color='aqua')

            plt.title("Earthquake cluster map 2014 using "+cname)
            for utm in ds2014:
                label = ds2014[utm]
                lon, lat = UTM2LL(utm)
                x,y = m(lon, lat)
                m.plot(x, y, colors[int(label)]+'o')

            plt.savefig(output_map_dir+'US_map_'+algorithm+'(year=2014,level='+str(level)+',number_of_cluster='+str(number_of_cluster)+').pdf',edgecolor='b', format='pdf')