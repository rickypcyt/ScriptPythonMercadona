import os
import re
from tabulate import tabulate
from collections import defaultdict
import calendar
from PyPDF2 import PdfReader


def extraer_datos_factura(texto_factura):
    inicio = texto_factura.find("Descripción")
    fin = texto_factura.find("TOTAL")
    texto_factura = texto_factura[inicio:fin]

    lineas_factura = texto_factura.split("\n")

    patron_descripcion = r"\d+\s*[\dA-Za-zÁ-Úá-ú.,]+"
    patron_importe = r"(\d+[.,]\d{2})"

    datos_factura = []
    total_factura = 0.0

    for linea in lineas_factura[1:]:
        match_descripcion = re.search(patron_descripcion, linea)
        match_importe = re.search(patron_importe, linea)

        if match_descripcion and match_importe:
            cantidad_descripcion = match_descripcion.group(0).strip()
            cantidad, descripcion = re.match(
                r"(\d+)\s*(.*)", cantidad_descripcion
            ).groups()
            importe = float(match_importe.group(0).replace(",", "."))

            datos_factura.append((descripcion, cantidad, importe))
            total_factura += importe

    datos_factura.sort(key=lambda x: x[0])

    return datos_factura, total_factura


def extraer_texto_factura(archivo_path):
    with open(archivo_path, "rb") as archivo_pdf:
        pdf_reader = PdfReader(archivo_pdf)
        texto_extraido = ""
        for pagina in range(len(pdf_reader.pages)):
            texto_extraido += pdf_reader.pages[pagina].extract_text()
    return texto_extraido


directorio_entrada = "ScriptPythonMercadona/Descargas Mails/"
directorio_salida = "ScriptPythonMercadona/OutputPdfsV2"

datos_por_ano_mes = defaultdict(lambda: defaultdict(list))

for archivo_name in os.listdir(directorio_entrada):
    if archivo_name.endswith(".pdf"):
        archivo_path = os.path.join(directorio_entrada, archivo_name)
        texto_factura = extraer_texto_factura(archivo_path)
        datos_factura, total_factura = extraer_datos_factura(texto_factura)
        fecha = archivo_name.split()[0]
        ano = fecha[:4]
        mes = fecha[4:6]
        nombre_mes = calendar.month_name[int(mes)]
        datos_por_ano_mes[ano][nombre_mes].extend(datos_factura)
        datos_por_ano_mes[ano][nombre_mes].append(("TOTAL", "", total_factura))

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
            #Habla Morenei 