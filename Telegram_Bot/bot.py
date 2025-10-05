import os
import requests
import datetime
import pytz
from config import TELEGRAM_BOT_TOKEN, GEMINI_API_KEY, WEATHER_API_KEY
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool

import random
from google.api_core.exceptions import ResourceExhausted

from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

# para que siempre funcione
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(
 #   os.path.dirname(__file__),
  #  "gen-lang-client-0417110434-6503fb99c175.json"
#)

# ----------------- Configurar Gemini -----------------
llm = ChatGoogleGenerativeAI(
     model="gemini-2.5-flash-lite",
     api_key=GEMINI_API_KEY  
 )

# ----------------- LangChain Tools personalizadas -----------------
def translator_function(texto: str) -> str:
    """
    Traduce texto usando Gemini AI.
    Formato esperado: "Idioma: texto"
    Ejemplo: "Francés: Hello world"
    Maneja límites de cuota de la API.
    """
    try:
        if ":" in texto:
            idioma, contenido = texto.split(":", 1)
            idioma = idioma.strip()
            contenido = contenido.strip()
        else:
            idioma = "es"  # por defecto español
            contenido = texto

        prompt = f"Traduce el siguiente texto al {idioma}: {contenido}"

        for intento in range(3):  # reintentar hasta 3 veces
            try:
                respuesta_obj = llm.invoke(prompt)
                return respuesta_obj.content
            except Exception as e:
                # Detectar error de cuota
                if "Quota exceeded" in str(e) or isinstance(e, ResourceExhausted):
                    wait_time = 5  # segundos a esperar antes de reintentar
                    time.sleep(wait_time)
                else:
                    raise e
        return "❌ Límite de Gemini alcanzado, intenta más tarde."
    except Exception:
        return "❌ No se pudo traducir el texto."


def chat_function(texto: str) -> str:
    try:
        respuesta_obj = llm.invoke(texto)
        return respuesta_obj.content
    except Exception as e:
        return f"❌ Error: {e}"


def joke_function(_: str = "") -> str:
    """Devuelve un chiste aleatorio."""
    jokes = [
        "¿Por qué los programadores confunden Halloween y Navidad? Porque OCT 31 == DEC 25 🎃🎄",
        "¿Cuántos desarrolladores se necesitan para cambiar una bombilla? Ninguno. Es un problema de hardware.",
        "¿Qué le dice un bit al otro? Nos vemos en el bus 🚌💻",
        "¿Qué le dice un 0 a un 1? ¡Eres el único para mí! ❤️"
    ]
    return random.choice(jokes)

translator_tool = Tool(
    name="TranslatorTool",
    description="Traduce textos automáticamente ",
    func=translator_function
)

joke_tool = Tool(
    name="JokeTool",
    description="Cuenta un chiste aleatorio de programación o tecnología.",
    func=joke_function
)

chat_tool = Tool(
    name="ChatTool",
    description="Responde cualquier pregunta general",
    func=chat_function
)

# ----------------- Memoria y agente -----------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools=[translator_tool, joke_tool, chat_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=False,
    handle_parsing_errors=True 
)


# ----------------- Comando /start -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Hola! Soy tu bot con inteligencia Gemini AI.\n\n"
        "Usa /help para ver todos los comandos disponibles."
    )

# ----------------- Comando /help -----------------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 *Comandos disponibles:*\n\n"
        "/start - Bienvenida\n"
        "/help - Ver comandos disponibles\n"
        "/fecha - Fecha y hora actual\n"
        "/fechaCorta - Mostrar solo la fecha\n"
        "/fechaCompleta - Mostrar fecha completa\n"
        "/clima <ciudad> - Ver clima actual\n"
        "/gemini <pregunta> - Preguntar a Gemini AI\n"
        "/calculatorTool <expresión> - Calculadora rápida\n"
        "/ask <pregunta> - Pregunta al agente y él decide qué Tool usar",
        parse_mode="Markdown"
    )


# ----------------- Comando /fecha -----------------
async def fecha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tz = pytz.timezone("America/El_Salvador")
    ahora = datetime.datetime.now(tz)
    fecha_texto = ahora.strftime("%d/%m/%Y %H:%M:%S")
    await update.message.reply_text(f"📅 Fecha y hora actual: {fecha_texto} (GMT-6)")

# ----------------- Comando /fechaCorta -----------------
async def fecha_corta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tz = pytz.timezone("America/El_Salvador")
    ahora = datetime.datetime.now(tz)
    fecha_texto = ahora.strftime("%d/%m/%Y")
    await update.message.reply_text(f"📆 Fecha corta: {fecha_texto}")

# ----------------- Comando /fechaCompleta -----------------
async def fecha_completa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tz = pytz.timezone("America/El_Salvador")
    ahora = datetime.datetime.now(tz)
    fecha_texto = ahora.strftime("%A, %d de %B de %Y, %I:%M %p")
    await update.message.reply_text(f"🕓 Fecha completa: {fecha_texto}")

