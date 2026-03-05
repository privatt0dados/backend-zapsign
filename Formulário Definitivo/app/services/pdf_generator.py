from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
import os
import re
import unicodedata

# ==================================================
# CONFIG
# ==================================================

OUTPUT_DIR = "app/storage/gerados"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MARGEM_X = 50
MARGEM_Y = 50

# ==================================================
# UTILIDADES
# ==================================================

def limpar_nome(nome):
    if not nome:
        return "cliente_sem_nome"

    nome = str(nome)
    nome_normalizado = unicodedata.normalize("NFKD", nome)
    nome_sem_acento = nome_normalizado.encode("ASCII", "ignore").decode("ASCII")

    return re.sub(r"[^a-zA-Z0-9_-]", "_", nome_sem_acento)


def draw_paragraph(c, text, x, y, max_width, leading=14, font="Helvetica", font_size=10):
    """
    Escreve texto com quebra automática de linha.
    Retorna a nova posição Y após o texto.
    """
    c.setFont(font, font_size)
    text_object = c.beginText(x, y)
    text_object.setLeading(leading)

    words = text.split(" ")
    line = ""

    for word in words:
        test_line = f"{line} {word}".strip()
        if stringWidth(test_line, font, font_size) <= max_width:
            line = test_line
        else:
            text_object.textLine(line)
            line = word

    if line:
        text_object.textLine(line)

    c.drawText(text_object)
    return text_object.getY()

# ==================================================
# GERADOR DE PDF
# ==================================================

def gerar_pdf(nome, email, perfil, descricao_perfil, respostas):
    nome_limpo = limpar_nome(nome)
    filename = f"questionario_{nome_limpo}.pdf"
    caminho = os.path.join(OUTPUT_DIR, filename)

    c = canvas.Canvas(caminho, pagesize=A4)
    largura, altura = A4

    y = altura - MARGEM_Y

    # ==================================================
    # TÍTULO
    # ==================================================

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(largura / 2, y, "Questionário de Perfil do Cliente")

    y -= 20
    c.setLineWidth(1)
    c.line(MARGEM_X, y, largura - MARGEM_X, y)

    # ==================================================
    # DADOS DO CLIENTE
    # ==================================================

    y -= 30
    c.setFont("Helvetica", 11)
    c.drawString(MARGEM_X, y, f"Nome: {nome}")

    y -= 18
    c.drawString(MARGEM_X, y, f"E-mail: {email}")

    y -= 18
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGEM_X, y, f"Perfil do Investidor: {perfil}")

    # ==================================================
    # DESCRIÇÃO DO PERFIL
    # ==================================================

    if descricao_perfil:
        y -= 18
        y = draw_paragraph(
            c=c,
            text=descricao_perfil,
            x=MARGEM_X,
            y=y,
            max_width=largura - (MARGEM_X * 2),
            leading=14,
            font="Helvetica",
            font_size=10
        )

    # ==================================================
    # RESPOSTAS
    # ==================================================

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGEM_X, y, "Respostas do Questionário")

    y -= 12
    c.line(MARGEM_X, y, largura - MARGEM_X, y)

    y -= 20
    c.setFont("Helvetica", 10)

    for pergunta, resposta in respostas:
        texto_resposta = f"{pergunta}: {resposta}"

        y = draw_paragraph(
            c=c,
            text=texto_resposta,
            x=MARGEM_X + 10,
            y=y,
            max_width=largura - (MARGEM_X * 2) - 10,
            leading=13,
            font="Helvetica",
            font_size=10
        )

        y -= 8

        if y < 120:
            c.showPage()
            y = altura - MARGEM_Y
            c.setFont("Helvetica", 10)

    # ==================================================
    # TERMO / DECLARAÇÃO
    # ==================================================

    y -= 25
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGEM_X, y, "Declaração")

    y -= 10
    c.line(MARGEM_X, y, largura - MARGEM_X, y)

    y -= 18

    termo = (
        "Declaro que as informações contidas neste questionário são verdadeiras, "
        "estando ciente de que as recomendações de investimentos dependem das informações prestadas. "
        "Tomei conhecimento do meu perfil de investimentos aferido a partir das informações fornecidas, "
        "estando ciente de que a instituição poderá informar se as operações por mim realizadas estão "
        "de acordo com aquelas recomendadas para o meu perfil de investimentos. "
        "Comprometo-me a manter este questionário atualizado, informando prontamente quaisquer alterações, "
        "bem como a atualizá-lo sempre que solicitado."
    )

    y = draw_paragraph(
        c=c,
        text=termo,
        x=MARGEM_X,
        y=y,
        max_width=largura - (MARGEM_X * 2),
        leading=14,
        font="Helvetica",
        font_size=10
    )

    # ==================================================
    # ASSINATURA
    # ==================================================

    #y -= 40
    #c.setLineWidth(0.8)

    #c.line(MARGEM_X, y, 300, y)
    #c.setFont("Helvetica", 9)
    #c.drawString(MARGEM_X, y - 12, "Assinatura do Cliente")

    #c.line(330, y, largura - MARGEM_X, y)
    #c.drawString(330, y - 12, "Data")

    # ==================================================
    # FINALIZA
    # ==================================================

    c.showPage()
    c.save()

    return caminho
