import os
from openai import OpenAI
from google import genai
from PIL import Image
from io import BytesIO
import requests
from telegram import Bot
import asyncio

# --- CREDENCIALES DESDE VARIABLES DE ENTORNO (GitHub Secrets) ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY") # O DEEPSEEK_API_KEY
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
LOGO_PATH = "logo_la_hiena.png"

# Cliente unificado para Groq / DeepSeek (IA 1, IA 2 y IA 4)
ai_client = OpenAI(
    base_url="https://api.groq.com/openai/v1", # O https://api.deepseek.com
    api_key=GROQ_API_KEY
)

# 1. IA 1 & IA 2: Análisis de Coyuntura y Conceptualización Satírica
def analizar_y_crear_concepto():
    prompt_sistema = """Eres el analista político internacional y director de arte de un medio de izquierda revolucionaria (marxista-leninista, guevarista y camilista). 
    Tu línea crítica rechaza por igual a la derecha fascista/oligarca y a la socialdemocracia progresista funcional al capital.
    Analiza la coyuntura actual de la lucha de clases en Colombia y el mundo. Selecciona un hecho clave (ej. entrega de soberanía, tarifazos, represión o farsa electoral).
    Genera en formato JSON estricto con tres llaves:
    - "contexto_analitico": Breve explicación de los hechos desde el análisis materialista histórico.
    - "prompt_imagen": Descripción detallada en inglés para IA de imagen, especificando caricatura en blanco y negro, trazo de tinta gruesa, estilo viñeta de prensa opositora. Exagera rasgos físicos según el rol (políticos con frentes anchas de hipocresía, banqueros o generales con grandes narices u orejas). Incluye pancartas con texto en español.
    - "pie_pagina": Un único párrafo combativo, sin viñetas, llamativo, de agitación popular que acompañará la caricatura en Telegram."""

    response = ai_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": prompt_sistema},
                  {"role": "user", "content": "Genera la viñeta de agitación para esta semana."}],
        response_format={ "type": "json_object" }
    )
    import json
    return json.loads(response.choices[0].message.content)

# 2. IA 3: Generación de Imagen (Gemini / Imagen 3)
def generar_caricatura_gemini(prompt_visual):
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    estilo_estricto = (
        "Political satirical cartoon in harsh black and white ink drawing style, heavy black outlines, "
        "vintage newspaper halftone dot shading. Satirical caricature with exaggerated facial features "
        "(prominent big foreheads for corrupt politicians, oversized ears for deaf bureaucrats, huge noses). "
        "Sharp class struggle critique aesthetic, clean vector line art. "
        f"Scene details: {prompt_visual}"
    )

    result = client.models.generate_images(
        model='imagen-3.0-generate-002',
        prompt=estilo_estricto,
        config=dict(number_of_images=1, aspect_ratio="1:1", output_mime_type="image/jpeg")
    )
    
    output_filename = "caricatura_bruta.jpg"
    for generated_image in result.generated_images:
        image = Image.open(BytesIO(generated_image.image.image_bytes))
        image.save(output_filename)
    return output_filename

# 3. Superposición del Logo "La Hiena"
def estampar_logo_hiena(imagen_path, logo_path, salida="caricatura_final.jpg"):
    base = Image.open(imagen_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")

    basewidth = int(base.size[0] * 0.20)
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int(float(logo.size[1]) * float(wpercent))
    logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)

    posicion = (base.size[0] - basewidth - 25, 25)
    base.paste(logo, posicion, logo)
    base.convert("RGB").save(salida, "JPEG")
    return salida

# 4. Publicación Automática en Telegram
async def publicar_telegram(imagen_final, texto_pie):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    mensaje_completo = f"🏴 <b>LA HIENA | Prensa Rebelde</b>\n\n{texto_pie}"
    
    with open(imagen_final, 'rb') as photo:
        await bot.send_photo(
            chat_id=TELEGRAM_CHAT_ID, 
            photo=photo, 
            caption=mensaje_completo, 
            parse_mode="HTML"
        )
    print("¡Caricatura y manifiesto publicados en Telegram con éxito!")

# Orquestador Principal
async def main():
    print("🤖 [IA 1 & 2] Analizando coyuntura y diseñando concepto revolucionario...")
    datos = analizar_y_crear_concepto()
    
    print("🎨 [IA 3] Renderizando caricatura en blanco y negro con Gemini...")
    img_bruta = generar_caricatura_gemini(datos["prompt_imagen"])
    
    print("🛠️ Estampando el sello de La Hiena...")
    img_final = estampar_logo_hiena(img_bruta, LOGO_PATH)
    
    print("📢 [IA 4] Difundiendo a través de Telegram...")
    await publicar_telegram(img_final, datos["pie_pagina"])

if __name__ == "__main__":
    asyncio.run(main())
