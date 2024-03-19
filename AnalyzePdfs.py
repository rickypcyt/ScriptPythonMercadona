import os
import re
from collections import defaultdict
from tabulate import tabulate

def extraer_datos_factura(texto_factura):
    # Tu función extraer_datos_factura aquí
    pass

def analizar_carpeta(ruta_carpeta):
    # Diccionario para almacenar los datos agrupados por año y mes
    datos_por_fecha = defaultdict(list)
    
    # Recorre todos los archivos en la carpeta
    for nombre_archivo in os.listdir(ruta_carpeta):
        # Verifica si el nombre del archivo coincide con el patrón de fecha
        match_fecha = re.match(r'(\d{4})(\d{2})(\d{2})\sMercadona\s(\d+,\d{2})\s€\.txt', nombre_archivo)
        if match_fecha:
            # Extrae el año, mes y día del nombre del archivo
            anho = match_fecha.group(1)
            mes = match_fecha.group(2)
            dia = match_fecha.group(3)
            precio = match_fecha.group(4)
            
            # Lee el contenido del archivo
            with open(os.path.join(ruta_carpeta, nombre_archivo), 'r', encoding='utf-8') as archivo:
                texto_factura = archivo.read()
            
            # Extrae datos de la factura
            datos_factura = extraer_datos_factura(texto_factura)
            
            # Agrega los datos al diccionario agrupado por año y mes
            datos_por_fecha[(anho, mes, dia)].append((nombre_archivo, precio, datos_factura))
    
    return datos_por_fecha

def guardar_datos_por_fecha(datos_por_fecha):
    for (anho, mes, dia), datos in datos_por_fecha.items():
        # Crear tabla con los datos extraídos
        tabla = tabulate(datos, headers=["Nombre Archivo", "Precio", "Descripción", "Cantidad", "Importe"], tablefmt="grid")
        
        # Guardar la tabla en un archivo de texto
        nombre_archivo_salida = f"datos_factura_{anho}_{mes}_{dia}.txt"
        with open(nombre_archivo_salida, "w", encoding='utf-8') as archivo_salida:
            archivo_salida.write(tabla)

# Ruta de la carpeta que contiene los archivos
ruta_carpeta = "ScriptPythonMercadona\Descargas Mails"

# Analizar la carpeta y obtener los datos agrupados por fecha
datos_por_fecha = analizar_carpeta(ruta_carpeta)

# Guardar los datos por fecha en archivos de texto separados
guardar_datos_por_fecha(datos_por_fecha)
