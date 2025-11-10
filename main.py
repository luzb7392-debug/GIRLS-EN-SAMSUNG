import telebot
from telebot import types
import bot_voz          # Interactuar con G-BOT
import imagen            # Saber si un objeto es reciclable o no 
import ia                # Saber información sobre G-BOT / cuándo pasa el basurero
import salir             # Opción de salir
from sentiment_analysis import analizar_sentimiento # Dejanos tu opinión 
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

bot = telebot.TeleBot(TOKEN)

# --- MENÚ PRINCIPAL ---
@bot.message_handler(commands=['start'])
def menu_principal(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    opcion1 = types.KeyboardButton("🤖 Interactuar con G-BOT")
    opcion2 = types.KeyboardButton("💬 Dejanos tu opinión")  # Comentado por ahora
    opcion3 = types.KeyboardButton("🚛 Saber cuándo pasa el basurero por mi casa")
    opcion4 = types.KeyboardButton("♻️ Saber si un objeto es reciclable")
    opcion5 = types.KeyboardButton("ℹ️ Saber información sobre G-BOT")
    opcion6 = types.KeyboardButton("🚪 Salir")

    # markup.add(opcion1, opcion2, opcion3, opcion4, opcion5, opcion6)
    markup.add(opcion1, opcion3, opcion4, opcion5, opcion6)  # Sin opinión

    bot.send_message(
        message.chat.id,
        "🌱 ¡Bienvenido a G-BOT! Seleccioná una opción del menú 👇",
        reply_markup=markup
    )

# --- RESPUESTAS SEGÚN OPCIÓN ---
@bot.message_handler(func=lambda message: True)
def responder_opciones(message):
    texto = message.text

    if texto == "🤖 Interactuar con G-BOT":
        bot_voz.send_welcome(message)

    elif texto == "💬 Dejar tu opinión":
        sentiment_analysis.analizar_sentimiento(bot, message)  # llama al análisis de sentimientos

    elif texto == "🚛 Saber cuándo pasa el basurero por mi casa":
        ia.responder(message)

    elif texto == "♻️ Saber si un objeto es reciclable":
        bot.send_message(message.chat.id, "📸 Enviá una imagen para analizar si el objeto es reciclable.")
        # El análisis se hace dentro del módulo imagen.py

    elif texto == "ℹ️ Saber información sobre G-BOT":
        ia.responder(message)

    elif texto == "🚪 Salir":
        salir.salir(bot, message)

    else:
        bot.send_message(message.chat.id, "❓ No reconozco esa opción. Escribí /start para ver el menú de nuevo.")

if __name__ == "__main__":
    print("🚀 G-BOT principal iniciado correctamente.")
    bot.infinity_polling()

