from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# -------------------------
# ENVOI EMAIL (optionnel)
# -------------------------
def send_email(mail_content):
    sender_email = "TON_EMAIL@gmail.com"
    sender_password = "MOT_DE_PASSE_APP"

    msg = MIMEText(mail_content, "plain", "utf-8")
    msg["Subject"] = "Mail administratif généré"
    msg["From"] = sender_email
    msg["To"] = sender_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()


# -------------------------
# PAGE ACCUEIL
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# GENERATION DU MAIL (SANS IA)
# -------------------------
@app.route("/generate", methods=["POST"])
def generate():
    service = request.form["service"]
    name = request.form["name"]
    message = request.form["message"]
    nie = request.form.get("nie", "")
    address = request.form.get("address", "")

    # 🔥 TEMPLATE INTELLIGENT (sans OpenAI)
    if service == "catastro":
        mail = f"""Estimados señores del Catastro,

Me dirijo a ustedes para solicitar información relativa a mi inmueble.

Dirección:
{address}

Número de NIE:
{nie}

Solicitud:
{message}

Datos del solicitante:
Nombre: {name}

Atentamente,
{name}
"""

    elif service == "avocat":
        mail = f"""Estimado abogado,

Solicito asesoramiento jurídico sobre la siguiente situación:

{message}

Datos:
Nombre: {name}

Atentamente,
{name}
"""

    elif service == "banque":
        mail = f"""Estimados señores del banco,

Me dirijo a ustedes para solicitar información sobre mi cuenta.

Solicitud:
{message}

Nombre: {name}

Atentamente,
{name}
"""

    else:
        mail = f"""Estimados señores,

{message}

Nombre: {name}

Atentamente,
{name}
"""

    return render_template("result.html", mail=mail)


# -------------------------
# ENVOI EMAIL (OPTIONNEL)
# -------------------------
@app.route("/send", methods=["POST"])
def send():
    mail = request.form["mail"]
    send_email(mail)
    return "<h2>✅ Email envoyé</h2><a href='/'>Retour</a>"


# -------------------------
# RUN LOCAL
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
