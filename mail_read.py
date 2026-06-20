from email.utils import formataddr
import imaplib
import email
import smtplib
from email.header import decode_header
from mail_content import mail_content
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage

# Configuración de credenciales
EMAIL_USUARIO = "pytoncommands@gmail.com"
PASSWORD_APP = "kxtz mcri ozmm ccqi"  # Clave de 16 caracteres

# Lee y retorna los mensajes
def leer_y_eliminar_correos(eliminaCorreos):

    # Lista a retornar
    lista_correos = []

    # Conectar al servidor IMAP de Gmail mediante SSL
    print("Conectando al servidor...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    
    try:
        # Iniciar sesión
        mail.login(EMAIL_USUARIO, PASSWORD_APP)
        
        # LEER: Seleccionar la bandeja de entrada (Inbox)
        # Cambia a readonly=False para poder modificar/eliminar mensajes
        mail.select("inbox", readonly=False)
        
        # Buscar correos específicos (Ej: "UNSEEN" para no leídos, o "ALL" para todos)
        status, mensajes = mail.search(None, "ALL")
        ids_correos = mensajes[0].split()
        
        if not ids_correos:
            print("No se encontraron correos nuevos.")
            return

        print(f"Se encontraron {len(ids_correos)} correos no leídos.")

        # Procesar solo los 3 más recientes para el ejemplo
        for mail_id in ids_correos[:3]:

            # Obtener los datos del correo por su ID
            status, data = mail.fetch(mail_id, "(RFC822)")
            
            for respuesta in data:
                if isinstance(respuesta, tuple):
                    # Convertir los bytes en un objeto de mensaje de texto
                    msg = email.message_from_bytes(respuesta[1])

                    # Obtengo el Body
                    mail_body = get_email_body(msg)
                    
                    # Decodificar el asunto del correo
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")
                    
                    # Obtener el remitente
                    desde = msg.get("From")
                    
                    # print(f"\n--- Leyendo Correo ID: {mail_id.decode()} ---")
                    # print(f"\n--- Leyendo Correo Body: {mail_body} ---")
                    # print(f"De: {desde}")
                    # print(f"Asunto: {subject}")

                    # Genero el objeto
                    correo = mail_content(mail_body, subject, desde)

                    # Adiciono a la lista
                    lista_correos.append(correo)

           
            # Si debo Eliminar 
            if (eliminaCorreos == True):
                # ELIMINAR: Mover a la papelera de Gmail ([Gmail]/Trash)
                # En Gmail, "marcar como eliminado" no siempre borra el correo;
                # lo correcto para eliminarlo de verdad es moverlo a la carpeta de Papelera.
                print(f"Eliminando correo ID: {mail_id.decode()}...")

                # Copiar el correo a la papelera
                mail.copy(mail_id, '"[Gmail]/Trash"')
                # Marcar el correo original en Inbox como eliminado (Deleted) para que desaparezca
                mail.store(mail_id, "+FLAGS", "\\Deleted")
                mail.uid('COPY', mail_id, '[Gmail]/Trash')

        # Aplicar los cambios de forma permanente en el servidor (Expunge)
        mail.expunge()
        print("\nProceso completado con éxito.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        
    finally:
        # Cerrar conexión de forma segura
        try:
            mail.close()
            mail.logout()
        except:
            pass

    # return lista_correos
    return lista_correos

# Función auxiliar para extraer el cuerpo del correo
def get_email_body(msg):
    body = ""
    # Recorremos todas las partes del correo (texto, html, adjuntos)
    for part in msg.walk():
        # Omitimos partes que son contenedores (multipart)
        if part.get_content_maintype() == "multipart":
            continue

        #imprime tipos de contenido del mail
        print(part.get_content_type())

        # Buscamos partes de texto o html
        if part.get_content_type() in ["text/plain", "text/html"]:
            try:
                body = part.get_payload(decode=True).decode("utf-8")
                # Si encontramos texto plano, priorizamos; si es HTML, también sirve
                if part.get_content_type() == "text/plain":
                    return body
            except:
                pass
    return body

# Procesa los correos
def procesa_correos(lista_correos):

    if lista_correos is not None:
        print (lista_correos)
        # recorro los correos
        for correo in lista_correos:
            
            if "encender" in correo.body.lower():
                print("Found encender")
                return correo;
    
    # retorno none
    return None

# Respuesta de correo
def respuesta_correo(mail_found : mail_content):
    # Setup sender and receiver
    SENDER_EMAIL = EMAIL_USUARIO
    APP_PASSWORD = PASSWORD_APP  # Paste your 16-digit App Password here
    RECEIVER_EMAIL = mail_found.mail_from
    print (mail_found.mail_from)

    # Create the email message
    msg = EmailMessage()
    msg["Subject"] = "Encendido Recibido - Un besito a quien creo este programa"
    msg["From"] = formataddr(("Chinitos Commands", SENDER_EMAIL))

    msg["To"] = RECEIVER_EMAIL
    msg.set_content("Encendido Recibido - Un besito a quien creo este programa!!")

    try:
        # Connect to Gmail's secure SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)  # Log in
            server.send_message(msg)                  # Send mail
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")