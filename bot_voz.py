import telebot as tlb
import os
import json
from groq import Groq
from typing import Optional
import time  
from dotenv import load_dotenv

# Cargar archivo .env
load_dotenv()

# Variables de entorno
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if not TELEGRAM_TOKEN:
    raise ValueError("No se encuentra el TOKEN de Telegram en el archivo .env")
if not GROQ_API_KEY:
    raise ValueError("No se encuentra la API key de Groq en el archivo .env")

# Instanciar objetos
bot = tlb.TeleBot(TELEGRAM_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)

# Cargar dataset
def load_company_data():
    try:
        with open('dataset1.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar el JSON: {str(e)}")
        return None

company_data = load_company_data()

# Función para obtener respuesta de Groq
def get_groq_response(user_message: str) -> Optional[str]:
    try:
        system_prompt = f"""
        Eres el asistente virtual de GIRSU. 
        Tu tarea es responder preguntas basándote ÚNICAMENTE en la siguiente información del dataset. 
        Si te preguntan algo que no está en estos datos, indica amablemente que no puedes proporcionar esa información y sugiere contactar directamente con la empresa.

Datos del plan:
{json.dumps(company_data, ensure_ascii=False, indent=2)}

Reglas:
1. Solo responde con información que esté en el dataset.
2. No inventes información.
3. Si la información no está, sugiere escribir a municipalidad@almafuerte.gov.ar, "instagram": "https://instagram.com/municipalidaddealmafuerte", "facebook": "https://facebook.com/MunicipalidadDeAlmafuerte", "youtube": "https://www.youtube.com/
4. No brindes datos sensibles del staff.
5. Sé amable y profesional.
6. No incluyas links que no estén en el dataset.
7. Usa emojis para hacerlo más amigable.
"""

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system",
                  "content": system_prompt
                },

                {"role": "user", 
                 "content": user_message
                }
            ],

            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=500
        )

        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error al obtener respuesta de Groq: {str(e)}")
        return None

# Transcripción de voz con Groq
def transcribe_voice_with_groq(message: tlb.types.Message) -> Optional[str]:
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        temp_file = "temp_voice.egg"

        with open(temp_file, "wb") as f:#guardar archivo temporalmente
            f.write(downloaded_file)

        with open(temp_file, "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=(temp_file, file.read()),
                model="whisper-large-v3-turbo",
                prompt="Transcripción en español, especifivar contexto o pronunciacion",
                response_format="json",
                language="es",
                temperature = 1
            )

        os.remove(temp_file)
        return transcription.text

    except Exception as e:
        print(f"Error al transcribir audio: {str(e)}")
        return None

# Manejo de mensajes de texto
@bot.message_handler(commands=['ia'])
def send_message(message: tlb.types.Message):
    if not company_data:
        bot.reply_to(message, "Error al cargar los datos del plan. Intente más tarde.")
        return

    bot.send_chat_action(message.chat.id, 'Escribiendo')
    response = get_groq_response(message.text)

    if response:
        bot.reply_to(message, response)
    else:
        error_message = """
        ❌ Lo siento, hubo un error al procesar tu consulta.
        Por favor, intenta nuevamente o contáctanos:
        📧 municipalidad@almafuerte.gov.ar
        Teléfono: +54 (3571) 558442
        Tucuman 777- Almafuerte - Dpto. Tercero Arriba """
        bot.reply_to(message, error_message)

# Iniciar el bot
if __name__ == "__main__":
    if company_data:
        print(f"🤖 Bot de {company_data['company_info']['name']} iniciado con Groq y Whisper...")
        while True:
            try:
                bot.polling(none_stop=True, interval=0, timeout=20)
            except Exception as e:
                print(f"Error en el bot: {str(e)}")
                print("Reiniciando...")
                time.sleep(5)
    else:
        print("Error: No se pudo cargar el archivo JSON. El bot no se iniciará.")
