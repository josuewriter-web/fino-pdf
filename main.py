from fastapi import FastAPI, Response, Request
from weasyprint import HTML, FontConfiguration

app = FastAPI()

@app.post("/convertir")
async def convertir_pdf(request: Request):
    body = await request.body()
    html_text = body.decode("utf-8")
    
    font_config = FontConfiguration()
    
    fuente_emojis = """
    <style>
    @font-face {
        font-family: 'MisEmojis';
        src: url('NotoColorEmoji-Regular.ttf');
    }
    *, body, table, td, th, span {
        font-family: 'Arial', 'MisEmojis', sans-serif !important;
    }
    </style>
    """
    html_final = fuente_emojis + html_text
    
    pdf_bytes = HTML(string=html_final, base_url=".").write_pdf(font_config=font_config)
    return Response(content=pdf_bytes, media_type="application/pdf")
