# Tarea2_Modulo3

# 🤖 Telegram Bot con Gemini AI y LangChain

## Descripción del proyecto
Este proyecto es un **bot de Telegram** potenciado por **Gemini AI** y **LangChain**, capaz de responder preguntas, traducir textos, realizar cálculos, consultar el clima y contar chistes.  
El bot puede decidir automáticamente qué herramienta usar basándose en la consulta del usuario gracias a un **LangChain Agent con memoria conversacional**.

---

## Funcionalidades
- **Comandos básicos**
  - `/start` - Mensaje de bienvenida.
  - `/help` - Lista de comandos disponibles.
- **Fecha y hora**
  - `/fecha` - Fecha y hora actual.
  - `/fechaCorta` - Solo la fecha.
  - `/fechaCompleta` - Fecha completa con día y hora.
- **Clima**
  - `/clima <ciudad>` - Consulta el clima actual de una ciudad usando WeatherAPI.
- **Calculadora**
  - `/calculatorTool <expresión>` - Calculadora rápida que soporta operaciones básicas y potencias (`^`).
- **Gemini AI**
  - `/gemini <pregunta>` - Pregunta directamente a Gemini AI.
- **LangChain Agent**
  - `/ask <pregunta>` - El agente decide automáticamente qué herramienta usar (traducción, chistes).
- **Traducción**
  - `TranslatorTool` - Traduce textos automáticamente. Formato: `"Idioma: texto"` (ej: `"Francés: Hello world"`).
- **Chistes**
  - `JokeTool` - Cuenta chistes aleatorios sobre programación o tecnología.
- **Eco de mensajes**
  - Responde cualquier texto no reconocido repitiendo el mensaje del usuario.

---

## Instrucciones de instalación local

1. Clonar el repositorio:
```bash
git clone <TU_REPOSITORIO>
cd <TU_REPOSITORIO>
