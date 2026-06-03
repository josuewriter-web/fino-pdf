from fastapi import FastAPI, Response, Request
from weasyprint import HTML

app = FastAPI()

@app.post("/convertir")
async def convertir_pdf(request: Request):
    body = await request.body()
    html_text = body.decode("utf-8")
    
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
    
    # Quitamos lo complicado, WeasyPrint buscará el archivo solo con el punto
    pdf_bytes = HTML(string=html_final, base_url=".").write_pdf()
    return Response(content=pdf_bytes, media_type="application/pdf")
