import re
import smtplib
import ssl
from email.mime.text import MIMEText
from datetime import datetime

import streamlit as st

st.set_page_config(page_title="Soporte Técnico en la Nube - Henry Monge", page_icon="🛠️", layout="centered")

TIPOS_PROBLEMA = ["Hardware", "Software", "Red / Conectividad", "Cuenta de usuario / Acceso", "Otro"]
PRIORIDADES = ["Baja", "Media", "Alta", "Crítica"]
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


def enviar_correo(nombre, correo_usuario, tipo_problema, prioridad, descripcion):
    remitente = st.secrets["email"]["EMAIL_ADDRESS"]
    password = st.secrets["email"]["EMAIL_PASSWORD"]
    destinatario = st.secrets["email"]["ADMIN_EMAIL"]
    smtp_server = st.secrets["email"].get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(st.secrets["email"].get("SMTP_PORT", 465))

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cuerpo = f"""Nuevo reporte de soporte técnico

Fecha: {fecha}
Nombre del usuario: {nombre}
Correo del usuario: {correo_usuario}
Tipo de problema: {tipo_problema}
Prioridad: {prioridad}

Descripción del problema:
{descripcion}
"""
    mensaje = MIMEText(cuerpo, "plain", "utf-8")
    mensaje["Subject"] = f"[Soporte Técnico] {tipo_problema} - Prioridad {prioridad}"
    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Reply-To"] = correo_usuario

    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=contexto) as servidor:
        servidor.login(remitente, password)
        servidor.sendmail(remitente, [destinatario], mensaje.as_string())


st.title("🛠️ Servicio de Soporte Técnico en la Nube")
st.caption("Reporta un problema y la aplicación enviará automáticamente un correo al administrador.")
st.divider()

with st.form("form_reporte", clear_on_submit=False):
    st.subheader("Formulario de reporte")

    nombre = st.text_input("Nombre del usuario *")
    correo_usuario = st.text_input("Correo electrónico *")
    tipo_problema = st.selectbox("Tipo de problema *", ["-- Seleccione --"] + TIPOS_PROBLEMA)
    prioridad = st.selectbox("Nivel de prioridad *", PRIORIDADES)
    descripcion = st.text_area("Descripción detallada del problema *", height=150)

    enviado = st.form_submit_button("Enviar reporte", use_container_width=True)

if enviado:
    errores = []

    if not nombre.strip():
        errores.append("El nombre del usuario es obligatorio.")
    if not correo_usuario.strip():
        errores.append("El correo electrónico es obligatorio.")
    elif not re.match(EMAIL_REGEX, correo_usuario.strip()):
        errores.append("El correo electrónico no tiene un formato válido.")
    if tipo_problema == "-- Seleccione --":
        errores.append("Debe seleccionar un tipo de problema.")
    if not descripcion.strip():
        errores.append("La descripción del problema es obligatoria.")

    if errores:
        st.error("Se encontraron los siguientes errores:")
        for e in errores:
            st.markdown(f"- {e}")
    else:
        try:
            with st.spinner("Enviando reporte al administrador..."):
                enviar_correo(nombre.strip(), correo_usuario.strip(), tipo_problema, prioridad, descripcion.strip())
            st.success("¡Reporte enviado correctamente! Su reporte ha sido enviado al administrador.")
        except Exception as e:
            st.error("No se pudo enviar el correo. Intente nuevamente más tarde.")
            st.exception(e)

st.divider()
st.caption("Esta aplicación no almacena los reportes en ninguna base de datos, archivo o sistema. La información solo se utiliza para enviar el correo.")
