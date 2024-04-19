import os
import re
from tabulate import tabulate
from collections import defaultdict
import calendar


def extraer_datos_factura(texto_factura):
    inicio = texto_factura.find("Descripción")
    fin = texto_factura.find("TOTAL")
    texto_factura = texto_factura[inicio:fin]

    lineas_factura = texto_factura.split("\n")

    # Included other characters such as ñ
    patron_descripcion = r"\d+\s*[\dA-Za-zÁ-Úá-úÑñÖöŻż.,]+"
    patron_importe = r"(\d+[.,]\d{2})"

    datos_factura = []
    total_factura = 0.0

    #[1:] Removed this, not necessary since we already start where we want
    for linea in lineas_factura:
        #Check these 2 and make sure they are actually finding what we need

        #match_descripcion looks for the quantity and description of the2 item
        match_descripcion = re.search(patron_descripcion, linea)
        #match_importe looks for the price of the item
        match_importe = re.search(patron_importe, linea)

        #Checks if both items were succesful, if not line is skipped
        if match_descripcion and match_importe:
            #Retrieves the matched string and removes white spaces
            cantidad_descripcion = match_descripcion.group(0).strip()
            #Separating quantity and description
            cantidad, descripcion = re.match(r"(\d+)\s*(.*)", cantidad_descripcion).groups()
            importe = float(match_importe.group(0).replace(",", "."))

            #Store in a tuple which cannot be changed (datatype)
            datos_factura.append((descripcion, cantidad, importe))
            total_factura += importe

    #Sorting before returning, lambda is a way of creating an anonymous function, used as a short one
    #Takes an argument x (each tuple in datos_factura) and returns first element in the tuple, sort by description a-z
    datos_factura.sort(key=lambda x: x[0])

    return datos_factura, total_factura


base_dir = '/Users/user/Dropbox/Mac/Desktop/Projects/Python/pythonProject1/ScriptPythonMercadona'
directorio_entrada = os.path.join(base_dir, 'PDF to TXT')
directorio_salida = os.path.join(base_dir, 'OutputTxtsV2')

# Diccionario para almacenar los datos de todas las facturas por año y mes
datos_por_ano_mes = defaultdict(lambda: defaultdict(list))

# Iterar sobre los archivos en el directorio
for archivo_name in os.listdir(directorio_entrada):
    if archivo_name.endswith(".txt"):
        archivo_path = os.path.join(directorio_entrada, archivo_name)
        with open(archivo_path, "r", encoding="utf-8") as archivo:
            texto_factura = archivo.read()
            datos_factura, total_factura = extraer_datos_factura(texto_factura)
            fecha = archivo_name.split()[0]
            ano = fecha[:4]  # Extraer el año
            mes = fecha[4:6]  # Extraer el mes
            nombre_mes = calendar.month_name[int(mes)]
            datos_por_ano_mes[ano][nombre_mes].extend(datos_factura)
            datos_por_ano_mes[ano][nombre_mes].append(("TOTAL", "", total_factura))

# Guardar los datos en archivos de texto en el directorio de salida
for ano, datos_por_mes in datos_por_ano_mes.items():
    for mes, datos_mes in datos_por_mes.items():
        tabla_mes = tabulate(
            datos_mes, headers=["Item", "Cantidad", "Total"], tablefmt="pretty"
        )
        tabla_mes = f"\nMes: {mes} | Año: {ano}\n" + tabla_mes
        nombre_archivo = f"datos_facturas_{ano}_{mes}.txt"
        ruta_archivo = os.path.join(directorio_salida, nombre_archivo)
        with open(ruta_archivo, "w", encoding="utf-8") as archivo_salida:
            archivo_salida.write(tabla_mes)
