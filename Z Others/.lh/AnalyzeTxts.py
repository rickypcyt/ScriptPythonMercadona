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

    patron_descripcion = (
        r"[^\W\d_]+(?:\s+[^\W\d_]+)*"  # Expresión regular para extraer solo texto
    )

    patron_cantidad = r"(\d+)\s*[^\W\d_]+(?:\s+[^\W\d_]+)*"

    patron_precio_unitario = r"(\d+[.,]\d{2})\s*(?=[^\d.,\n]*\d)"

    datos_factura = []
    total_factura = 0.0
    siguiente_importe = None

    for idx, linea in enumerate(lineas_factura[1:]):
        # match_descripcion looks for the quantity and description of the2 item
        match_descripcion = re.search(patron_descripcion, linea)
        match_cantidad = re.search(patron_cantidad, linea)
        match_precio_unitario = re.search(patron_precio_unitario, linea)

        if match_descripcion and match_cantidad:
            # Retrieves the matched string and removes white spaces
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

            if "MANZANA GRANNY" in descripcion.upper() and not siguiente_importe:
                siguiente_linea_idx = idx + 1
                for _ in range(
                    1
                ):  # Saltar las dos primeras líneas después de MANZANA GRANNY
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
            elif "MANZANA GRANNY" in descripcion.upper() and siguiente_importe:
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
                elif "MANZANA GRANNY" in descripcion.upper() and idx + 1 < len(
                    lineas_factura
                ):
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

    # Sorting before returning, lambda is a way of creating an anonymous function, used as a short one
    # Takes an argument x (each tuple in datos_factura) and returns first element in the tuple, sort by description a-z

    datos_factura.sort(key=lambda x: x[0])

    return datos_factura, round(total_factura, 2)


def extraer_texto_factura(archivo_path):
    with open(archivo_path, "r", encoding="utf-8") as archivo:
        texto_extraido = archivo.read()
    return texto_extraido


base_dir = "/Users/user/Dropbox/Mac/Desktop/Projects/Python/pythonProject1/ScriptPythonMercadona"

directorio_entrada = "ScriptPythonMercadona/PDF to TXT/"
directorio_salida = "ScriptPythonMercadona/OutputTxtsV2/"

# Diccionario para almacenar los datos de todas las facturas por año y mes
datos_por_ano_mes = defaultdict(lambda: defaultdict(list))

# Iterar sobre los archivos en el directorio
for archivo_name in os.listdir(directorio_entrada):
    # iterates through the files that end with .txt
    if archivo_name.endswith(".txt"):
        # Combine the directory path and the file name into a pull path to the file os.path.join()
        archivo_path = os.path.join(directorio_entrada, archivo_name)
        with open(archivo_path, "r", encoding="utf-8") as archivo:
            # Reads the entire content of the file into the variable "texto_factura"
            texto_factura = archivo.read()
            # Calls function extraer with the text of the invoice, returns list of tuples with item data and tot amount
            datos_factura, total_factura = extraer_datos_factura(
                texto_factura
            )  # It takes the first part as the date
            fecha = archivo_name.split()[0]  # It takes the first part as the date
            ano = fecha[:4]  # Extraer el año
            mes = fecha[4:6]  # Extraer el mes
            nombre_mes = calendar.month_name[
                int(mes)
            ]  # Convert the month num to an integer and then to its month
            # Extends the list of data for the specific year and month with new invoice data, appends tuple and total amount
            datos_por_ano_mes[ano][nombre_mes].extend(datos_factura)
            datos_por_ano_mes[ano][nombre_mes].append(
                (
                    "TOTAL",
                    "",
                    total_factura,
                )
            )
# Guardar los datos en archivos de texto en el directorio de salida
for ano, datos_por_mes in datos_por_ano_mes.items():  # Each year
    for (
        mes,
        datos_mes,
    ) in datos_por_mes.items():  # For each year, loops through each month
        tabla_mes = tabulate(
            datos_mes, headers=["Item", "Cantidad", "Total"], tablefmt="pretty"
        )
        tabla_mes = (
            f"\nMes: {mes} | Año: {ano}\n" + tabla_mes
        )  # Uses the tabulate library to format the data into table
        nombre_archivo = f"datos_facturas_{ano}_{mes}.txt"  # Constructs a filename for the output file based on year and month
        ruta_archivo = os.path.join(
            directorio_salida, nombre_archivo
        )  # Joins the output directory path and filename
        with open(
            ruta_archivo, "w", encoding="utf-8"
        ) as archivo_salida:  # Opens a file for writing
            total_formateado = f"{datos_mes[-1][2]:.2f}"
            tabla_mes = tabla_mes.replace(str(datos_mes[-1][2]), total_formateado)
            archivo_salida.write(tabla_mes)  # writes formatted table to the output file
