import os
import re
from tabulate import tabulate
from collections import defaultdict
import calendar

def extraer_datos_factura(texto_factura):
    # Buscar la parte del texto que va desde la descripción hasta la palabra "TOTAL"
    inicio = texto_factura.find("Descripción")
    fin = texto_factura.find("TOTAL")
    texto_factura = texto_factura[inicio:fin]
    
    # Dividir el texto de la factura en líneas
    lineas_factura = texto_factura.split('\n')
    
    # Patrones de expresiones regulares para encontrar la descripción, cantidad y importe
    patron_descripcion = r'[\dA-Za-zÁ-Úá-ú\s.,]+'
    patron_cantidad = r'(\d+)([.,]\d+)?'
    patron_importe = r'(\d+[.,]\d{2})'
    
    # Lista para almacenar los datos de la factura
    datos_factura = []
    
    # Iterar sobre las líneas de la factura, omitiendo la primera fila que contiene los encabezados
    for linea in lineas_factura[1:]:
        # Buscar coincidencias en cada línea de la factura
        match_descripcion = re.search(patron_descripcion, linea)
        match_cantidad = re.search(patron_cantidad, linea)
        match_importe = re.search(patron_importe, linea)
        
        # Verificar si se encontraron todas las coincidencias
        if match_descripcion and match_cantidad and match_importe:
            descripcion = match_descripcion.group(0).strip()
            cantidad = match_cantidad.group(0)
            importe = match_importe.group(0)
            
            # Agregar los datos a la lista de la factura
            datos_factura.append((descripcion, cantidad, importe))
    
    return datos_factura


# Directorio que contiene los archivos de texto de las facturas
directorio = "ScriptPythonMercadona/PDF to TXT/"

# Diccionario para almacenar los datos de todas las facturas por año y mes
datos_por_ano_mes = defaultdict(lambda: defaultdict(list))

# Iterar sobre los archivos en el directorio
for archivo_name in os.listdir(directorio):
    if archivo_name.endswith(".txt"):
        archivo_path = os.path.join(directorio, archivo_name)
        with open(archivo_path, 'r', encoding='utf-8') as archivo:
            texto_factura = archivo.read()
            datos_factura = extraer_datos_factura(texto_factura)
            # Extraer la fecha del nombre del archivo (formato YYYYMMDD)
            fecha = archivo_name.split()[0]
            ano = fecha[:4]  # Extraer el año
            mes = fecha[4:6]  # Extraer el mes
            # Convertir el número del mes a su nombre correspondiente
            nombre_mes = calendar.month_name[int(mes)]
            # Agregar los datos de la factura al diccionario correspondiente al año y mes
            datos_por_ano_mes[ano][nombre_mes].extend(datos_factura)

# Guardar los datos en archivos de texto
for ano, datos_por_mes in datos_por_ano_mes.items():
    for mes, datos_mes in datos_por_mes.items():
        tabla_mes = tabulate(datos_mes, headers=["Descripción", "Cantidad", "Importe"], tablefmt="pretty")
        tabla_mes = f"\nMes: {mes} | Año: {ano}\n" + tabla_mes
        nombre_archivo = f"datos_facturas_{ano}_{mes}.txt"
        with open(nombre_archivo, "w", encoding='utf-8') as archivo_salida:
            archivo_salida.write(tabla_mes)
