import os
from PyPDF2 import PdfReader

# Función para convertir un archivo PDF a un archivo de texto
def pdf_to_text(pdf_path, txt_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        text = ''
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

# Directorio de entrada y salida
input_directory = '/Users/user/Dropbox/Mac/Desktop/Projects/Python/pythonProject1/ScriptPythonMercadona/Descargas Mails'
output_directory = '/Users/user/Dropbox/Mac/Desktop/Projects/Python/pythonProject1/ScriptPythonMercadona/PDF to TXT'

# Asegúrate de que el directorio de salida exista
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Iterar sobre todos los archivos en el directorio de entrada
for filename in os.listdir(input_directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(input_directory, filename)
        txt_path = os.path.join(output_directory, filename.replace('.pdf', '.txt'))
        pdf_to_text(pdf_path, txt_path)
