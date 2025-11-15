#Informacion sobre girsu (dataset.json)
import telebot
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'

DATASET_PATH = 'dataset.json'  # Ruta al archivo JSON que contiene el dataset de preguntas y respuestas


# CARGAR DATASET
def cargar_dataset():
    try:
        with open(DATASET_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)

            # Asegurarse de que siempre devuelva una lista de diccionarios válidos
            resultado = []

            if isinstance(data, dict) and "preguntas" in data:
                data = data["preguntas"]

            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "pregunta" in item and "respuesta" in item:
                        resultado.append(item)

            return resultado

    except Exception as e:
        print(f"Error al cargar dataset: {e}")
        return []



# BUSCAR EN EL DATASET
def buscar_en_dataset(pregunta, dataset):
    pregunta = pregunta.strip().lower()

    for item in dataset:
        try:
            if item["pregunta"].strip().lower() == pregunta:
                return item["respuesta"]
        except:
            # Si el item NO es un dict válido, lo ignora
            continue

    return None


# CONSULTA A GROQ
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
            return resp.json()['choices'][0]['message']['content'].strip()
        else:
            return f"[Error Groq {resp.status_code}]"

    except Exception as e:
        return f"[Error de conexión a Groq: {e}]"


# BOT TELEGRAM
bot = telebot.TeleBot(TELEGRAM_TOKEN)
dataset = cargar_dataset()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_chat_action(message.chat.id, "escribiendo")
    bot.reply_to(message, "¡Hola! Soy un bot IA. Pregúntame algo y responderé usando IA o mi base de datos.")


@bot.message_handler(func=lambda message: True)
def responder(message):
    pregunta = message.text

    # Intentar dataset
    respuesta = buscar_en_dataset(pregunta, dataset)

    if respuesta:
        bot.reply_to(message, respuesta)
        return

    # Si no existe, usar IA
    respuesta_ia = respuesta_groq(pregunta)
    bot.reply_to(message, respuesta_ia)

