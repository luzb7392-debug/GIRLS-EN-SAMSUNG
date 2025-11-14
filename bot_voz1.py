# INTERACTUAR CON GBOT (dataset1.json)
# INTERACTUAR CON GBOT (Datase1.json)
import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)


# --- CARGAR DATASET ---
def load_company_data():
    try:
        with open('dataset1.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Error cargando dataset:", e)
        return None


company_data = load_company_data()

# RESPUESTA CON GROQ
def get_groq_response(user_message: str):
    if not company_data:
        return "❌ No puedo acceder a la información en este momento."

    system_prompt = f"""
Eres el asistente virtual de GIRSU.
Responde únicamente usando el siguiente dataset.
Si la información no está incluida, responde:
"No cuento con esa información ahora mismo. Podés comunicarte con municipalidad@almafuerte.gov.ar 😊".

Dataset:
{json.dumps(company_data, ensure_ascii=False, indent=2)}
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    return response.choices[0].message.content.strip()


# --- CONVERSACIÓN ---
def send_welcome(bot, message):
    bienvenida = (
        "👋 ¡Hola! Soy *G-BOT*, tu asistente virtual del programa GIRSU Almafuerte 🌱\n\n"
        "Podés *escribirme* o enviarme un *mensaje de voz* para hacerme consultas como:\n"
        "• ¿Como puedo comunicarme con Girsu?\n"
        "• ¿Cómo separar los residuos?\n"
        "• ¿Qué puedo reciclar?\n\n"
        "🗣️ Escribí o mandá tu consulta ahora 👇"
    )
    bot.send_message(message.chat.id, bienvenida, parse_mode="Markdown")
    bot.register_next_step_handler(message, lambda m: procesar_consulta(bot, m))


# --- PROCESAR TEXTO O AUDIO ---
def procesar_consulta(bot, message):

    # 🔹 Si el usuario manda un AUDIO → convertir a texto
    if message.voice:
        try:
            file_info = bot.get_file(message.voice.file_id)
            file_data = bot.download_file(file_info.file_path)

            # Guardar archivo temporal
            with open("temp.ogg", "wb") as f:
                f.write(file_data)

            # Usar Groq Whisper
            audio_text = groq_client.audio.transcriptions.create(
                file="temp.ogg",
                model="whisper-large-v3-turbo"
            )

            consulta = audio_text.text.strip()

        except Exception as e:
            bot.send_message(message.chat.id, "❌ No pude procesar tu audio.")
            print("Error conversión audio:", e)
            return

    # 🔹 Si escribió texto
    elif message.text:
        consulta = message.text.strip()

    else:
        bot.send_message(message.chat.id, "❗ Enviame un mensaje de voz o escribí algo.")
        return

    #  Enviar acción "escribiendo"
    bot.send_chat_action(message.chat.id, "typing")

    #  Obtener respuesta IA
    respuesta = get_groq_response(consulta)

    #  Responder al usuario
    bot.send_message(message.chat.id, respuesta)

    #  Seguir conversando automáticamente
    bot.register_next_step_handler(message, lambda m: procesar_consulta(bot, m))
