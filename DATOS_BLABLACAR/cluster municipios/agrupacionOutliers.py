import pandas as pd


data = pd.read_excel("municipios_cluster.xls")
outliers = data.loc[data['zona'] == -1,:]
max_lon = data['Longitud'].max()
min_lon = data['Longitud'].min()
min_lat = data['Latitud'].min()
max_lat = data['Latitud'].max()

print("Latitud mínima ",min_lat," Latitud maxima ",max_lat) #Valor medio aproximado 39.5
print("Longitud mínima ",min_lon," Longitud maxima ",max_lon) #Valor medio aproximado -4.3

data.loc[(data['zona'] == -1) & (data['Longitud'] < -4.3) & (data['Latitud'] > 39.5), 'zona'] = 25  #Zona noroeste
data.loc[(data['zona'] == -1) & (data['Longitud'] > -4.3) & (data['Latitud'] > 39.5), 'zona'] = 26 #Zona noreste
data.loc[(data['zona'] == -1) & (data['Longitud'] < -4.3) & (data['Latitud'] < 39.5), 'zona'] = 27 #Zona suroeste
data.loc[(data['zona'] == -1) & (data['Longitud'] > -4.3) & (data['Latitud'] < 39.5), 'zona'] = 28 #Zona sureste

labels = data['zona']
data.drop(columns=['Unnamed: 0'])

import plotly.express as px
fig = px.scatter(x=data['Longitud'], y=data['Latitud'], color = labels)
fig.show()

print(data.head())
data.to_excel("municipios_cluster_final.xls")


