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

    patron_descripcion = (
        r"[^\W\d_]+(?:\s+[^\W\d_]+)*"  # Expresión regular para extraer solo texto
    )

    patron_cantidad = r"(\d+)\s*[^\W\d_]+(?:\s+[^\W\d_]+)*"

    patron_precio_unitario = r"(\d+[.,]\d{2})\s*(?=[^\d.,\n]*\d)"

    datos_factura = []
    total_factura = 0.0

    for linea in lineas_factura[1:]:
        match_descripcion = re.search(patron_descripcion, linea)
        match_cantidad = re.search(patron_cantidad, linea)
        match_precio_unitario = re.search(patron_precio_unitario, linea)

        if match_descripcion and match_cantidad:
            descripcion = match_descripcion.group(0).strip()
            cantidad = match_cantidad.group(1)

            if match_precio_unitario:
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

            if importe is not None:
                importe = round(importe, 2)
                if "kg" not in descripcion.lower():
                    datos_factura.append((descripcion, int(cantidad), importe))
                    total_factura += importe

    return datos_factura, round(total_factura, 2)


base_dir = "/Users/user/Dropbox/Mac/Desktop/Projects/Python/pythonProject1/ScriptPythonMercadona"

directorio_entrada = "ScriptPythonMercadona/PDF to TXT/"
directorio_salida = "ScriptPythonMercadona/OutputTxtsV2/"

datos_totales = defaultdict(list)

for archivo_name in os.listdir(directorio_entrada):
    if archivo_name.endswith(".txt"):
        archivo_path = os.path.join(directorio_entrada, archivo_name)
        with open(archivo_path, "r", encoding="utf-8") as archivo:
            texto_factura = archivo.read()
            datos_factura, _ = extraer_datos_factura(texto_factura)
            for item, cantidad, importe in datos_factura:
                datos_totales[item].append((cantidad, importe))

# Calcular el total de todos los ítems combinados por mes y consolidar datos
total_por_mes = defaultdict(float)
factura_grande_por_mes = defaultdict(list)

for archivo_name in os.listdir(directorio_entrada):
    if archivo_name.endswith(".txt"):
        archivo_path = os.path.join(directorio_entrada, archivo_name)
        with open(archivo_path, "r", encoding="utf-8") as archivo:
            texto_factura = archivo.read()
            datos_factura, total_factura = extraer_datos_factura(texto_factura)
            fecha = archivo_name.split()[0]
            ano = fecha[:4]
            mes = fecha[4:6]
            nombre_mes = calendar.month_name[int(mes)]
            # Almacenar los datos de la factura para la consolidación
            factura_grande_por_mes[(ano, nombre_mes)].extend(datos_factura)
            # Calcular el total de la factura sumando los importes
            total_por_mes[(ano, nombre_mes)] += total_factura

# Guardar la factura consolidada por mes en archivos de texto
for (ano, mes), total_mes in total_por_mes.items():
    nombre_archivo_mes = f"Factura_Consolidada_{mes.lower()}_{ano}.txt"
    ruta_archivo_mes = os.path.join(directorio_salida, nombre_archivo_mes)
    with open(ruta_archivo_mes, "w", encoding="utf-8") as archivo_salida_mes:
        archivo_salida_mes.write(f"Factura Consolidada para {mes} {ano}\n\n")
        archivo_salida_mes.write(
            tabulate(
                factura_grande_por_mes[(ano, nombre_mes)],
                headers=["Item", "Cantidad", "Total"],
                tablefmt="plain",
            )
        )
        archivo_salida_mes.write(f"\n\nTotal del Mes: {total_mes:.2f}\n")
