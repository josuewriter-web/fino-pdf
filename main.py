from fastapi import FastAPI, Response, Request
from weasyprint import HTML

app = FastAPI()

@app.post("/convertir")
async def convertir_pdf(request: Request):
    body = await request.body()
    html_text = body.decode("utf-8")
    pdf_bytes = HTML(string=html_text).write_pdf()
    return Response(content=pdf_bytes, media_type="application/pdf")
