Claro 😊, te propongo un README más completo, organizado y profesional, incluyendo las funciones principales del bot y detalles sobre su uso:

---

# GIRLS-EN-SAMSUNG

**Proyecto final Samsung 🤖 – GIRSU Bot ♻️**

**GIRSU Bot** es un asistente ambiental para **Telegram** diseñado para ayudar a los ciudadanos de Almafuerte, Córdoba, a:

* Reciclar correctamente
* Separar residuos
* Consultar los días de recolección por barrio
* Ubicar puntos limpios y ecopuntos

Forma parte del plan de **Gestión Integral de Residuos Sólidos Urbanos (GIRSU)**, cuyo objetivo es promover una gestión responsable y sostenible de los residuos.

---

## 🌱 Funciones principales

* 🗓️ **Consultar días de recolección**
  Consulta los horarios y días de recolección de residuos comunes, selectivos y verdes según tu barrio o calle.
  -Algunos barrios para probar: Parque, Manuel Belgrano, Las Heras, Arenales.
* ♻️ **Aprender a separar residuos**
  Guía rápida de separación de residuos: reciclables, orgánicos, verdes y no reciclables.

* 📍 **Ubicación de ecopuntos**
  Consulta los puntos limpios de Almafuerte para llevar plásticos, vidrio, latas y otros materiales reciclables.

* 💬 **Información general sobre GIRSU**
  Educación ambiental, recomendaciones y contacto con la Municipalidad para reclamos o dudas.

* 🖼️ **Enviar imágenes de residuos**
  Permite analizar o mostrar ejemplos de residuos mediante fotos o archivos PNG/JPG.

* 🎤 **Soporte de audio y texto**
  Permite enviar consultas por mensaje de texto o grabaciones de voz para interactuar con el bot.

---

## ⚙️ Tecnologías utilizadas

* **Python 3.10**
* **TeleBot / Telegram API** para interacción con usuarios
* **Groq API** para respuestas generadas por IA
* **JSON** para datasets locales de preguntas y respuestas
* **dotenv** para gestión de variables de entorno

---

## 📝 Cómo usar

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/luzb7392-debug/GIRLS-EN-SAMSUNG.git
   ```
2. Crear un archivo `.env` con tus credenciales:

   ```env
   TELEGRAM_TOKEN=<tu_token_telegram>
   GROQ_API_KEY=<tu_api_key_groq>
   ```
3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```
4. Ejecutar el bot:

   ```bash
   python main.py
   ```
5. Abrir Telegram, buscar tu bot y comenzar a interactuar.

---

## 💡 Consideraciones

* Las respuestas se obtienen primero del **dataset local** y, si no hay coincidencias, se consulta la **IA de Groq**.
* Se puede enviar texto o voz; el bot transcribe automáticamente los audios.
* El sistema está diseñado para **uso en Almafuerte**, pero puede adaptarse a otras ciudades modificando los datasets.

---

## 👩‍💻 Equipo desarrollador

* Luz Ríos Becerra
* Catalina Pacioni
* Brunela Abril Torres

---

## 📚 Bibliografía / Referencias

* [Colocaron 5 nuevos contenedores ecológicos](https://www.codigocba.com/post/colocaron-5-nuevos-contenedores-ecologicos)
* [Reciclaje en Córdoba: ecopuntos y campañas](https://infodecordoba.com.ar/reciclar-plastico-y-otros-objetos-en-cordoba-capital-ecopuntos-y-campanas-para-reciclaje/)
* [Almafuerte – Ambiente](https://almafuertecba.gob.ar/ambiente-0)
* [Recolección de residuos Almafuerte](https://almafuertecba.gob.ar/recoleccion-residuos)
* [GIRSU Almafuerte](https://almafuertecba.gob.ar/girsu)
* [Separación de residuos PDF](https://almafuertecba.gob.ar/sites/default/files/girsu_separacion_de_residuos_2_0.pdf)

---

Si querés, puedo hacer también **una versión visual con emojis y secciones plegables** para que quede más atractiva en GitHub, como estilo “portfolio de proyecto” 🌟.

¿Querés que haga eso?
