# Servicio de Soporte Técnico en la Nube

## Integrante
Henry Monge

## Objetivo
Aplicación web que permite reportar incidencias de soporte técnico mediante un formulario. Valida la información ingresada y, si es correcta, envía automáticamente un correo electrónico al administrador con los datos del reporte. No utiliza base de datos ni almacenamiento persistente.

## Funcionamiento
1. El usuario abre la aplicación en el navegador.
2. Completa el formulario: nombre, correo, tipo de problema, prioridad y descripción.
3. Al presionar "Enviar reporte", la aplicación valida:
   - Campos obligatorios completos.
   - Formato válido de correo (regex).
   - Tipo de problema seleccionado.
   - Descripción no vacía.
4. Si hay errores, se muestran en pantalla y no se envía correo.
5. Si todo es válido, se envía un correo vía SMTP (Gmail) al administrador con los datos del reporte.
6. Se muestra el mensaje de confirmación: "¡Reporte enviado correctamente! Su reporte ha sido enviado al administrador."

## Tecnologías utilizadas
- Python 3
- Streamlit (interfaz web)
- smtplib / email (librerías estándar de Python para envío de correo)
- Gmail SMTP como servicio de correo saliente

## Envío de correo: decisión técnica
Se usa **Gmail SMTP con Contraseña de Aplicación** (App Password), no la contraseña normal de la cuenta:
- Es gratuito, no requiere backend adicional ni servicios de terceros.
- Requiere verificación en dos pasos activada en la cuenta de Google.
- La contraseña de aplicación es un token de 16 caracteres exclusivo para esta app, revocable en cualquier momento desde la cuenta de Google, y distinto de la contraseña real.
- Alternativas evaluadas: servicios de relay como SendGrid o Mailgun (planes gratuitos limitados y requieren verificación de dominio), o `smtplib` con otro proveedor (Outlook/Office365). Para un proyecto académico individual, Gmail SMTP + App Password es la opción más simple, gratuita y suficientemente segura.

## Manejo seguro de credenciales
- Las credenciales (correo, contraseña de aplicación, correo del administrador) se almacenan **únicamente** en `st.secrets`, mediante el archivo `.streamlit/secrets.toml`.
- Ese archivo **no se sube al repositorio** (está en `.gitignore`).
- En Streamlit Community Cloud, las credenciales se configuran en el panel de la app: **Settings → Secrets**, y se inyectan en tiempo de ejecución.
- El código fuente (`app.py`) nunca contiene contraseñas, tokens ni claves; solo referencia `st.secrets["email"][...]`.
- Se incluye `secrets.toml.example` como plantilla, sin credenciales reales, solo para referencia de formato.

## Cómo obtener la contraseña de aplicación de Gmail
1. Activar verificación en dos pasos en la cuenta de Google.
2. Ir a https://myaccount.google.com/apppasswords
3. Crear una nueva contraseña de aplicación (nombre: "Soporte Tecnico Streamlit").
4. Copiar el código de 16 caracteres generado y usarlo como `EMAIL_PASSWORD` en los secrets (nunca la contraseña real de la cuenta).

## Procedimiento de ejecución local
```bash
pip install -r requirements.txt
mkdir .streamlit
# copiar secrets.toml.example a .streamlit/secrets.toml y completar con datos reales
streamlit run app.py
```

## Despliegue en Streamlit Community Cloud
1. Subir el repositorio a GitHub (sin el archivo `secrets.toml`).
2. Entrar a https://streamlit.io/cloud y crear una nueva app apuntando al repositorio y a `app.py`.
3. En **Settings → Secrets** de la app, pegar el contenido equivalente a `secrets.toml.example` con los valores reales.
4. Desplegar y probar el enlace generado desde otro dispositivo/navegador.

## Restricciones cumplidas
- No se usa base de datos.
- No se almacenan reportes en archivos, hojas de cálculo ni ningún sistema; los datos solo viven en memoria durante el envío del correo.
- Ninguna credencial está escrita en el código fuente ni se sube al repositorio.
