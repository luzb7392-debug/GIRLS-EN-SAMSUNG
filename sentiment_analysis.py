import warnings  #  Permite manejar mensajes de advertencia
warnings.filterwarnings("ignore") #oculta  las advertencias para que no molesten en pantalla

import logging #controlar los mensajes del sistema (logs)
logging.getLogger("transformers").setLevel(logging.ERROR)#  Oculta mensajes de transformers
logging.getLogger("huggingface_hub").setLevel(logging.ERROR) #  Oculta mensajes del repo
logging.getLogger("torch").setLevel(logging.ERROR)#  Oculta mensajes de PyTorch (usa el CPU/GPU)

from transformers import pipeline #  Importa sentimientos

# Cargamos el modelo de análisis de sentimiento
analizador = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    revision="714eb0f"
)
# Pedimos el nombre del usuario

nombre = input(" ¡Hola! ¿Cúal es tu nombre? ")

# Pedimos la reseña del usuario
reseña = input(" Escribí tu reseña sobre el servicio de recolección: ")

# Ejecutamos el análisis
resultado = analizador(reseña)[0]
etiqueta = resultado["label"]     # POSITIVE o NEGATIVE
puntaje = resultado["score"] * 100  # porcentaje

print(f"\nResultado del análisis:")
print(f"Sentimiento: {etiqueta}")
print(f"Confianza: {puntaje:.2f}%")

# Mostramos faces o mensaje de mejora
if etiqueta == "POSITIVE" and puntaje >= 50:
    print("😊 Gracias por tu buena reseña!!", nombre)

else:
    print("😔 Lamentamos que tu experiencia no haya sido buena.")
    sugerencia = input("¿En qué podemos mejorar?  ")
    print(f"Gracias por tu comentario, {nombre} . Valoramos tu opinión: '{sugerencia}'")

