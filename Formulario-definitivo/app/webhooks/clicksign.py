from fastapi import APIRouter, Request
import requests
import os

router = APIRouter()

ASSINADOS_DIR = "app/storage/assinados"
os.makedirs(ASSINADOS_DIR, exist_ok=True)


@router.post("/clicksign/webhook")
async def clicksign_webhook(request: Request):
    payload = await request.json()

    if payload.get("event") == "document_signed":
        doc = payload["document"]
        url = doc["download_url"]
        key = doc["key"]

        pdf = requests.get(url).content
        with open(f"{ASSINADOS_DIR}/{key}.pdf", "wb") as f:
            f.write(pdf)

    return {"status": "ok"}
