import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
DATASET_PATH = 'dataset2.json'

def cargar_dataset():
    try:
        with open(DATASET_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def buscar_en_dataset(pregunta, dataset):
    pregunta = pregunta.strip().lower()
    for item in dataset:
        if item['pregunta'].strip().lower() == pregunta:
            return item['respuesta']
    return None

def respuesta_groq(mensaje):
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": mensaje}]
    }
    try:
        resp = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=20)
        if resp.status_code == 200:
            return resp.json()['choices'][0]['message']['content'].strip()
        else:
            return f"[Error Groq {resp.status_code}]"
    except Exception as e:
        return f"[Error de conexión a Groq: {e}]"
