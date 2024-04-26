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

    patron_descripcion = r"[^\W\d_]+(?:\s+[^\W\d_]+)*"
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

            if (
                "BANANA" in descripcion.upper()
                or "MANZANA GRANNY" in descripcion.upper()
                or "LIMON" in descripcion.upper()
            ) and not siguiente_importe:
                siguiente_linea_idx = idx + 1
                for _ in range(
                    1
                ):  # Saltar las dos primeras líneas después de BANANA o MANZANA GRANNY
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

            if (
                "BANANA" in descripcion.upper()
                or "MANZANA GRANNY" in descripcion.upper()
                or "LIMON" in descripcion.upper()
            ) and siguiente_importe:
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

                if (
                    "BANANA" in descripcion.upper()
                    or "MANZANA GRANNY" in descripcion.upper()
                    or "LIMON" in descripcion.upper()
                ) and idx + 1 < len(lineas_factura):
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

    return datos_factura, round(total_factura, 2)


# El resto del código permanece igual hasta el procesamiento final

base_dir = "/Users/user/Dropbox/Mac/Desktop/Projects/Python/pythonProject1/ScriptPythonMercadona"
directorio_entrada = "ScriptPythonMercadona/PDF to TXT/"
directorio_salida = "ScriptPythonMercadona/OutputTxtsV2/"

datos_por_ano_mes = defaultdict(
    lambda: defaultdict(lambda: defaultdict(lambda: [0, 0.0]))
)

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
            total_cantidad_mes = sum(int(cantidad) for _, cantidad, _ in datos_factura)
            for descripcion, cantidad, precio_total in datos_factura:
                datos_por_ano_mes[ano][nombre_mes][descripcion][0] += int(cantidad)
                datos_por_ano_mes[ano][nombre_mes][descripcion][1] += precio_total
            datos_por_ano_mes[ano][nombre_mes]["TOTAL"][0] += total_cantidad_mes
            datos_por_ano_mes[ano][nombre_mes]["TOTAL"][1] += total_factura

for ano, datos_por_mes in sorted(datos_por_ano_mes.items()):
    for mes, datos_mes in datos_por_mes.items():
        datos_agrupados = [
            (item, cantidad, round(precio_total, 2))
            for item, (cantidad, precio_total) in sorted(datos_mes.items())
            if item != "TOTAL"
        ]
        total_mes = datos_mes["TOTAL"]
        total_cantidad_mes = total_mes[0]
        tabla_mes = tabulate(
            datos_agrupados, headers=["Item", "Cantidad", "Total"], tablefmt="pretty"
        )
        tabla_mes += (
            f"\nTotal Cantidad: {total_cantidad_mes:}, Total Precio: {total_mes[1]:.2f}"
        )

        nombre_archivo = f"datos_facturas_{ano}_{mes}.txt"
        ruta_archivo = os.path.join(directorio_salida, nombre_archivo)
        with open(ruta_archivo, "w", encoding="utf-8") as archivo_salida:
            archivo_salida.write(tabla_mes)
