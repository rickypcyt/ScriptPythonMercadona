import os
import re
from tabulate import tabulate
from collections import defaultdict
import calendar
from PyPDF2 import PdfReader

base_dir = '/Users/user/Dropbox/Mac/Desktop/Projects/Python/pythonProject1/ScriptPythonMercadona'

def extraer_datos_factura(texto_factura):
    inicio = texto_factura.find("Descripción")
    fin = texto_factura.find("TOTAL")
    texto_factura = texto_factura[inicio:fin]

    lineas_factura = texto_factura.split("\n")

    patron_descripcion = (
        r"[^\W\d_]+(?:\s+[^\W\d_]+)*"  # Expresión regular para extraer solo texto
    )

    patron_cantidad = r"(\d+)\s*[^\W\d_]+(?:\s+[^\W\d_]+)*"

    patron_precio_unitario = r"(\d+[.,]\d{2})\s*(?=[^\d.,\n]*\d)"

    datos_factura = []
    total_factura = 0.0
    siguiente_importe = None

    for idx, linea in enumerate(lineas_factura[1:]):
        match_descripcion = re.search(patron_descripcion, linea)
        match_cantidad = re.search(patron_cantidad, linea)
        match_precio_unitario = re.search(patron_precio_unitario, linea)

        if match_descripcion and match_cantidad:
            descripcion = match_descripcion.group(0).strip()
            cantidad = match_cantidad.group(1)

            if "BANANA" in descripcion.upper() and not siguiente_importe:
                siguiente_linea_idx = idx + 1
                for _ in range(1):  # Saltar las dos primeras líneas después de BANANA
                    siguiente_linea_idx += 1
                    if siguiente_linea_idx >= len(lineas_factura):
                        break
                if siguiente_linea_idx < len(lineas_factura):
                    siguiente_linea = lineas_factura[siguiente_linea_idx]
                    match_importe_siguiente = re.search(
                        r"(\d+[.,]\d{2})", siguiente_linea
                    )
                    if match_importe_siguiente:
                        siguiente_importe = float(
                            match_importe_siguiente.group(1).replace(",", ".")
                        )

            if "BANANA" in descripcion.upper() and siguiente_importe:
                importe = siguiente_importe
                siguiente_importe = None
            elif match_precio_unitario:
                precio_unitario = float(
                    match_precio_unitario.group(1).replace(",", ".")
                )
                importe = precio_unitario * int(cantidad)
            else:
                match_importe = re.search(r"(\d+[.,]\d{2})", linea)
                if match_importe:
                    importe = float(match_importe.group(1).replace(",", "."))
                else:
                    importe = None

                if "BANANA" in descripcion.upper() and idx + 1 < len(lineas_factura):
                    siguiente_linea = lineas_factura[idx + 1]
                    match_importe_siguiente = re.search(
                        r"(\d+[.,]\d{2})", siguiente_linea
                    )
                    if match_importe_siguiente:
                        importe = float(
                            match_importe_siguiente.group(1).replace(",", ".")
                        )

            if importe is not None:
                importe = round(importe, 2)
                if (
                    "kg" not in descripcion.lower()
                ):  # Verificar si 'kg' está en la descripción
                    datos_factura.append((descripcion, cantidad, importe))
                    total_factura += importe

    datos_factura.sort(key=lambda x: x[0])

    return datos_factura, round(total_factura, 2)


def extraer_texto_factura(archivo_path):
    with open(archivo_path, "rb") as archivo_pdf:
        pdf_reader = PdfReader(archivo_path)
        texto_extraido = ""
        for pagina in range(len(pdf_reader.pages)):
            texto_extraido += pdf_reader.pages[pagina].extract_text()
    return texto_extraido


directorio_entrada = os.path.join(base_dir, 'Descargas Mails')
directorio_salida = os.path.join(base_dir, 'OutputPdfsV2')

datos_por_ano_mes = defaultdict(lambda: defaultdict(list))

for archivo_name in os.listdir(directorio_entrada):
    if archivo_name.endswith(".pdf"):
        print(f"Processing file: {archivo_name}")  # Debug print
        archivo_path = os.path.join(directorio_entrada, archivo_name)
        texto_factura = extraer_texto_factura(archivo_path)
        datos_factura, total_factura = extraer_datos_factura(texto_factura)
        print(f"Extracted data for {archivo_name}: {datos_factura}")  # Debug print
        fecha = archivo_name.split()[0]
        ano = fecha[:4]
        mes = fecha[4:6]
        nombre_mes = calendar.month_name[int(mes)]
        datos_por_ano_mes[ano][nombre_mes].extend(datos_factura)
        datos_por_ano_mes[ano][nombre_mes].append(("TOTAL", "", total_factura))

for ano, datos_por_mes in datos_por_ano_mes.items():
    for mes, datos_mes in datos_por_mes.items():
        tabla_mes = tabulate(datos_mes, headers=["Item", "Cantidad", "Total"], tablefmt="pretty")
        tabla_mes = f"\nMes: {mes} | Año: {ano}\n" + tabla_mes
        nombre_archivo = f"datos_facturas_{ano}_{mes}.txt"
        ruta_archivo = os.path.join(directorio_salida, nombre_archivo)
        print(f"Writing to {ruta_archivo}")  # Debug print
        print(tabla_mes)  # Debug print
        with open(ruta_archivo, "w", encoding="utf-8") as archivo_salida:
            total_formateado = f"{datos_mes[-1][2]:.2f}"
            tabla_mes = tabla_mes.replace(str(datos_mes[-1][2]), total_formateado)
            archivo_salida.write(tabla_mes)