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
            TS[aline[1]].append(int(aline[2]))
        else:
            TS[aline[1]] = [int(aline[2]),]





if __name__=='__main__':
    print UTM2LL('N1') #-177, 4
    print UTM2LL('F30') #-3, -52

    # get only recent 1024
    TSpct = {}
    for key in TS:
        TSpct[key] = TS[key][len(TS[key])-1024:len(TS[key])]

    # get only recent 1024
    TSpct2010 = {}
    for key in TS:
        TSpct2010[key] = TS[key][0:256]

    TSpct2013 = {}
    for key in TS:
        TSpct2013[key] = TS[key][(365*3):(365*3+256)]

    TSwfv,TSsse,TSrec = generate_feature_vectors(TSpct)
    (TSwfv2010,a,b) = generate_feature_vectors(TSpct2010)
    (TSwfv2013,a,b) = generate_feature_vectors(TSpct2013)

    np.random.seed(0)
    clustering_names = [
        'MiniBatchKMeans', 'AffinityPropagation',
        'SpectralClustering', 'Ward', 'AgglomerativeClustering',
        'Birch', 'DBSCAN']

     # Retrieve the L4 coefficients for all time series
    '''score_dict={}
    for al in clustering_names:
        score_dict[al] = []'''

    #example
    #score = get_silhouette_score('MiniBatchKMeans', TSwfv, 4, 8)['score']
    level = 6
    number_of_cluster = 4
    algorithm = 'MiniBatchKMeans'
    #ds = get_silhouette_score(algorithm, TSwfv, level, number_of_cluster)['ds']
    ds2010 = get_silhouette_score(algorithm, TSwfv2010, level, number_of_cluster)['ds']
    ds2013 = get_silhouette_score(algorithm, TSwfv2013, level, number_of_cluster)['ds']

    colors = ['b', 'r', 'k', 'g', 'c']
    #getting score dict according to level of feature extraction
    number_of_cluster_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    level_list = [2, 4, 6, 8, 10]

    plt.figure()
    m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
                llcrnrlon=-180,urcrnrlon=180,resolution='c')

    m.fillcontinents(color='gray',lake_color='None')
    # draw parallels and meridians.
    m.drawmapboundary(fill_color='aqua')

    plt.title("Earthquake cluster map 2010")
    for utm in ds2010:
        label = ds2010[utm]
        lon, lat = UTM2LL(utm)
        x,y = m(lon, lat)
        m.plot(x, y, colors[int(label)]+'o')

    plt.savefig(output_map_dir+algorithm+'(year=2010,level='+str(level)+',number_of_cluster='+str(number_of_cluster)+').pdf',edgecolor='b', format='pdf')


    plt.figure()
    m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
                llcrnrlon=-180,urcrnrlon=180,resolution='c')

    m.fillcontinents(color='gray',lake_color='None')
    # draw parallels and meridians.
    m.drawmapboundary(fill_color='aqua')

    plt.title("Earthquake cluster map 2013")
    for utm in ds2013:
        label = ds2013[utm]
        lon, lat = UTM2LL(utm)
        x,y = m(lon, lat)
        m.plot(x, y, colors[int(label)]+'o')

    plt.savefig(output_map_dir+algorithm+'(year=2013,level='+str(level)+',number_of_cluster='+str(number_of_cluster)+').pdf',edgecolor='b', format='pdf')
