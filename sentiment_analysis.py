# sentiment_analysis.py (con paso de usuario)
def pedir_opinion(bot, message):
    """
    Función que inicia la encuesta de opinión.
    Pide al usuario que escriba su reseña y luego llama a analizar_sentimiento.
    """
    bot.send_message(message.chat.id, "💬 Escribí tu reseña sobre el servicio de recolección:")
    bot.register_next_step_handler(message, analizar_sentimiento)

def analizar_sentimiento(message, bot):
    """
    Analiza si el texto del usuario es positivo o negativo usando palabras clave.
    """

    texto = message.text.lower()

    positivas = ["bien", "bueno", "excelente", "genial", "me gusta", "perfecto", "muy bueno"]
    negativas = ["mal", "malo", "horrible", "pesimo", "terrible", "no funciona", "tarde"]

    puntaje = 0
    for palabra in positivas:
        if palabra in texto:
            puntaje += 1
    for palabra in negativas:
        if palabra in texto:
            puntaje -= 1

    if puntaje > 0:
        bot.send_message(
            message.chat.id,
            "😊 ¡Gracias por tu comentario positivo! Nos alegra que estés conforme."
        )
    elif puntaje < 0:
        bot.send_message(
            message.chat.id,
            "😔 Lamentamos que tu experiencia no haya sido buena.\n"
            "¡Gracias por contarnos! Lo tendremos en cuenta."
        )
    else:
        bot.send_message(
            message.chat.id,
            "🙂 Gracias por tu comentario. ¡Lo tendremos en cuenta!"
        )
