import os
import re
from tabulate import tabulate
from collections import defaultdict
import calendar
from PyPDF2 import PdfReader

base_dir = '/Users/user/Dropbox/Mac/Desktop/Projects/Python/pythonProject1/ScriptPythonMercadona'
directorio_entrada = os.path.join(base_dir, 'Descargas Mails')
directorio_salida = os.path.join(base_dir, 'OutputPdfsV2')

def extraer_texto_factura(archivo_path):
    """Extract all text from a PDF file."""
    with open(archivo_path, "rb") as archivo_pdf:
        pdf_reader = PdfReader(archivo_path)
        texto_extraido = "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
    return texto_extraido

def extract_details_from_line(line):
    """Extracts quantity, description, and price from a given line of invoice data."""
    match = re.search(r"(\d+) ([\w\s]+) (\d+[.,]\d{2})$", line.strip())
    if match:
        quantity = int(match.group(1))
        description = match.group(2).strip()
        price = float(match.group(3).replace(',', '.'))  # Normalize decimal separator
        return quantity, description, price
    return None, None, None

def extraer_datos_factura(texto_factura):
    """Extract structured data from extracted text."""
    inicio = texto_factura.find("Descripción")
    fin = texto_factura.find("TOTAL")
    texto_factura = texto_factura[inicio:fin]

    lineas_factura = texto_factura.split("\n")
    datos_factura = defaultdict(lambda: [0, 0.0])  # Summing quantities and total prices

    for linea in lineas_factura:
        cantidad, descripcion, importe = extract_details_from_line(linea)
        if cantidad and descripcion and importe:
            datos_factura[descripcion][0] += cantidad
            datos_factura[descripcion][1] += importe

    return datos_factura

def process_pdf_files(directorio_entrada, directorio_salida):
    """Process all PDF files in the directory, extract, aggregate by month, and output summaries."""
    datos_por_ano_mes = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0, 0.0])))

    for archivo_name in os.listdir(directorio_entrada):
        if archivo_name.endswith(".pdf"):
            archivo_path = os.path.join(directorio_entrada, archivo_name)
            texto_factura = extraer_texto_factura(archivo_path)
            datos_factura = extraer_datos_factura(texto_factura)
            fecha = archivo_name.split()[0]
            ano = fecha[:4]
            mes = fecha[4:6]
            nombre_mes = calendar.month_name[int(mes)]

            for descripcion, (cantidad, total) in datos_factura.items():
                datos_por_ano_mes[ano][nombre_mes][descripcion][0] += cantidad
                datos_por_ano_mes[ano][nombre_mes][descripcion][1] += total

    for ano, meses in datos_por_ano_mes.items():
        for mes, items in meses.items():
            final_data = [(desc, details[0], round(details[1], 2)) for desc, details in items.items()]
            final_data.append(("TOTAL", "", round(sum(details[1] for details in items.values()), 2)))

            tabla_mes = tabulate(final_data, headers=["Item", "Cantidad", "Total"], tablefmt="pretty")
            tabla_mes = f"\nMes: {mes} | Año: {ano}\n" + tabla_mes
            nombre_archivo = f"datos_facturas_{ano}_{mes}.txt"
            ruta_archivo = os.path.join(directorio_salida, nombre_archivo)
            with open(ruta_archivo, "w", encoding="utf-8") as archivo_salida:
                archivo_salida.write(tabla_mes)

process_pdf_files(directorio_entrada, directorio_salida)
