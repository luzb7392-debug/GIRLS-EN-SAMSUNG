import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)


# Cargar dataset
def load_company_data():
    try:
        with open('dataset1.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Error cargando dataset:", e)
        return None

company_data = load_company_data()

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


# FUNCIÓN PRINCIPAL QUE SE LLAMA DESDE EL MENÚ
def responder(message):
    bot = message._bot
    bot.send_message(message.chat.id, "🏡 Escribí tu *dirección* o *barrio* para decirte cuándo pasa el basurero 😊")
    bot.register_next_step_handler(message, procesar_consulta)


def procesar_consulta(message):
    bot = message._bot
    consulta = message.text.strip()
    bot.send_chat_action(message.chat.id, "escribiendo...")
    respuesta = get_groq_response(consulta)
    bot.send_message(message.chat.id, respuesta)

    bot.send_message(message.chat.id, "🌱 ¡Gracias por usar G-BOT! Escribí /start para volver al menú principal.")
