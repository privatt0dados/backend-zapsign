# 📄 Sistema de Automação de Formulários com Assinatura Digital (Tally + FastAPI + ZapSign)

Este projeto implementa uma **pipeline completa de automação** que conecta:

**Tally → Backend em FastAPI → ZapSign**

O objetivo é receber dados de um formulário, processar essas informações no backend e **gerar automaticamente um documento para assinatura digital via ZapSign**.

---

## 🚀 Visão Geral do Fluxo

1. Usuário preenche o formulário no **Tally**
2. O Tally dispara um **webhook**
3. O backend em **FastAPI** recebe os dados
4. O backend:
   - valida os dados
   - gera o payload do documento
   - envia para a **API da ZapSign**
5. A ZapSign gera o documento e envia para **assinatura digital**

---

## 🧱 Arquitetura do Projeto 

## ⚙️ Requisitos

- Python **3.10+** (recomendado: **3.11**)
- Virtualenv
- Conta ativa no:
  - Tally
  - ZapSign -> plano ativo
- Ngrok (para expor o backend local)

---

## 🛠️ Instalação do Ambiente

## 1️⃣ Criar ambiente virtual


python -m venv venv

## 2️⃣ Ativar ambiente virtual
Windows:
.\venv\Scripts\activate

Linux / macOS:
source venv/bin/activate

## 3️⃣ Instalar dependências
pip install -r requirements.txt

## Variáveis de Ambiente
arquivo .env na raiz do projeto:

- ZAPSIGN_API_KEY=chave_da_api
- ZAPSIGN_BASE_URL=https://api.zapsign.com.br/api/v1

ZAPSIGN_API_KEY=3e41e694-892c-4186-a783-b990bdb09a27072b7aca-e137-47c9-9fd5-67a15289c2ba
ZAPSIGN_HOST=https://api.zapsign.com.br

#enviar o email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=privatt0.dados@gmail.com
EMAIL_PASS=ghprcacafdouzbzt
EMAIL_FROM=privatt0.dados@gmail.com

#segurança
Tally_webhook_secret=mfcOftç6Ndo6e1e82gadfSDdgKÇ48Ç527ieof984DcDKF350EÇKPH

## ▶️ Rodando o Backend Localmente
Estando dentro da pasta principal do projeto:

python -m uvicorn app.main:app --reload
Uvicorn running on http://127.0.0.1:8000
- (venv) PS C:\Users\ti_Pr\OneDrive\Documentos\Codes\Formulario\Formulario> python -m uvicorn app.main:app --reload   (colar no terminal 1) 

https://SEU_SUBDOMINIO.ngrok-free.dev/docs
🌐 Expondo o Backend para a Internet (Ngrok)
ngrok http 8000
receber uma URL pública como: https://xxxxx.ngrok-free.dev
- (venv) PS C:\Users\ti_Pr\OneDrive\Documentos\Codes\Formulario\Formulario\app> ngrok http 8000 (colar no terminal 2)

--- 

### Testando a pipeline 

# Suba o backend:
python -m uvicorn app.main:app --reload

# Inicie o ngrok:
ngrok http 8000

# Envie um formulário pelo Tally
- Verifique:
  -Logs do backend
  -Painel do ngrok: http://127.0.0.1:4040
  -Documento gerado na ZapSign

