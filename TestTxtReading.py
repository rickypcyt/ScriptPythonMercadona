import re
from tabulate import tabulate
from PyPDF2 import PdfReader


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

            # Buscar el precio de la banana en el texto de la factura
            if "BANANA" in descripcion.upper() and not siguiente_importe:
                for siguiente_linea in lineas_factura[idx + 1 :]:
                    match_importe_siguiente = re.search(
                        r"(\d+[.,]\d{2})", siguiente_linea
                    )
                    if match_importe_siguiente:
                        siguiente_importe = float(
                            match_importe_siguiente.group(1).replace(",", ".")
                        )
                        break

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


archivo_path = "ScriptPythonMercadona/Descargas Mails/20231213 Mercadona 14,55 €.pdf"
texto_factura = extraer_texto_factura(archivo_path)
datos_factura, total_factura = extraer_datos_factura(texto_factura)

total_formateado = f"{total_factura:.2f}"

tabla_factura = tabulate(
    datos_factura, headers=["Descripción", "Cantidad", "Importe"], tablefmt="plain"
)
tabla_factura += f"\nTOTAL: {total_formateado}"

print(tabla_factura)

