##################################################################################################
#BOT IMAGEN (dateset1.json)

import os
import telebot
from groq import Groq
from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN_BOT_TELEGRAM = os.getenv("TELEGRAM_TOKEN")
CLAVE_API_GROQ = os.getenv("GROQ_API_KEY")

if not TOKEN_BOT_TELEGRAM:
    raise ValueError("❌ TELEGRAM_TOKEN no está configurado en .env")
if not CLAVE_API_GROQ:
    raise ValueError("❌ GROQ_API_KEY no está configurado en .env")

bot = telebot.TeleBot(TOKEN_BOT_TELEGRAM)
cliente_groq = Groq(api_key=CLAVE_API_GROQ)

def send_welcome(mensaje):
    """Mensaje de bienvenida"""

    texto_bienvenida = """


🖼️ **¿Cómo funciono?**
Simplemente envíame una imagen y yo te daré una descripción detallada de lo que veo, ademas te dire si es reciclable o no reciclable

📸 **¡Pruébame!**
Envía cualquier imagen y verás lo que puedo hacer.

    """

#subir imagen a servidor temporal
def subir_imagen_temporal(bytes_imagen):
    """Sube una imagen a un servidor temporal (https://0x0.st) y devuelve la URL"""
    try:
        respuesta = requests.post("https://0x0.st", files={"file": ("imagen.png", bytes_imagen)})
        if respuesta.status_code == 200:
            return respuesta.text.strip()
        else:
            print(f"Error al subir imagen: {respuesta.text}")
            return None
    except Exception as e:
        print(f"Error al subir imagen temporal: {e}")
        return None

#Descripcion y clasificacion del residuo 
def describir_imagen_con_groq(url_imagen):
    """Envía una imagen por URL a Groq y obtiene descripción + reciclabilidad"""
    try:
        completado_chat = cliente_groq.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Analiza la siguiente imagen. "
                                "1️⃣ Describe brevemente qué objeto(s) contiene. "
                                "2️⃣ Indica si son reciclables o no y en qué contenedor deberían ir "
                                "(por ejemplo: papel, plástico, vidrio, orgánico, etc.). "
                                "Responde en español, de manera clara y concisa."
                            )
                        },
                        {"type": "image_url", "image_url": {"url": url_imagen}},
                    ],
                }
            ],
            model="llama-3.2-11b-vision-preview",
            temperature=0.7,
            max_tokens=500,
        )

        return completado_chat.choices[0].message.content

    except Exception as e:
        print(f"Error al describir imagen con Groq: {e}")
        return None

# Inicio

@bot.message_handler(commands=['start'])
def enviar_bienvenida(mensaje):
    texto = (
        "📸 Envíame una foto de un objeto y te diré si es reciclable o no.\n\n"
        "Usa /help para más información."
    )
    bot.reply_to(mensaje, texto)


@bot.message_handler(commands=['help'])
def enviar_ayuda(mensaje):
    texto = (
        "🧭 **Cómo usar el bot:**\n\n"
        "1️⃣ Envía una **imagen** (foto o archivo PNG/JPG).\n"
        "2️⃣ Espera unos segundos mientras la analizo.\n"
        "3️⃣ Recibirás una descripción y una indicación de si es reciclable ♻️.\n\n"
        "Comandos:\n"
        "/start - Inicia el bot\n"
        "/help - Muestra esta ayuda"
    )
    bot.reply_to(mensaje, texto, parse_mode='Markdown')


# Manejo de imágenes
def procesar_imagen(mensaje, file_id):
    try:
        info_archivo = bot.get_file(file_id)
        archivo_descargado = bot.download_file(info_archivo.file_path)
        bot.reply_to(mensaje, "📸 Imagen recibida. Analizando... ⏳")

        url_imagen = subir_imagen_temporal(archivo_descargado)
        if not url_imagen:
            bot.reply_to(mensaje, "❌ No pude subir la imagen temporalmente.")
            return

        descripcion = describir_imagen_con_groq(url_imagen)
        if descripcion:
            respuesta = f"♻️ **Análisis del objeto:**\n\n{descripcion}"
            bot.reply_to(mensaje, respuesta, parse_mode='Markdown')
        else:
            bot.reply_to(mensaje, "❌ No pude analizar la imagen.")
    except Exception as e:
        print(f"Error al procesar imagen: {e}")
        bot.reply_to(mensaje, "❌ Ocurrió un error al procesar la imagen.")

@bot.message_handler(content_types=['photo'])
def manejar_foto(mensaje):
    foto = mensaje.photo[-1]
    procesar_imagen(mensaje, foto.file_id)

@bot.message_handler(content_types=['document'])
def manejar_documento(mensaje):
    if mensaje.document.mime_type and mensaje.document.mime_type.startswith("image/"):
        procesar_imagen(mensaje, mensaje.document.file_id)
    else:
        bot.reply_to(mensaje, "❌ El archivo no parece ser una imagen.")


# Inicio del bot
if __name__ == '__main__':
    print("🤖 Bot iniciado y esperando imágenes...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error al iniciar el bot: {e}")

