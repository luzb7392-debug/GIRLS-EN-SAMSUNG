
import json

DATASET2_PATH = "dataset2.json"


def cargar_dataset2():
    try:
        with open(DATASET2_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


dataset2 = cargar_dataset2()


def buscar_barrio(barrio):
    barrio = barrio.strip().lower()

    for item in dataset2:
        if item["barrio"].strip().lower() == barrio:
            return item["info"]

    return None



# -------------------------------
def procesar_texto(texto):
    texto = texto.strip().lower()


    respuesta = buscar_barrio(texto)

    if respuesta:
        return f"🚛 {respuesta}"


    return "❌ No tengo ese barrio registrado. ¿Podés repetirlo?"


import speech_recognition as sr

def procesar_audio(ruta_audio):
    r = sr.Recognizer()

    try:
        with sr.AudioFile(ruta_audio) as source:
            audio = r.record(source)

        texto = r.recognize_google(audio, language="es-AR")


        return procesar_texto(texto)

    except sr.UnknownValueError:
        return "⚠️ No pude entender el audio. ¿Podés repetirlo?"
    except Exception as e:
        return f"❌ Error procesando audio: {e}"
