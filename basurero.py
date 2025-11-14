import telebot
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
DATASET_PATH = 'dataset.json'
DATASET2_PATH = 'dataset2.json'  # Nuevo dataset de barrios


# -------------------------------
# Cargar dataset principal
# -------------------------------
def cargar_dataset():
    try:
        with open(DATASET_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


# -------------------------------
# Cargar dataset de barrios
# -------------------------------
def cargar_dataset2():
    try:
        with open(DATASET2_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


# -------------------------------
# Buscar pregunta exacta en dataset.json
# -------------------------------
def buscar_en_dataset(pregunta, dataset):
    pregunta = pregunta.strip().lower()
    for item in dataset:
        if item['pregunta'].strip().lower() == pregunta:
            return item['respuesta']
    return None


# -------------------------------
# Buscar barrio en dataset2.json
# -------------------------------
def buscar_barrio(barrio, dataset2):
    barrio = barrio.strip().lower()
    for item in dataset2:
        if item['barrio'].strip().lower() == barrio:
            return item['info']  # clave “info” en tu dataset2.json
    return None


# -------------------------------
# Respuesta IA Groq
# -------------------------------
def respuesta_groq(mensaje):
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": mensaje}
        ]
    }

    try:
        resp = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=20)

        if resp.status_code == 200:
            respuesta = resp.json()['choices'][0]['message']['content']
            return respuesta.strip()
        else:
            return f"[Error Groq {resp.status_code}]"

    except Exception as e:
        return f"[Error de conexión a Groq: {e}]"


# -------------------------------
# Inicializar bot
# -------------------------------
bot = telebot.TeleBot(TELEGRAM_TOKEN)

dataset = cargar_dataset()
dataset2 = cargar_dataset2()


# -------------------------------
# Comandos
# -------------------------------
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(
        message,
        "¡Hola! Soy un bot de gestión de residuos ♻️.\n"
        "Podés preguntarme algo o decirme tu barrio para darte información."
    )


# -------------------------------
# Handler de mensajes principales
# -------------------------------
@bot.message_handler(func=lambda message: True)
def responder(message):

    pregunta = message.text

    # 1️⃣ Buscar en dataset.json
    respuesta = buscar_en_dataset(pregunta, dataset)
    if respuesta:
        bot.reply_to(message, respuesta)
        return

    # 2️⃣ Buscar si es un barrio en dataset2.json
    respuesta_barrio = buscar_barrio(pregunta, dataset2)
    if respuesta_barrio:
        bot.reply_to(message, respuesta_barrio)
        return

    # 3️⃣ Si no está en ningún dataset → IA Groq
    respuesta_ia = respuesta_groq(pregunta)
    bot.reply_to(message, respuesta_ia)


# -------------------------------
# Ejecutar bot
# -------------------------------
if __name__ == "__main__":
    print("Bot de Telegram IA (Groq + dataset + barrios) iniciado. Esperando mensajes...")
    bot.infinity_polling()
