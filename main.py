import os
import json
import asyncio
from io import BytesIO
from openai import OpenAI
from google import genai
from PIL import Image
from telegram import Bot

# --- 1. CONFIGURACIÓN DE CREDENCIALES (GitHub Secrets) ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Ruta exacta del logo en tu repositorio
LOGO_PATH = "logo la hiena.jpeg"

# Clientes configurados para Groq y OpenRouter (con timeout de 1000 segundos)
groq_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY,
    timeout=1000.0
)

openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    timeout=1000.0
)

# --- 2. GROQ (IA 1): ANÁLISIS DE COYUNTURA GLOBAL Y LATINOAMERICANA ---
def analizar_coyuntura_groq():
    prompt_sistema = """Eres el analista político internacional de un medio de comunicación popular con línea marxista-leninista, maoísta, antiimperialista, camilista y guevarista. 
    Tu crítica rechaza frontalmente tanto a la derecha oligárquica como al reformismo progresista funcional al capital.
    Analiza la coyuntura actual de la lucha de clases, tarifas, opresión estatal o entregas de soberanía en Colombia, América Latina y el mundo.
    Genera un análisis materialista, crudo y directo de la situación actual que sirve de base para una caricatura de agitación."""
    
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Modelo activo y recomendado en Groq
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": "Analiza los hechos más urgentes de la semana sobre la opresión burguesa y la resistencia popular."}
        ]
    )
    return response.choices[0].message.content

# --- 3. OPENROUTER (IA 2): DIRECTOR DE ARTE Y REDACTOR DEL MANIFIESTO ---
def generar_guion_y_pie_openrouter(analisis_previo):
    prompt_sistema = """Eres el director de arte y jefe de redacción de 'Prensa Rebelde'. 
    Basándote en el análisis político provisto, debes generar un objeto JSON estricto con exactamente dos llaves:
    1. "prompt_imagen": Descripción detallada en INGLÉS para una IA generativa de imágenes. Especifica: caricatura política satírica en blanco y negro, trazo de tinta gruesa, estilo viñeta de prensa opositora. Exagera de manera grotesca y precisa los rasgos físicos según el rol: políticos burgueses con frentes gigantescas de hipocresía (frentones), burócratas o tecnócratas con orejas descomunales sordas al clamor popular (orejones), y banqueros o militares con narices inmensas (narizones). Incluye carteles o pancartas con textos de protesta visibles en español.
    2. "pie_pagina": Un único párrafo combativo, sin viñetas, de agitación popular que acompañará la caricatura en Telegram, alineado rígidamente con el marxismo-leninismo, el maoísmo, el pensamiento de Ho Chi Minh, el camilismo y el guevarismo."""

    response = openrouter_client.chat.completions.create(
        model="deepseek/deepseek-chat",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f"A partir de este análisis de coyuntura, genera la viñeta satírica y el pie de página revolucionario:\n\n{analisis_previo}"}
        ],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)

# --- 4. GEMINI (IA 3): RENDERIZADO GRÁFICO DE LA CARICATURA ---
def generar_caricatura_gemini(prompt_visual):
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    estilo_estricto = (
        "Political satirical cartoon in harsh black and white ink drawing style, heavy black outlines, "
        "vintage newspaper halftone dot shading. Satirical caricature with heavily exaggerated facial features: "
        "massive giant foreheads for corrupt politicians (frentones), grotesquely oversized ears for deaf bureaucrats (orejones), "
        "huge dominant noses (narizones). Sharp class struggle critique aesthetic, clean vector line art. "
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

# --- 5. PROCESAMIENTO LOCAL: ESTAMPADO DEL LOGO ---
def estampar_logo_hiena(imagen_path, logo_path, salida="caricatura_final.jpg"):
    base = Image.open(imagen_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")

    basewidth = int(base.size[0] * 0.20)
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int(float(logo.size[1]) * float(wpercent))
    logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)

    posicion = (base.size[0] - basewidth - 25, 25)
    base.paste(logo, posicion)
    base.convert("RGB").save(salida, "JPEG")
    return salida

# --- 6. DIFUSIÓN EN TELEGRAM ---
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
    print("🌍 [Groq] Analizando coyuntura global, regional y nacional...")
    analisis = analizar_coyuntura_groq()
    
    print("🎨 [OpenRouter] Procesando sátira visual (frentones, orejones, narizones) y manifiesto...")
    datos_creativos = generar_guion_y_pie_openrouter(analisis)

    print("🖌️ [Google Gemini] Renderizando caricatura en blanco y negro...")
    img_bruta = generar_caricatura_gemini(datos_creativos["prompt_imagen"])
    
    print("🛠️ Aplicando el sello oficial de La Hiena...")
    img_final = estampar_logo_hiena(img_bruta, LOGO_PATH)
    
    print("📢 [Telegram] Publicando contenido en el canal...")
    await publicar_telegram(img_final, datos_creativos["pie_pagina"])

if __name__ == "__main__":
    asyncio.run(main())
