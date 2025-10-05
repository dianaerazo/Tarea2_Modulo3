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
bash
git clone <TU_REPOSITORIO>
cd <TU_REPOSITORIO>

2. Crear un entorno virtual e instalar depencias
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  o venv\Scripts\activate    # Windows
  pip install -r requirements.txt

3. Configurar variables de entorno en un archivo .env:
  TELEGRAM_BOT_TOKEN=<Tu_token_de_Telegram>
  GEMINI_API_KEY=<Tu_API_Key_de_Gemini_AI>
  WEATHER_API_KEY=<Tu_API_Key_de_WeatherAPI>

4. Ejecutar el comando para correr el bot:
   python bot.py

**Comandos disponibles con ejemplos**
| Comando                       | Descripción                          | Ejemplo                                 |
| ----------------------------- | ------------------------------------ | --------------------------------------- |
| `/start`                      | Mensaje de bienvenida                | `/start`                                |
| `/help`                       | Lista de comandos                    | `/help`                                 |
| `/fecha`                      | Fecha y hora actual                  | `/fecha`                                |
| `/fechaCorta`                 | Solo la fecha                        | `/fechaCorta`                           |
| `/fechaCompleta`              | Fecha completa                       | `/fechaCompleta`                        |
| `/clima <ciudad>`             | Clima de una ciudad                  | `/clima Madrid`                         |
| `/calculatorTool <expresión>` | Calculadora rápida                   | `/calculatorTool 25*8`                  |
| `/gemini <pregunta>`          | Pregunta a Gemini AI                 | `/gemini ¿Quién es Albert Einstein?`    |
| `/ask <pregunta>`             | LangChain Agent decide qué tool usar | `/ask Tradúceme al francés: Hola mundo` |

**Algunas imágenes del avance del bot**
<img width="1091" height="776" alt="Captura de pantalla 2025-10-04 a la(s) 11 52 17 p  m" src="https://github.com/user-attachments/assets/b570f769-220a-4c7a-98c5-95c08bc7db29" />

<img width="967" height="774" alt="Captura de pantalla 2025-10-04 a la(s) 11 53 26 p  m" src="https://github.com/user-attachments/assets/0689a05a-ded8-4f31-9637-8d47b2a740ae" />

<img width="963" height="663" alt="Captura de pantalla 2025-10-04 a la(s) 11 53 58 p  m" src="https://github.com/user-attachments/assets/791e857b-d62a-4f81-a130-6c791957ad68" />

<img width="947" height="780" alt="Captura de pantalla 2025-10-04 a la(s) 11 54 17 p  m" src="https://github.com/user-attachments/assets/17f1e5f8-d9fa-4197-bfae-f57048c1fc34" />

**APIs utilizadas**
Gemini AI
 - Generación de respuestas inteligentes y traducción.

WeatherAPI
 - Consultar clima de ciudades en tiempo real.

**Créditos y contacto**
Autor: Diana Erazo
Correo: 00149823@uca.edu.sv
GitHub: dianaerazo

Proyecto realizado como parte del Bootcamp de Machine Learning de KODIGO.
