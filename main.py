##################################################################################################
#BOT IMAGEN
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


##################################################################################################
#BOT IMAGEN

import os
import base64
import telebot
from groq import Groq
from dotenv import load_dotenv
from PIL import Image
import io
import requests

load_dotenv()

# Configuración
TOKEN_BOT_TELEGRAM = os.getenv('TELEGRAM_BOT_TOKEN')
CLAVE_API_GROQ = os.getenv('GROQ_API_KEY')

if not TOKEN_BOT_TELEGRAM:
    raise ValueError("TELEGRAM_BOT_TOKEN no está configurado")
if not CLAVE_API_GROQ:
    raise ValueError("GROQ_API_KEY no está configurado")

# Inicialización
bot = telebot.TeleBot(TOKEN_BOT_TELEGRAM)
cliente_groq = Groq(api_key=CLAVE_API_GROQ)

# Convierte imagen a base64
def imagen_a_base64(ruta_o_bytes_imagen):
    """Convierte una imagen a base64"""
    try:
        if isinstance(ruta_o_bytes_imagen, bytes):
            return base64.b64encode(ruta_o_bytes_imagen).decode('utf-8')
        else:
            with open(ruta_o_bytes_imagen, "rb") as archivo_imagen:
                return base64.b64encode(archivo_imagen.read()).decode('utf-8')
    except Exception as e:
        print(f"Error al convertir imagen a base64: {e}")
        return None

# Envía imagen a Groq para describirla
def describir_imagen_con_groq(imagen_base64):
    """Envía la imagen a Groq y obtiene la descripción"""
    try:
        completado_chat = cliente_groq.chat.completions.create(
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": "Por favor, describe esta imagen de manera detallada en español."},
                    {"type": "image_url",
                     "image_url": {"url": f"data:image/jpeg;base64,{imagen_base64}"}}
                ]
            }],
            model="llama-3.2-11b-vision-preview",
            temperature=0.7,
            max_tokens=1000
        )
        return completado_chat.choices[0].message.content
    except Exception as e:
        print(f"Error al describir imagen con Groq: {e}")
        return None

# /start
@bot.message_handler(commands=['start'])
def enviar_bienvenida(mensaje):
    """Mensaje de bienvenida"""
    texto_bienvenida = """
¡Hola! 👋 Soy un bot que describe imágenes.

📸 Envíame una imagen y te daré una descripción detallada.
🤖 Uso Groq AI para analizar las imágenes.
Usa /help para más información.
"""
    bot.reply_to(mensaje, texto_bienvenida)

# /help
@bot.message_handler(commands=['help'])
def enviar_ayuda(mensaje):
    """Mensaje de ayuda"""
    texto_ayuda = """
🔧 **Comandos:**
/start - Inicia el bot
/help - Muestra esta ayuda

📸 Envía una imagen y recibirás una descripción detallada.
"""
    bot.reply_to(mensaje, texto_ayuda)

# Manejo de imágenes
@bot.message_handler(content_types=['photo'])
def manejar_foto(mensaje):
    """Procesa imágenes enviadas"""
    try:
        bot.reply_to(mensaje, "📸 Imagen recibida. Analizando... ⏳")
        foto = mensaje.photo[-1]
        info_archivo = bot.get_file(foto.file_id)
        archivo_descargado = bot.download_file(info_archivo.file_path)
        imagen_base64 = imagen_a_base64(archivo_descargado)

        if not imagen_base64:
            bot.reply_to(mensaje, "❌ Error al procesar la imagen.")
            return

        descripcion = describir_imagen_con_groq(imagen_base64)
        if descripcion:
            respuesta = f"🤖 **Descripción:**\n\n{descripcion}"
            bot.reply_to(mensaje, respuesta, parse_mode='Markdown')
        else:
            bot.reply_to(mensaje, "❌ No pude analizar la imagen.")
    except Exception as e:
        print(f"Error al procesar imagen: {e}")
        bot.reply_to(mensaje, "❌ Error al procesar la imagen.")

# Otros mensajes
@bot.message_handler(func=lambda mensaje: True)
def manejar_otros_mensajes(mensaje):
    """Maneja mensajes que no son imágenes"""
    bot.reply_to(mensaje, """
📝 Solo puedo procesar imágenes por ahora.
📸 Envía una imagen o usa /help.
""")

if __name__ == '__main__':
    print("🤖 Bot iniciado...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error al iniciar el bot: {e}")
