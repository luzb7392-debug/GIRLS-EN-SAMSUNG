# Interactuar con g-bot (dataset1.json)

import json
import os
from groq import Groq
from dotenv import load_dotenv
import telebot

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

# Historial por usuario para conversación
conversaciones = {}


#  CARGAR DATASET 
def load_company_data():
    try:
        with open('dataset1.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("❌ Error cargando dataset:", e)
        return None

company_data = load_company_data()


#  IA CON GROQ + HISTORIAL
def get_groq_response(user_id: int, user_message: str):

    if not company_data:
        return "❌ No puedo acceder a la información en este momento."

    # Crear historial si no existe
    if user_id not in conversaciones:
        conversaciones[user_id] = []

    system_prompt = f"""
Eres el asistente virtual de GIRSU.
Responde únicamente usando el siguiente dataset.
Si la información no está incluida, responde:
"No cuento con esa información ahora mismo. Podés comunicarte con municipalidad@almafuerte.gov.ar 😊 o ☎️ Municipalidad de Almafuerte: +54 (3571) 558442".

Dataset:
{json.dumps(company_data, ensure_ascii=False)}
"""

    # Preparar mensajes para Groq
    mensajes = [{"role": "system", "content": system_prompt}]
    mensajes.extend(conversaciones[user_id])  # historial real
    mensajes.append({"role": "user", "content": user_message})

    # Llamada al modelo
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=mensajes,
        temperature=0.2
    )

    respuesta = response.choices[0].message.content.strip()

    # Guardar intercambio en historial
    conversaciones[user_id].append({"role": "user", "content": user_message})
    conversaciones[user_id].append({"role": "assistant", "content": respuesta})

    return respuesta


#  MENSAJE DE BIENVENIDA
def send_welcome(bot, message):

    user_id = message.chat.id

    # Reiniciar historial de conversación para este usuario
    conversaciones[user_id] = []

    bienvenida = (
        "👋 ¡Hola! Soy *G-BOT*, tu asistente virtual de GIRSU Almafuerte 🌱\n\n"
        "Podés *escribirme* o enviarme un *mensaje de voz* para consultar sobre:\n"
        "• ¿Como puedo comunicarme con Girsu?\n" 
        "• ¿Cómo separar los residuos?\n" 
        "• ¿Qué puedo reciclar?\n\n"
        "• Información del programa GIRSU\n\n"
        " 👇Decime tu consulta!! "
    )
    bot.send_message(user_id, bienvenida, parse_mode="Markdown")

    # Activar conversación
    bot.register_next_step_handler(message, lambda m: procesar_consulta(bot, m))

#  PROCESAR TEXTO O AUDIO
def procesar_consulta(bot, message):

    user_id = message.chat.id

   
    # SI ES AUDIO → Transcribir
    if message.voice:
        try:
            file_info = bot.get_file(message.voice.file_id)
            file_data = bot.download_file(file_info.file_path)

            # Guardar archivo temporal
            with open("temp.ogg", "wb") as f:
                f.write(file_data)

            # Transcribir audio – archivo cerrado automáticamente
            try:
                with open("temp.ogg", "rb") as audio_file:
                    audio = groq_client.audio.transcriptions.create(
                        file=audio_file,
                        model="whisper-large-v3-turbo"
                    )
            finally:
                # borrar archivo temp sin dejarlo bloqueado
                if os.path.exists("temp.ogg"):
                    try:
                        os.remove("temp.ogg")
                    except Exception as e:
                        print("⚠ No pude borrar temp.ogg:", e)

            consulta = audio.text.strip()

        except Exception as e:
            print("Error procesando audio:", e)
            bot.send_message(user_id, "❌ No pude procesar tu mensaje de voz.")
            return

    
    # SI ES TEXTO NORMAL
    elif message.text:
        consulta = message.text.strip()

    else:
        bot.send_message(user_id, "❗ Enviame un mensaje de voz o escribí algo.")
        return

    # Mostrar escribiendo…
    bot.send_chat_action(user_id, "typing")

    # Obtener respuesta IA con historial
    respuesta = get_groq_response(user_id, consulta)

    # Enviar respuesta
    bot.send_message(user_id, respuesta)

    # Mantener la conversación activa
    bot.register_next_step_handler(message, lambda m: procesar_consulta(bot, m))
