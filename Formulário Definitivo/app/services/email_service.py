import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT","587"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM")


def enviar_email_assinatura(nome: str, email: str,  link_assinatura: str):
    msg = MIMEMultipart("alternative")
    #msg = MIMEMultipart()
    msg["Subject"] = "Privatto Documento (Assinatura) - Perfil de Investidor "
    msg["From"] = EMAIL_FROM
    msg["To"] = email

    html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8">
    <title>Assinatura de Documento</title>
  </head>
  <body style="
    margin: 0;
    padding: 0;
    background-color: #f6f7f9;
    font-family: Arial, Helvetica, sans-serif;
    color: #333333;
  ">
    <table width="100%" cellpadding="0" cellspacing="0" style="padding: 24px;">
      <tr>
        <td align="center">
          <table width="600" cellpadding="0" cellspacing="0" style="
            background-color: #ffffff;
            border-radius: 8px;
            padding: 32px;
          ">
            <tr>
              <td>
                <p style="font-size: 16px; margin: 0 0 16px 0;">
                  Olá, <strong>{nome}</strong> 👋
                </p>

                <p style="font-size: 16px; margin: 0 0 16px 0;">
                  Seu documento já está pronto para assinatura.
                </p>

                <p style="font-size: 14px; margin: 0 0 24px 0;">
                  Proteção de Dados: 
                  As informações contidas neste email e em seus anexos são confidenciais e utilizadas exclusivamente
                  para a finalidade a que se destinam. O documento é tratado conforme a legislação vigente de proteção
                  de dados (LGPD).
                </p>

                <p style="font-size: 16px; margin: 0 0 24px 0;">
                  Para continuar, basta clicar no botão abaixo:
                </p>

                <p style="text-align: center; margin: 32px 0;">
                  <a href="{link_assinatura}" target="_blank" style="
                    background-color: #111827;
                    color: #ffffff;
                    text-decoration: none;
                    padding: 14px 28px;
                    border-radius: 6px;
                    font-size: 16px;
                    display: inline-block;
                  ">
                    Assinar documento
                  </a>
                </p>

                <p style="font-size: 14px; color: #555555; margin: 0 0 16px 0;">
                  Caso não consiga acessar pelo botão, copie e cole o link abaixo no seu navegador:
                </p>

                <p style="font-size: 14px; word-break: break-all; color: #2563eb; margin: 0 0 24px 0;">
                  {link_assinatura}
                </p>

                <p style="font-size: 14px; margin: 0 0 24px 0;">
                  Se tiver qualquer dúvida, é só responder este e-mail.
                </p>

                <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 24px 0;">

                <p style="font-size: 13px; color: #6b7280; margin: 0;">
                  Atenciosamente,<br>
                  <strong>Equipe Privatto</strong>
                </p>
              </td>
            </tr>
          </table>

          <p style="font-size: 12px; color: #9ca3af; margin-top: 16px;">
            Este é um e-mail automático. Caso não reconheça esta solicitação, você pode ignorar esta mensagem.
          </p>
        </td>
      </tr>
    </table>
  </body>
</html>
"""

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_FROM, email, msg.as_string()) 

    
  

    


