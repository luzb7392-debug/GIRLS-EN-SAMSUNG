import logging
from transformers import pipeline

# Ocultar warnings molestos
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)


import telebot as tlb
import os
from dotenv import load_dotenv
import logging  # asegúrate de tener este import si usas logging

# Cargar archivo .env
load_dotenv()

# Oculta mensajes innecesarios
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)


# Cargamos el modelo UNA SOLA VEZ (si no, tarda mucho)
analizador = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    revision="714eb0f"
)

# ------------------------------------------------
# FUNCIÓN: Pedir opinión al usuario
# ------------------------------------------------
def pedir_opinion(bot, message):
    bot.send_message(
        message.chat.id,
        "💬 *Queremos saber tu opinión*\n\nEscribinos un comentario sobre el servicio:",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, procesar_opinion)

# ------------------------------------------------
# FUNCIÓN: Analizar sentimiento del mensaje
# ------------------------------------------------
def procesar_opinion(message):
    texto = message.text

    if not texto:
        return bot.send_message(message.chat.id, "⚠️ Debés enviar un mensaje de texto.")

    # Analizamos el sentimiento
    resultado = analizador(texto)[0]
    puntaje = resultado["score"] * 100

    # Interpretación simple
    if puntaje >= 50 and resultado["label"] == "POSITIVE":
        respuesta = (
            "😊 *Gracias por tu reseña positiva!*\n"
            "Nos alegra saber que tu experiencia fue buena."
        )
    else:
        respuesta = (
            "😔 *Lamentamos que tu experiencia no haya sido buena.*\n"
            "Gracias por contarnos, ¡vamos a trabajar para mejorar!"
        )

    message.bot.send_message(message.chat.id, respuesta, parse_mode="Markdown")
