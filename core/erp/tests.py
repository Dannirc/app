import smtplib
from email.mime.text import MIMEText

from config import settings


def send_mail():
    try:
        # Establecemos conexion con el servidor smtp de gmail
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, 587)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print('Conectado!')

        # Construimos el mensaje simple
        mensaje = MIMEText("""Este es el mensaje de las narices""")
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = settings.EMAIL_HOST_USER
        mensaje['Subject'] = "Tienes un correo desde django"

        # Envio del mensaje
        mailServer.sendmail(settings.EMAIL_HOST_USER,
                            settings.EMAIL_HOST_USER,
                            mensaje.as_string())

        print('Correo enviado correctamente =)')

    except Exception as e:
        print(e)


send_mail()

