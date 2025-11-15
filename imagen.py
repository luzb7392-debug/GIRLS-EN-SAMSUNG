##################################################################################################
#Saber si un objeto es reciclable

import os
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

CLAVE_API_GROQ = os.getenv("GROQ_API_KEY")

if not CLAVE_API_GROQ:
    raise ValueError("❌ GROQ_API_KEY no está configurado en .env")

cliente_groq = Groq(api_key=CLAVE_API_GROQ)


# ------------------------------
# SUBIR IMAGEN A SERVIDOR TEMPORAL
# ------------------------------
def subir_imagen_temporal(ruta_imagen):
    """Sube una imagen a 0x0.st y devuelve la URL accesible."""
    try:
        with open(ruta_imagen, "rb") as f:
            respuesta = requests.post("https://0x0.st", files={"file": f})

        if respuesta.status_code == 200:
            return respuesta.text.strip()
        else:
            print("Error al subir imagen:", respuesta.text)
            return None

    except Exception as e:
        print("Error al subir imagen temporal:", e)
        return None


# ------------------------------
# ANALIZAR IMAGEN CON GROQ
# ------------------------------
def describir_imagen_con_groq(url_imagen):
    """Envía la URL de la imagen a Groq Vision y obtiene análisis."""
    try:
        completado = cliente_groq.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Analiza esta imagen. "
                                "1) Describe qué objeto(s) contiene. "
                                "2) Decime si es reciclable o no y en qué contenedor debe ir. "
                                "Responde corto y claro, en español."
                            )
                        },
                        {"type": "image_url", "image_url": {"url": url_imagen}}
                    ]
                }
            ],
            temperature=0.7,
            max_tokens=500
        )

        return completado.choices[0].message.content

    except Exception as e:
        print("Error Groq:", e)
        return None


# ------------------------------
# FUNCIÓN PRINCIPAL QUE USA MAIN.PY
# ------------------------------
def clasificar(ruta_imagen):
    """
    Recibe la ruta local de la imagen (objeto.jpg)
    La sube a internet
    La analiza con Groq
    Devuelve un texto con la descripción
    """
    url = subir_imagen_temporal(ruta_imagen)

    if not url:
        return "❌ No pude subir la imagen."

    descripcion = describir_imagen_con_groq(url)

    if not descripcion:
        return "❌ No pude analizar la imagen."

    return descripcion
