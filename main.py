from fastapi import FastAPI, Response, Request
from weasyprint import HTML

app = FastAPI()

@app.post("/convertir")
async def convertir_pdf(request: Request):
    body = await request.body()
    html_text = body.decode("utf-8")
    
    # Python le inyecta la fuente al texto automáticamente
    fuente_emojis = """
    <style>
    @font-face {
        font-family: 'MisEmojis';
        src: url('https://cdn.jsdelivr.net/gh/googlefonts/noto-emoji@main/fonts/NotoColorEmoji.ttf');
    }
    *, body, table, td, th, span {
        font-family: 'Arial', 'MisEmojis', sans-serif !important;
    }
    </style>
    """
    html_final = fuente_emojis + html_text
    
    pdf_bytes = HTML(string=html_final).write_pdf()
    return Response(content=pdf_bytes, media_type="application/pdf")
