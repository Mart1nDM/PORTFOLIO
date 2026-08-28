from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
# Habilitamos CORS para que tu portfolio pueda comunicarse con esta API
CORS(app) 

@app.route('/enviar-correo', methods=['POST'])
def enviar_correo():
    try:
        # Recibimos los datos del formulario (en formato JSON)
        datos = request.json
        nombre = datos.get('nombre')
        email_usuario = datos.get('email')
        mensaje_usuario = datos.get('mensaje')

        # Configuración de tu correo (te enseñaré a crear una contraseña de aplicación)
        # Usamos variables de entorno por seguridad, para no subir tu clave a GitHub
        mi_correo = os.environ.get('MI_CORREO', 'tu_correo@gmail.com') 
        mi_password = os.environ.get('MI_PASSWORD', 'tu_contraseña_de_aplicacion_aqui')

        # Armamos el correo que te va a llegar a ti
        msg = MIMEMultipart()
        msg['From'] = mi_correo
        msg['To'] = mi_correo
        msg['Subject'] = f"Portfolio: Nuevo mensaje de {nombre}"

        cuerpo = f"Has recibido un nuevo mensaje desde tu Portfolio.\n\n" \
                 f"Nombre: {nombre}\n" \
                 f"Email de contacto: {email_usuario}\n\n" \
                 f"Mensaje:\n{mensaje_usuario}"
                 
        msg.attach(MIMEText(cuerpo, 'plain'))

        # Nos conectamos a los servidores de Gmail para enviar el correo
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(mi_correo, mi_password)
        server.send_message(msg)
        server.quit()

        return jsonify({"mensaje": "¡Correo enviado con éxito!"}), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Hubo un problema al enviar el correo."}), 500

if __name__ == '__main__':
    app.run(debug=True)