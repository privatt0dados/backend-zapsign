from fastapi import FastAPI, Request, HTTPException
from app.services.pdf_generator import gerar_pdf
from app.services.zapsign_services import enviar_documento_para_assinatura
from app.services.email_service import enviar_email_assinatura
import unicodedata
import re 
import os 

import os
import uvicorn

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8000))  # pega porta do Render
    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT)

app = FastAPI()

# ==========================
# UTILIDADES
# ==========================

def normalizar_nome_arquivo(texto: str) -> str:
    texto = texto or "cliente"
    texto = unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")
    texto = re.sub(r"[^a-zA-Z0-9_-]", "_", texto)
    return texto.lower()


def extrair_respostas(fields):
    respostas = []

    for field in fields:
        if field.get("type") == "MULTIPLE_CHOICE":
            pergunta = field.get("label", "Pergunta")

            value_ids = field.get("value") or []
            options = field.get("options") or []

            textos = [
                opt.get("text")
                for opt in options
                if opt.get("id") in value_ids
            ]

            resposta_texto = ", ".join(textos) if textos else "Não respondido"
            respostas.append((pergunta, resposta_texto))

    return respostas


def perfil_por_score(score):
    perfil = "Não definido"
    descricao = "Perfil não identificado com base no score informado."

    try:
        score = int(score)
    except Exception:
        return perfil, descricao

    if score <= 23:
        perfil = "Ultraconservador"
        descricao = (
            "O perfil Ultraconservador caracteriza-se por clientes com alta aversão ao risco," 
            "cujo principal objetivo é minimizar perdas e obter retornos estáveis e previsíveis." 
            "A prioridade é a preservação total do capital, mesmo que isso implique baixa rentabilidade." 
            "Os ativos recomendados concentram-se em títulos públicos, fundos de renda fixa de baixo risco" 
            "e instrumentos de alta liquidez, como a poupança. A exposição ao risco é considerada baixa, adequada" 
            "a famílias que buscam segurança máxima e estabilidade."
        )

    elif 24 <= score <= 32:
        perfil = "Conservador"
        descricao = (
            "O perfil Conservador mantém foco na preservação do capital, mas admite uma mínima volatilidade em troca" 
            "de crescimento gradual com riscos controlados. Nesse caso, além da renda fixa tradicional, a carteira pode" 
            "incluir fundos multimercado e ações de empresas consolidadas em setores estáveis, que fornecem equilíbrio" 
            "entre proteção e retorno adicional. A exposição ao risco é moderada, adequada a investidores que priorizam" 
            "solidez mas aceitam algum nível de oscilação."
        )

    elif 33 <= score <= 41:
        perfil = "Moderado"
        descricao = (
            "O perfil Moderado representa clientes dispostos a aceitar um grau equilibrado de risco para buscar retornos" 
            "superiores à média. O objetivo é estruturar uma gestão balanceada, que combina segurança e crescimento. As" 
            "carteiras desse perfil tendem a ser mais diversificadas, englobando renda fixa corporativa, ações de empresas" 
            "de médio e grande porte e fundos de investimento variados. A exposição ao risco situa-se entre moderada e alta," 
            "refletindo a busca por retornos consistentes sem abrir mão de proteção parcial."
        )

    elif 42 <= score <= 49:
        perfil = "Agressivo"
        descricao = (
            "O perfil Agressivo reflete investidores com maior tolerância à volatilidade, que buscam retornos significativamente" 
            "mais elevados. A estratégia é mais dinâmica, com peso maior em renda variável e abertura a mercados emergentes e" 
            "investimentos alternativos. As carteiras desse perfil incluem ações de empresas de crescimento, fundos de" 
            "investimento especializados e ativos de maior risco relativo. A exposição ao risco é alta, adequada a clientes que" 
            "aceitam oscilações especializados e ativos de maior risco relativo. A exposição ao risco é alta, adequada a" 
            "clientes que aceitam oscilações relevantes no curto prazo em troca de valorização no longo prazo."
            
        )

    else:
        perfil = "Arrojado"
        descricao = (
            "O perfil Arrojado corresponde a investidores que priorizam a maximização dos retornos e estão prontos para" 
            "assumir riscos significativos, aceitando alta volatilidade em suas carteiras. Esse perfil concentra-se em" 
            "ativos de alto crescimento, como ações disruptivas, fundos de venture capital, criptomoedas e outras oportunidades" 
            "de investimento de elevado risco. A exposição ao risco é considerada muito alta, típica de clientes que possuem" 
            "elevado grau de sofisticação financeira, horizonte de longo prazo e ampla resiliência a oscilações de mercado."
        )

    return perfil, descricao


# ==========================
# ROTAS
# ==========================

@app.get("/")
def healthcheck():
    return {"status": "ok"}


@app.post("/tally/webhook")
async def receber_webhook_tally(request: Request):
    print("\n🔥 WEBHOOK DO TALLY RECEBIDO")

    payload = await request.json()
    data = payload.get("data", {})
    fields = data.get("fields", [])

    nome = None
    email = None
    score = None

    # 🔍 Extração segura dos campos principais
    for field in fields:
        label = (field.get("label") or "").strip().lower()
        value = field.get("value")

        if label == "nome":
            nome = value

        elif label in ["e-mail", "email"]:
            email = value

        elif label == "score":
            score = value

    if not nome or not email:
        raise HTTPException(
            status_code=400,
            detail="Nome ou e-mail não informados no formulário"
        )

    respostas = extrair_respostas(fields)
    perfil, descricao_perfil = perfil_por_score(score)

    #print("📌 Nome:", nome)
    #print("📌 Email:", email)
    #print("📌 Perfil:", perfil)
    #print("📌 Total respostas:", len(respostas))

    # ==========================
    # GERAÇÃO DO PDF
    # ==========================

    caminho_pdf = gerar_pdf(
        nome=nome,
        email=email,
        perfil=perfil,
        descricao_perfil=descricao_perfil,
        respostas=respostas
    )

    #print("📄 PDF gerado em:", caminho_pdf)

    # ==========================
    # ZAPSIGN + EMAIL
    # ==========================

    try:
        print("🚀 Enviando PDF para o ZapSign...")

        sign_url = enviar_documento_para_assinatura(
            file_path=caminho_pdf,
            nome=nome,
            email=email
        )

        print("✍️ Documento criado com sucesso!")
        #print("🔗 LINK DE ASSINATURA:", sign_url)

        print("📧 Enviando email...")
        enviar_email_assinatura(
            nome=nome,
            email=email,
            link_assinatura=sign_url
        )
        print("✅ Email enviado com sucesso!")
    
    finally:
        # 🔥 AQUI ESTÁ O PONTO-CHAVE
        if os.path.exists(caminho_pdf):
            os.remove(caminho_pdf)
            print("🗑️ PDF removido com sucesso:", caminho_pdf)

    #except Exception as e:
    #    print("❌ Erro ao enviar para o ZapSign:", str(e))
    #    raise HTTPException(
    #        status_code=500,
    #        detail="Erro ao gerar link de assinatura"
    #    )

    # ==========================
    # RESPOSTA FINAL
    # ==========================

    return {
        "status": "ok",
        "perfil": perfil,
        "sign_url": sign_url
    } 
   
