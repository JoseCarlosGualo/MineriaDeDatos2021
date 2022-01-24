import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn import tree
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt
import numpy as np

# DEFINICION PARA LA FUNCION ENCARGADA DE CALCULAR EL PORCENTAJE DE VIAJES DESTINADOS A UNA ZONA
def getPercentage(row,total_viajes):
    return (row['VOLUMEN']/total_viajes) * 100

# CARGAMOS LOS DATOS DEL ARCHIVO TABLA_PORCENTAJES.csv
df_result = pd.read_csv("TABLA_VOLUMENES.csv")

# DEFINIMOS LOS ATRIBUTOS QUE USAREMOS EN LAS PREDICCIONES
feature_names_clf = ['ZONA_ORIGEN', 'ZONA_DESTINO', 'DIA_SEMANA', 'SEMANA']
X = df_result[feature_names_clf]
# DEFINIMOS EL ATRIBUTO OBJETIVO DE LAS PREDICCIONES
Y = df_result['VOLUMEN']
print("X shape {}: ".format(X.shape))
print("Y shape {}: ".format(Y.shape))

destinos = []
destinos = df_result['ZONA_DESTINO'].unique()


# DIVIDIMOS EL DATASET PARA SU ENTRENAMIENTO: 40%->TESTING --- 60%->ENTRENAMIENTO
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)
regressor = RandomForestRegressor(n_estimators= 15, max_depth = 10, criterion='absolute_error', random_state=0)
# ENTRENAMOS EL ALGORITMO DE REGRESION
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
# CALCULO DEL ERROR MEDIO
mae = mean_absolute_error(y_test,y_pred)
print ("Error Measure ",  mae)

# VEMOS LA GRÁFICA PARA 
xx = np.stack(i for i in range(len(y_test)))
plt.scatter(xx, y_test, c='r', label='data')
plt.plot(xx, y_pred, c='g', label='prediction')
plt.axis('tight')
plt.legend()
plt.title("RandomForests Regressor")

plt.show()

observaciones_zona_origen = []
observaciones_zona_destino = []
observaciones_dia_semana = []
observaciones_semana = []
observaciones_volumen = []
default_dia_semana = 6
default_semana = 1  
default_zona_origen = 28
for zona_destino in range(0,29):
    if zona_destino in destinos:
        to_predict = [default_zona_origen,zona_destino,default_dia_semana,default_semana]
        result = regressor.predict([to_predict])
        observaciones_dia_semana.append(default_dia_semana)
        observaciones_semana.append(default_semana)
        observaciones_zona_destino.append(zona_destino)
        observaciones_zona_origen.append(default_zona_origen)
        observaciones_volumen.append(int(result[0]))

observaciones = pd.DataFrame(list(zip(observaciones_zona_origen,observaciones_zona_destino,observaciones_dia_semana,observaciones_semana,observaciones_volumen)), columns = ['ZONA_ORIGEN','ZONA_DESTINO','DIA_SEMANA','SEMANA','VOLUMEN'])
total_viajes = observaciones['VOLUMEN'].sum()
observaciones["PORCENTAJE"] = observaciones.apply(lambda row: getPercentage(row,total_viajes), axis=1)
print(observaciones)
    
