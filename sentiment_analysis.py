def analizar_sentimiento(bot, message):
    import warnings  # Permite manejar mensajes de advertencia
    warnings.filterwarnings("ignore")  # Oculta las advertencias para que no molesten

    import telebot as tlb
    import os
    import logging  # Controla los mensajes del sistema (logs)
    from transformers import pipeline  # Importa el modelo de análisis de sentimiento
    from dotenv import load_dotenv  # Para leer el archivo .env

    # Oculta mensajes innecesarios
    logging.getLogger("transformers").setLevel(logging.ERROR)
    logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
    logging.getLogger("torch").setLevel(logging.ERROR)

    # Cargar archivo .env
    load_dotenv()

    # Variables de entorno 
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    if not TELEGRAM_TOKEN:
        raise ValueError("No se encuentra el TOKEN de Telegram en el archivo .env")

    # Instanciar objetos
    bot = tlb.TeleBot(TELEGRAM_TOKEN)

    # Cargamos el modelo de análisis de sentimiento
    analizador = pipeline(
        "sentiment-analysis",
        model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
        revision="714eb0f"
    )

    # Pedimos la reseña del usuario
    reseña = input("Escribí tu reseña sobre el servicio de recolección: ")

    # Ejecutamos el análisis
    resultado = analizador(reseña)[0]
    puntaje = resultado["score"] * 100  # Convertimos a porcentaje

    # Según el puntaje, mostramos el mensaje adecuado
    if puntaje >= 50:
        print(f"😊 ¡Gracias por tu reseña!")
    else:
        print("😔 Lamentamos que tu experiencia no haya sido buena.")
        sugerencia = input("¿En qué podemos mejorar? 💬 ")
        print(f"Gracias por tu comentario. Valoramos tu opinión: '{sugerencia}'")
