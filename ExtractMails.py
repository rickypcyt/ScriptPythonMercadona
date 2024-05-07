import imaplib
import email
import os

# Configuración de conexión IMAP para Gmail
IMAP_SERVER = 'imap.gmail.com'
EMAIL = 'rickypcyt@gmail.com'
REMITENTE = 'ticket_digital@mail.mercadona.com'

# Función para decodificar los encabezados del correo electrónico
def decode_subject_header(header):
    decoded_parts = email.header.decode_header(header)
    subject = ''
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            subject += part.decode(encoding or 'utf-8')
        else:
            subject += part
    return subject

# Conexión al servidor IMAP de Gmail
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)

# Seleccionar la bandeja de entrada (inbox)
mail.select('inbox')

# Definir el filtro para los correos electrónicos con PDF adjuntos y del remitente específico
filtro = f'(SUBJECT "Mercadona") FROM "{REMITENTE}"'  # Ajusta el filtro según tus necesidades

# Buscar correos electrónicos que coincidan con el filtro
result, data = mail.search(None, filtro)

# Iterar sobre los IDs de los correos electrónicos encontrados
for num in data[0].split():
    # Obtener el correo electrónico completo
    result, data = mail.fetch(num, '(RFC822)')
    raw_email = data[0][1]
    
    # Convertir el correo electrónico a un objeto Email
    msg = email.message_from_bytes(raw_email)
    
    # Iterar sobre los archivos adjuntos
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        
        # Descargar archivos adjuntos (solo PDF)
        if part.get_content_type() == 'application/pdf':
            filename = part.get_filename()
            if filename:
                filepath = os.path.join(
                    '/Users/user/Dropbox/Mac/Desktop/Projects/Python/pythonProject1/ScriptPythonMercadona/Descargas PDF Mails',
                    filename)

                # Ensure the directory exists
                directory = os.path.dirname(filepath)
                if not os.path.exists(directory):
                    os.makedirs(directory)

                # Open the file safely
                with open(filepath, 'wb') as fp:
                    fp.write(part.get_payload(decode=True))

            # Cerrar la conexión
            mail.logout()
