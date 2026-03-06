import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

ZAPSIGN_API_KEY = os.getenv("ZAPSIGN_API_KEY")
ZAPSIGN_HOST = os.getenv("ZAPSIGN_HOST", "https://api.zapsign.com.br")

if not ZAPSIGN_API_KEY:
    raise RuntimeError("❌ ZAPSIGN_API_KEY não encontrada no .env")

HEADERS = {
    "Authorization": f"Bearer {ZAPSIGN_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def enviar_documento_para_assinatura(file_path: str, nome: str, email: str) -> str:
    print("📤 Enviando documento para o ZapSign...")

    # 🔹 LÊ PDF CORRETAMENTE
    with open(file_path, "rb") as f:
        pdf_bytes = f.read()

    if not pdf_bytes:
        raise Exception("PDF está vazio")

    pdf_base64 = base64.b64encode(pdf_bytes).decode("utf-8")

    payload = {
        "name": f"Questionário de Perfil - {nome}",
        "base64_pdf": pdf_base64,
        "lang": "pt-br",
        "sandbox": False,
        "signers": [
            {
                "name": nome,
                "email": email,
                "auth_mode": "email"
            }
        ]
    }

    url = f"{ZAPSIGN_HOST}/api/v1/docs"

    response = requests.post(
        url,
        headers=HEADERS,
        json=payload,
        timeout=30
    )

    if response.status_code >= 400:
        print("❌ ERRO ZAPSIGN")
        print("STATUS:", response.status_code)
        print("BODY:", response.text)
        raise Exception("Erro ao criar documento no ZapSign")

    data = response.json()

    return data["signers"][0]["sign_url"]
