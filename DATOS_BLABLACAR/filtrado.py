import os
import pandas as pd

class filtrado:
    def main(self):
        # Creamos un dataframe con las fechas de las festividades de Castilla la mancha
        #df_fechas = pd.read_csv('FESTIVIDADES.txt', sep= " ", header= 0)
        
        # Creamos un dataframe con los datos de la aplicación de BLABLACAR
        df_blablacar = pd.read_csv('DATOS_BLABLACAR.txt', sep= "|", header=0)
        
        # Creamos un dataframe de un archivo con información sobre municipios de Castilla la mancha
        df_municipios = pd.read_csv('Municipios_de_Castilla-La_Mancha.csv', sep= ",", header=0)
        # Hacemos una lista con todos los municipios para luego saber si pertenecen o no a Castilla la Mancha las ciudades de 
        # origen y destino de los datos de BLABLACAR
        lista_municipios = df_municipios['NAMEUNIT'].to_list()
        
        # Creamos los filtros, y usamos el metodo loc para crear un nuevo dataset que será nuestra tarjeta de datos
        filter_origen = df_blablacar['ORIGEN'].isin(lista_municipios)
        filter_destino = df_blablacar['DESTINO'].isin(lista_municipios)
        dataframe = df_blablacar.loc[(filter_origen | filter_destino) & (df_blablacar['ASIENTOS_CONFIRMADOS'] != 0) & (df_blablacar['VIAJES_CONFIRMADOS'] != 0)]
        print(dataframe)

        print("dataframe: " + str(len(dataframe)))
        print("blablacar: "+ str(len(df_blablacar)))

        df_dataframe = pd.DataFrame(dataframe)
        df_dataframe.to_csv("dataset.csv")

if __name__ == '__main__':
    filtrado_ins = filtrado()
    filtrado_ins.main()