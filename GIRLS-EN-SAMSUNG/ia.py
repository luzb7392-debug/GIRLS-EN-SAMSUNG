##################################################################################################
# Bot de Telegram que responde usando la IA de Groq y un dataset local en JSON
import telebot
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
DATASET_PATH = 'dataset.json' # Ruta al archivo JSON que contiene el dataset de preguntas y respuestas

# Función para cargar el dataset desde el archivo JSON
def cargar_dataset():
	try:
		# Abre el archivo dataset.json en modo lectura y codificación utf-8
		with open(DATASET_PATH, 'r', encoding='utf-8') as f:
			# Carga y retorna el contenido como una lista de diccionarios, abre, lee, codifica (utf-8), da un alias, retorna el archivo cargado
			return json.load(f)
	except Exception:
		# Si hay error (por ejemplo, el archivo no existe), retorna una lista vacía
		return []

#Busca una pregunta exacta en el dataset y retorna la respuesta si la encuenta
def buscar_en_dataset(pregunta, dataset):
	#Normaliza la pregunta(quita espacios y pasa a minusculas)
	pregunta = pregunta.strip().lower()
	#Recorre cada elemento del dataset 
	for item in dataset:
		#Compara la pregunta del usuario con la del dataset (normalizada)
		if item['pregunta'].strip().lower() == pregunta:
			#Si hay coincidencia exacta, retorna la respuesta 
			return item['respuesta']
	#Si no encuentra coicidencia
	return None


# Busca una pregunta exacta en el dataset y retorna la respuesta si la encuentra
def buscar_en_dataset(pregunta, dataset):
	# Normaliza la pregunta (quita espacios y pasa a minúsculas)
	pregunta = pregunta.strip().lower()
	# Recorre cada elemento del dataset
	for item in dataset:
		# Compara la pregunta del usuario con la del dataset (normalizada)
		if item['pregunta'].strip().lower() == pregunta:
			# Si hay coincidencia exacta, retorna la respuesta
			return item['respuesta']
	# Si no encuentra coincidencia, retorna None
	return None


# Consulta la API de Groq para obtener una respuesta generada por IA
def respuesta_groq(mensaje):
	# Define los headers de la petición HTTP, incluyendo la API key
	headers = {
		'Authorization': f'Bearer {GROQ_API_KEY}',
		'Content-Type': 'application/json'
	}
	# Define el cuerpo de la petición, con el modelo y el mensaje del usuario
	data = {
		"model": "llama-3.1-8b-instant",
		"messages": [
			{"role": "user", "content": mensaje}
		]
	}
      
	try:
		resp = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=20)
            
		#respuesta es exitosa (código 200)
		if resp.status_code == 200: 
			# Extrae el contenido generado por la IA
			respuesta = resp.json()['choices'][0]['message']['content'] #formato texto
			return respuesta.strip()
		else:
			# Si hay error, retorna el código de error
			return f"[Error Groq {resp.status_code}]"
	except Exception as e:
		# Si ocurre una excepción (por ejemplo, timeout), retorna el error
		return f"[Error de conexión a Groq: {e}]"
	
# Crea una instancia del bot de Telegram usando el token
bot = telebot.TeleBot(TELEGRAM_TOKEN)
# Carga el dataset al iniciar el bot
dataset = cargar_dataset()


# Handler para los comandos /start y /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	# Responde con un mensaje de bienvenida
	bot.send_chat_action(message.chat.id, "escribiendo")
	bot.reply_to(message, "¡Hola! Soy un bot IA. Pregúntame algo y responderé usando IA o mi base de datos.")

# Handler para cualquier otro mensaje de texto
@bot.message_handler(func=lambda message: True)
def responder(message):
	# Obtiene el texto del mensaje recibido
	pregunta = message.text
	# Busca la respuesta en el dataset
	respuesta = buscar_en_dataset(pregunta, dataset)
	if respuesta:
		# Si la encuentra, responde con la respuesta del dataset
        
		bot.reply_to(message, respuesta)
	else:
		# Si no la encuentra, consulta la IA de Groq y responde con la respuesta generada
		respuesta_ia = respuesta_groq(pregunta)
		bot.reply_to(message, respuesta_ia)

# Punto de entrada principal del script
if __name__ == "__main__":
	# Imprime un mensaje en consola indicando que el bot está iniciado
	print("Bot de Telegram IA (Groq + dataset) iniciado. Esperando mensajes...")
	# Inicia el polling infinito para recibir mensajes de Telegram, esta constantemente a la espera que alguien use el bot
	bot.infinity_polling()

