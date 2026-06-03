import re
from fastapi import FastAPI, Response, Request
from weasyprint import HTML
from bcv import obtener_tasa_y_fecha

app = FastAPI()

def cambiar_emojis_por_fotos(texto_html):
    # Detecta cualquier emoji en el texto
    patron = re.compile(r'[\U0001f000-\U0001ffff]')
    
    def reemplazar(match):
        # Convierte el emoji en una imagen limpia de internet
        codigo_hex = f"{ord(match.group(0)):x}"
        url_foto = f"https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/{codigo_hex}.png"
        return f'<img src="{url_foto}" style="width: 1.1em; height: 1.1em; vertical-align: middle; margin-right: 3px;" />'
        
    return patron.sub(reemplazar, texto_html)

@app.post("/convertir")
async def convertir_pdf(request: Request):
    body = await request.body()
    html_text = body.decode("utf-8")
    
    # Python cambia los emojis por imágenes automáticamente
    html_final = cambiar_emojis_por_fotos(html_text)
    
    pdf_bytes = HTML(string=html_final).write_pdf()
    return Response(content=pdf_bytes, media_type="application/pdf")
