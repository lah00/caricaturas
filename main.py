import os
import json
import asyncio
from io import BytesIO
from openai import OpenAI
from google import genai
from PIL import Image
from telegram import Bot

# --- 1. CONFIGURACIÓN DE CREDENCIALES (Variables de Entorno / GitHub Secrets) ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Ruta exacta del logo seleccionado en tu repositorio
LOGO_PATH = "logo la hiena.jpeg"

# Cliente unificado para Groq (compatible con formato OpenAI)
ai_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

# --- 2. IA 1 & IA 2: ANÁLISIS DE COYUNTURA Y GUION SATÍRICO ---
def analizar_y_crear_concepto():
    prompt_sistema = """Eres el analista político internacional y director de arte de un medio de izquierda revolucionaria (marxista-leninista, guevarista y camilista). 
    Tu línea crítica rechaza por igual a la derecha fascista y a la socialdemocracia reformista funcional al capital.
    Analiza la coyuntura actual de la lucha de clases en Colombia y el mundo. Selecciona un hecho clave reciente (tarifazos, entrega de soberanía, represión o farsa burguesa).
    Devuelve estrictamente un objeto JSON con tres llaves:
    - "contexto_analitico": Breve explicación de los hechos desde el materialismo histórico.
    - "prompt_imagen": Descripción detallada en INGLÉS para la IA generativa de imágenes. Especifica: caricatura política satírica en blanco y negro, trazo de tinta gruesa, estilo viñeta de prensa opositora. Exagera rasgos físicos según el personaje (políticos con frentes anchas de hipocresía, burócratas con grandes orejas sordas al pueblo, banqueros o militares con grandes narices). Incluye pancartas o carteles con texto visible en español.
    - "pie_pagina": Un único párrafo combativo, sin viñetas, de agitación popular que acompañará la caricatura en Telegram, alineado con tus ideales revolucionarios."""

    response = ai_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": "Genera la viñeta de agitación para la publicación de hoy."}
        ],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)

# --- 3. IA 3: GENERACIÓN GRÁFICA CON GEMINI (IMAGEN 3) ---
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
        config=dict(
            number_of_images=1, 
            aspect_ratio="1:1", 
            output_mime_type="image/jpeg"
        )
    )
    
    output_filename = "caricatura_bruta.jpg"
    for generated_image in result.generated_images:
        image = Image.open(BytesIO(generated_image.image.image_bytes))
        image.save(output_filename)
        
    return output_filename

# --- 4. PROCESAMIENTO LOCAL: ESTAMPADO DEL LOGO ---
def estampar_logo_hiena(imagen_path, logo_path, salida="caricatura_final.jpg"):
    base = Image.open(imagen_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")

    # Redimensionar el logo proporcionalmente (20% del ancho de la viñeta)
    basewidth = int(base.size[0] * 0.20)
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int(float(logo.size[1]) * float(wpercent))
    logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)

    # Posicionar el logo en la esquina superior derecha con un margen de 25 píxeles
    posicion = (base.size[0] - basewidth - 25, 25)
    
    base.paste(logo, posicion)
    base.convert("RGB").save(salida, "JPEG")
    return salida

# --- 5. DIFUSIÓN AUTOMÁTICA EN TELEGRAM ---
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
    print("¡Caricatura y manifiesto publicados con éxito en Telegram!")

# --- ORQUESTADOR PRINCIPAL ---
async def main():
    print("🤖 [IA 1 & 2] Analizando coyuntura y diseñando concepto revolucionario...")
    datos = analizar_y_crear_concepto()
    print(f"-> Contexto seleccionado: {datos['contexto_analitico'][:100]}...")

    print("🎨 [IA 3] Renderizando caricatura en blanco y negro con Gemini...")
    img_bruta = generar_caricatura_gemini(datos["prompt_imagen"])
    
    print("🛠️ Procesando imagen y aplicando el sello de La Hiena...")
    img_final = estampar_logo_hiena(img_bruta, LOGO_PATH)
    
    print("📢 [IA 4] Enviando comunicación gráfica a Telegram...")
    await publicar_telegram(img_final, datos["pie_pagina"])

if __name__ == "__main__":
    asyncio.run(main())
