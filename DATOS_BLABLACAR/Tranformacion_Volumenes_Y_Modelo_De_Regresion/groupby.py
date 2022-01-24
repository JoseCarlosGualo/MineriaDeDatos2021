import pandas as pd
import numpy as np
df_result = pd.read_csv("Tabla_Volumen.csv", index_col=[0])
df_result.drop(df_result.loc[df_result['FLUJO']!= 1].index, inplace=True)
df_result = df_result.groupby(["ZONA_ORIGEN", "ZONA_DESTINO", "DIA_SEMANA", "SEMANA"], as_index=False)["VOLUMEN"].count()
df_result.to_csv("grouped.csv",index=False)

def sum1(row, df_result):
    zona_origen = [row["ZONA_ORIGEN"]]
    dia_semana = [row["DIA_SEMANA"]]
    semana = [row["SEMANA"]]
    df_aux = df_result[df_result.ZONA_ORIGEN.isin(zona_origen) & df_result.DIA_SEMANA.isin(dia_semana) & df_result.SEMANA.isin(semana)]
    return df_aux["VOLUMEN"].sum()

def changeClsOr(row):
    if row["ZONA_ORIGEN"] == 101:
        return int(25)
    elif row["ZONA_ORIGEN"] == 102:
        return int(26)
    elif row["ZONA_ORIGEN"] == 103:
        return int(27)
    elif row["ZONA_ORIGEN"] == 104:
        return int(28)
    else:
        return int(row["ZONA_ORIGEN"])
    
def changeClsDes(row):
    if row["ZONA_DESTINO"] == 101:
        return int(25)
    elif row["ZONA_DESTINO"] == 102:
        return int(26)
    elif row["ZONA_DESTINO"] == 103:
        return int(27)
    elif row["ZONA_DESTINO"] == 104:
        return int(28)
    else:
        return int(row["ZONA_DESTINO"])

def getPercentage(row):
    return (row["VOLUMEN"]/row["TOTAL"]) * 100

def discretizeDayOfWeek(row):
        if row["DIA_SEMANA"] == "Lunes":
            return 0
        elif row["DIA_SEMANA"] == "Martes":
            return 1
        elif row["DIA_SEMANA"] == "Miercoles":
            return 2
        elif row["DIA_SEMANA"] == "Jueves":
            return 3
        elif row["DIA_SEMANA"] == "Viernes":
            return 4
        elif row["DIA_SEMANA"] == "Sabado":
            return 5
        elif row["DIA_SEMANA"] == "Domingo":
            return 6
        else:
            return ""
        
# APLICAMOS LOS FILTROS Y AÑADIMOS LA COLUNMA QUE ALMACENE EL PORCENTAJE
df_result["TOTAL"] = df_result.apply(lambda row: sum1(row,df_result), axis=1)
df_result["DIA_SEMANA"] = df_result.apply(lambda row: discretizeDayOfWeek(row), axis=1)
df_result["ZONA_ORIGEN"] = df_result.apply(lambda row: changeClsOr(row), axis=1)
df_result["ZONA_DESTINO"] = df_result.apply(lambda row: changeClsDes(row), axis=1)
df_result.drop(["TOTAL"], axis=1, inplace=True)
df_result.to_csv("TABLA_VOLUMENES.csv",index=False)

# EJEMPLO PARA VER LOS PORCENTAJES DESDE UNA ZONA EN UN DIA CONCRETO
zona_origen = [10]
dia_semana = [6]
semana = [2]
df_pruebas = df_result[df_result.ZONA_ORIGEN.isin(zona_origen) & df_result.DIA_SEMANA.isin(dia_semana) & df_result.SEMANA.isin(semana)]
print(df_pruebas)
