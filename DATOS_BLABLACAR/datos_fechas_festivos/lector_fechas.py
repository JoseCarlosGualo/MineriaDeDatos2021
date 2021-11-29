import os
import pandas as pd

class lector_fechas:
    def main(self):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        
        with os.scandir(dir_path) as ficheros:
            ficheros = [fichero.name for fichero in ficheros if fichero.is_file() and fichero.name.endswith('.xlsx')]
        
        age = 2017
        
        aux = []
        fechas_letras = []
        for fichero in ficheros:
            df = pd.read_excel(fichero)
            for i in df.index:
                fechas_letras.append(df['festividades'][i].split(sep = ",")[0] + " " +str(age))
            age = age + 1
        
        for fecha in fechas_letras:
            dia = fecha.replace("de", "")
            dia_list = dia.split()
            aux.append(dia_list)
         
        file = open(os.path.pardir + "\\FESTIVIDADES.txt", "w")
        file.write("\"FESTIVIDAD\"" + "\n")
        numero_mes = ""
        str_mes = ""
        for fecha in aux:
            str_mes = fecha[1]
            if str_mes == "enero":
                numero_mes = "01"
            elif str_mes == "febrero":
                numero_mes = "02"
            elif str_mes == "marzo":
                numero_mes = "03"
            elif str_mes == "abril":
                numero_mes = "04"
            elif str_mes == "mayo":
                numero_mes = "05"
            elif str_mes == "junio":
                numero_mes = "06"
            elif str_mes == "julio":
                numero_mes = "07"
            elif str_mes == "agosto":
                numero_mes = "08"
            elif str_mes == "septiembre":
                numero_mes = "09"
            elif str_mes == "octubre":
                numero_mes = "10"
            elif str_mes == "noviembre":
                numero_mes = "11"
            elif str_mes == "diciembre":
                numero_mes = "12"
            
            cadena = "\""+ fecha[0] +"/"+ numero_mes +"/"+ fecha[2] +"\"" + "\n"
            if len(cadena) < 13:
                cadena = "\""+ "0" + fecha[0] +"/"+ numero_mes +"/"+ fecha[2] +"\"" + "\n"
            
            file.write(cadena)
            
            

if __name__ == '__main__':
    lector_fechas_ins = lector_fechas()
    lector_fechas_ins.main()