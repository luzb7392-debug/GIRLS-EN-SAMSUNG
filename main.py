import telebot
from telebot import types
import os
import bot_voz1 as bot_voz         # Interactuar con G-BOT
import imagen           # Saber si un objeto es reciclable o no
import ia               # Saber información sobre G-BOT / cuándo pasa el basurero
import salir            # Opción de salir
from sentiment_analysis import analizar_sentimiento  # Dejanos tu opinión
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- MENÚ PRINCIPAL ---
@bot.message_handler(commands=['start'])
def menu_principal(message):
    markup = types.InlineKeyboardMarkup(row_width=1)

    markup.add(types.InlineKeyboardButton("🤖 Interactuar con G-BOT", callback_data="interactuar"))
    markup.add(types.InlineKeyboardButton("🚛 Saber cuándo pasa el basurero por mi casa", callback_data="basurero"))
    markup.add(types.InlineKeyboardButton("♻️ Saber si un objeto es reciclable", callback_data="reciclable"))
    markup.add(types.InlineKeyboardButton("ℹ️ Información sobre GIRSU", callback_data="info"))
    markup.add(types.InlineKeyboardButton("💬 Dejanos tu opinión", callback_data="opinion"))
    markup.add(types.InlineKeyboardButton("🚪 Salir", callback_data="salir"))

    mensaje = (
        "🌱 *¡Bienvenido a G-BOT!*\n\n"
      "Soy tu asistente virtual para ayudarte con la *separación de residuos*, "
        "informarte sobre los *días de recolección* y acompañarte en el cuidado del ambiente. 🌍\n\n"
        
        "Elegí una opción del menú 👇"
    )

    bot.send_message(message.chat.id, mensaje, parse_mode="Markdown", reply_markup=markup)


# RESPUESTAS A LOS BOTONES 
@bot.callback_query_handler(func=lambda call: True)
def menu_callback(call):
    if call.data == "interactuar":
        bot_voz.send_welcome(bot, call.message)

    elif call.data == "basurero":
        bot.send_message(call.message.chat.id, "🏘️ Decime el *nombre de tu barrio*:", parse_mode="Markdown")

    elif call.data == "reciclable":
        bot.send_message(call.message.chat.id, "📸 Enviá una imagen y te digo si es reciclable ✅")

    elif call.data == "info":
        ia.responder(call.message)

    elif call.data == "opinion":
        analizar_sentimiento(bot, call.message)

    elif call.data == "salir":
        salir.salir(bot, call.message)


# Si el usuario escribe texto (para barrios y otros casos) 
@bot.message_handler(func=lambda message: True)
def manejar_texto(message):
    texto = message.text.lower()

    # Acá seguís manejando tus barrios o lógica antigua, si corresponde
    bot.send_message(message.chat.id, "❓ No reconozco esa opción. Usá /start para ver el menú.")


if __name__ == "__main__":
    print("🚀 G-BOT principal iniciado correctamente.")
    bot.infinity_polling()
