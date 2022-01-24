import pandas as pd
import numpy as np


df = pd.read_csv("Tabla_Volumen.csv")
table = pd.pivot_table(df, values='VOLUMEN', index=['ORIGEN','FLUJO', 'SEMANA'],
                    columns=['ZONA_DESTINO'], aggfunc=np.sum)
table = table.fillna(value=0)



#table.to_csv("tabla_pivotada.csv")

#Clasificando según el flujo, para posible tratamiento futuro (0 INTERNO, 1 SALIENTE, 2 ENTRANTE)

f_mantiene = table.iloc[(table.index.get_level_values('FLUJO') == 0)] 
f_saliente = table.iloc[table.index.get_level_values('FLUJO') == 1] 
f_interno = table.iloc[table.index.get_level_values('FLUJO') == 2]

#Nos quedamos solo con las capitales de provincia para la prueba, flujo saliente
aux = table.iloc[(table.index.get_level_values('ORIGEN') == 'Albacete') | (table.index.get_level_values('ORIGEN') == 'Ciudad Real') | (table.index.get_level_values('ORIGEN') == 'Toledo') | (table.index.get_level_values('ORIGEN') == 'Cuenca') | (table.index.get_level_values('ORIGEN') == 'Guadalajara')]
salienteCLM = aux.iloc[aux.index.get_level_values('FLUJO') == 1]

print(salienteCLM.head())
#salienteCLM.to_csv("flujoSalienteCLM.csv")