# ----------------- Comando /clima -----------------
def get_weather_emoji(condicion):
    if "lluvia" in condicion.lower():
        return "🌧️"
    elif "nublado" in condicion.lower():
        return "☁️"
    elif "soleado" in condicion.lower():
        return "☀️"
    elif "nieve" in condicion.lower():
        return "❄️"
    return "🌤️"
    
async def clima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❌ Por favor, indica la ciudad. Ejemplo: /clima Londres")
        return

    ciudad = " ".join(context.args)
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={ciudad}&lang=es"

    try:
        response = requests.get(url) 
        data = response.json() 
        if "error" in data: 
            await update.message.reply_text(f"❌ {data['error']['message']}") 
        else: 
            condicion = data["current"]["condition"]["text"] 
            temp_c = data["current"]["temp_c"] 
            hum = data["current"]["humidity"] 
            emoji = get_weather_emoji(condicion) 
            await update.message.reply_text( 
                f"{emoji}Clima en {ciudad}:\n" 
                f"Condición: {condicion}\n" 
                f"Temperatura: {temp_c}°C\n" 
                f"Humedad: {hum}%" ) 
    except Exception as e: 
        await update.message.reply_text(f"❌ Error al obtener el clima: {e}")


# ----------------- Comando /calculator_tool -----------------
async def calculator_tool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("🧮 Usa /calc seguido de una expresión. Ejemplo: /calc 2+2*3")
        return

    try:
        # Unir todos los argumentos (por si la expresión tiene espacios)
        expression = " ".join(context.args)
        
        # Reemplazar ^ por ** para potencias
        expression = expression.replace("^", "**")

        # Evaluar la expresión
        resultado = eval(expression)

        await update.message.reply_text(f"✅ Resultado: {resultado}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error en la expresión: {e}")

    # ----------------- Comando /ask -----------------
async def ask_agent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Por favor escribe tu pregunta después de /ask")
        return

    pregunta = " ".join(context.args)
    await update.message.chat.send_action(ChatAction.TYPING)

    try:
        # Si tiene el formato "Idioma: texto", usar TranslatorTool directamente
        if ":" in pregunta:
            idioma, contenido = pregunta.split(":", 1)
            # Evitar traducciones vacías
            if contenido.strip():
                respuesta = translator_function(pregunta)
                await update.message.reply_text(respuesta)
                return

        # Si no, usar el agente normalmente
        for intento in range(3):
            try:
                respuesta = agent.run(pregunta)
                await update.message.reply_text(respuesta)
                return
            except Exception as e:
                if "Quota exceeded" in str(e):
                    wait_time = 5
                    await update.message.reply_text(
                        f"⚠️ Límite de Gemini alcanzado, reintentando en {wait_time}s..."
                    )
                    time.sleep(wait_time)
                else:
                    raise e

        await update.message.reply_text("❌ Límite de Gemini alcanzado, intenta más tarde.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error al consultar el agente: {e}")


# ----------------- Comando /gemini -----------------
async def gemini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("❌ Por favor, escribe tu pregunta después de /gemini")
        return

    pregunta = " ".join(context.args)
    try:
        await update.message.chat.send_action(ChatAction.TYPING)
        
        # Llamar directamente al modelo sin usar el agente
        respuesta_obj = llm.invoke(pregunta)
        await update.message.reply_text(respuesta_obj.content)

    except Exception as e:
        await update.message.reply_text(f"❌ Error al consultar Gemini AI: {e}")



async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    try:
        await update.message.chat.send_action(ChatAction.TYPING)

        # Usa la memoria para mantener el contexto
        respuesta = agent.run(user_msg)

        # Si la respuesta está vacía, usa saludo natural
        if not respuesta.strip():
            saludos = [
                "Hola 😄, ¿cómo estás?",
                "¡Hey! ¿Qué tal tu día?",
                "Hola 👋, cuéntame algo interesante",
                "¡Hola! Me alegra verte por aquí 😁"
            ]
            respuesta = random.choice(saludos)

        await update.message.reply_text(respuesta)

    except Exception as e:
        await update.message.reply_text(f"❌ Error al procesar tu mensaje: {e}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("fecha", fecha))
    app.add_handler(CommandHandler("fechaCorta", fecha_corta))
    app.add_handler(CommandHandler("fechaCompleta", fecha_completa))
    app.add_handler(CommandHandler("clima", clima))
    app.add_handler(CommandHandler("calculatorTool", calculator_tool))
    app.add_handler(CommandHandler("ask", ask_agent))
    app.add_handler(CommandHandler("gemini", gemini))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("🤖 Bot en ejecución...")
    app.run_polling()

if __name__ == "__main__":
    main()