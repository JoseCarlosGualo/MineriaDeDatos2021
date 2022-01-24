# -*- coding: utf-8 -*-

import numpy
import matplotlib.pyplot as plt


# 0. Load data
import pandas as pd
data = pd.read_excel("municipios.xls")
portugal = pd.read_csv('pt.csv', sep=",", header=0)
portugal = portugal.rename(columns={'lat' : 'Latitud', 'lng' : 'Longitud', 'city' : 'Población', 'population' : 'Habitantes'})
portugal = portugal[portugal.admin_name != "Azores"]
portugal = portugal[portugal.admin_name != "Madeira"]

exclude = ['Comunidad','Provincia','Población','Altitud','Habitantes','Hombres','Mujeres']
data_longlat = data.loc[:, data.columns.difference(exclude)]

exclude2 = ['country', 'iso2', 'admin_name', 'capital', 'population_proper']
longlat_Portugal = portugal.loc[:, portugal.columns.difference(exclude2)]

data = data.append(longlat_Portugal, ignore_index=True)
longlat_Portugal = longlat_Portugal.loc[:, longlat_Portugal.columns.difference(['Población', 'Habitantes'])]
data_longlat = data_longlat.append(longlat_Portugal, ignore_index=True)


    

# 2.1 Parametrization
import sklearn.neighbors	
dist = sklearn.neighbors.DistanceMetric.get_metric('euclidean')
matsim = dist.pairwise(data_longlat)


minPts=15
from sklearn.neighbors import kneighbors_graph
A = kneighbors_graph(data_longlat, minPts, include_self=False)
Ar = A.toarray()

seq = []
for i,s in enumerate(data_longlat):
    for j in range(len(data_longlat)):
        if Ar[i][j] != 0:
            seq.append(matsim[i][j])
            
seq.sort()
plt.plot(seq)
plt.show()

# 2.2 DBSCAN Execution
from sklearn.cluster import DBSCAN
results = []
for eps in numpy.arange(1/6371.0088, 20/6371.0088, 1/6371.088):
  db = DBSCAN(eps, min_samples=minPts, metric='haversine').fit(numpy.radians(data_longlat))
  core_samples_mask = numpy.zeros_like(db.labels_, dtype=bool)
  core_samples_mask[db.core_sample_indices_] = True
  labels = db.labels_
  n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
  n_outliers = list(labels).count(-1)
 
  results.append([eps, n_clusters_, n_outliers])

#print results
from tabulate import tabulate
import numpy as np
print(tabulate(results, headers = ("eps", "clusters", "outliers")))

db = DBSCAN(eps=17/6371.0088, min_samples=minPts, metric='haversine').fit(np.radians(data_longlat))
labels = db.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
print(n_clusters_)




data['zona'] = labels
pd.set_option("display.max_rows", None, "display.max_columns", None)
#data.to_excel('municipios_cluster.xls')

# 4. plot
import plotly.express as px
fig = px.scatter(x=data_longlat['Longitud'], y=data_longlat['Latitud'], color = labels)
fig.show()








# 6. characterization
from sklearn import metrics
n_clusters_ = len(set(labels)) #- (1 if -1 in labels else 0)
print('Estimated number of clusters: %d' % n_clusters_)

print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(data_longlat, labels))
      
