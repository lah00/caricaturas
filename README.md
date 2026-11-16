# 🏴 Prensa Rebelde | Bot Automatizado de Caricaturas Satíricas

Sistema autónomo de agitación y propaganda política impulsado íntegramente por **Google Gemini**, diseñado para analizar la coyuntura de la lucha de clases, estructurar sátira visual con proporciones grotescas y exageradas (**frentones**, **orejones**, **narizones**), renderizar caricaturas en blanco y negro al estilo de la prensa gráfica opositora, estampar el sello oficial de **La Hiena** y publicarlas automáticamente en Telegram.

---

## ☭ Línea Editorial e Ideológica
Este software responde a los principios del **marxismo-leninismo, el maoísmo, el pensamiento de Ho Chi Minh, el camilismo y el guevarista**. Su crítica rechaza frontalmente tanto a la derecha oligárquica como al reformismo progresista funcional al capital, sirviendo como trinchera digital para la difusión de la verdad revolucionaria y la agitación popular.

---

## 🤖 Arquitectura del Sistema (Gemini + Telegram)
1. **Google Gemini (`gemini-2.5-flash`):** Analiza la coyuntura materialista histórica de la semana (global, regional y nacional), diseña el guion satírico, define las exageraciones físicas y redacta el manifiesto/pie de página combativo para Telegram en formato JSON estricto.
2. **Google Gemini Imagen (`imagen-3.0-generate-001`):** Renderiza la caricatura en formato gráfico de alta calidad con trazo de tinta negra, estilo viñeta de prensa y medios tonos.
3. **Python & Pillow:** Procesa localmente la imagen para redimensionar y superponer limpiamente el logo oficial de **La Hiena**.
4. **GitHub Actions:** Orquesta la ejecución automática del sistema en la nube 24/7 sin necesidad de servidores locales.
5. **Telegram Bot API:** Canal de difusión masiva para la agitación directa.

---

## 📂 Estructura del Repositorio
```text
prensa-rebelde-bot/
├── .github/
│   └── workflows/
│       └── bot.yml         # Automatización en la nube (GitHub Actions)
├── .gitignore              # Archivos protegidos y temporales excluidos
├── requirements.txt        # Dependencias de Python
├── logo la hiena.jpeg      # Sello gráfico oficial de la marca
├── main.py                 # Orquestador principal con Gemini
└── LÉAME.md                # Documentación del proyecto
