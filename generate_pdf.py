import os
import sys

# Garante a instalação do reportlab se não estiver presente
try:
    import reportlab
except ImportError:
    print("ReportLab não encontrado. Instalando via pip...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def draw_cover_background(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#0a1d3a"))
    canvas.rect(0, 0, 612, 792, fill=1, stroke=0) # Fundo azul escuro da capa
    canvas.setFillColor(colors.HexColor("#008f7a"))
    canvas.rect(0, 0, 18, 792, fill=1, stroke=0) # Barra vertical verde-água à esquerda
    
    # Desenha a logo diretamente no Canvas para controle fino de posicionamento (deslocado para cima e para a esquerda)
    logo_path = os.path.join("assets", "images", "logo", "logo.png")
    if os.path.exists(logo_path):
        # x = 54 (margem padrão) - 10 (deslocado para esquerda) = 44
        # y = 576 (base original) + 70 (margin-top de -70px) = 646
        canvas.drawImage(logo_path, 44, 646, width=180, height=122, mask='auto')
    canvas.restoreState()

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        # Ignora a capa (Página 1)
        if self._pageNumber == 1:
            return

        self.saveState()
        
        # Cores da AXIA
        primary_color = colors.HexColor("#0a1d3a")
        accent_color = colors.HexColor("#008f7a")
        grey_color = colors.HexColor("#718096")
        
        # Cabeçalho
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(primary_color)
        self.drawString(54, 750, "AXIA GROUP | ACADEMY")
        self.setFont("Helvetica", 8)
        self.setFillColor(grey_color)
        self.drawRightString(558, 750, "Código de Conduta e Ética")
        
        # Linha do Cabeçalho
        self.setStrokeColor(accent_color)
        self.setLineWidth(1)
        self.line(54, 742, 558, 742)
        
        # Rodapé
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.line(54, 55, 558, 55)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(grey_color)
        self.drawString(54, 40, "© 2026 AXIA GROUP. Todos os direitos reservados.")
        self.drawRightString(558, 40, f"Página {self._pageNumber} de {page_count}")
        
        self.restoreState()

def create_conduct_pdf():
    pdf_dir = "pdf"
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, "codigo_de_conduta.pdf")
    
    # Configurações do documento (margens de 0.75 in / 54 pt)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    # Cores personalizadas
    primary = colors.HexColor("#0a1d3a")
    accent = colors.HexColor("#008f7a")
    text_color = colors.HexColor("#2d3748")
    
    # Novos estilos de parágrafo para a Capa (Fundo Escuro)
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        textColor=colors.white, # Branco para contraste com fundo azul escuro
        alignment=0,
        spaceAfter=15
    )
    
    cover_subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=20,
        textColor=colors.HexColor("#e2e8f0"), # Cinza claro
        alignment=0,
        spaceAfter=30
    )

    cover_meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=16,
        textColor=colors.HexColor("#94a3b8") # Slate grey
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=16,
        textColor=text_color,
        spaceAfter=16 # Aumentado de 12 para 16 para dar mais espaço entre parágrafos
    )
    
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary,
        spaceBefore=24, # Aumentado de 18 para 24 para espaçar melhor do conteúdo anterior
        spaceAfter=16,  # Aumentado de 12 para 16 para afastar do subtítulo/texto abaixo
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=accent,
        spaceBefore=20, # Aumentado de 14 para 20
        spaceAfter=12,  # Aumentado de 8 para 12
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=primary,
        spaceBefore=14, # Aumentado de 10 para 14
        spaceAfter=10,  # Aumentado de 6 para 10
        keepWithNext=True
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=body_style,
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=10 # Aumentado de 6 para 10
    )
    
    story = []
    
    # ==========================================
    # CAPA (Página 1)
    # ==========================================
    # Espaço reservado para a logo desenhada no Canvas (deslocada) e para centralização vertical
    story.append(Spacer(1, 260))
    
    # Título Principal
    story.append(Paragraph("CÓDIGO DE CONDUTA E ÉTICA", cover_title_style))
    
    # Linha Decorativa Teal
    decorative_line = Table([[""]], colWidths=[504], rowHeights=[4])
    decorative_line.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), accent),
        ('PADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(decorative_line)
    story.append(Spacer(1, 20))
    
    # Subtítulo da Capa
    story.append(Paragraph("Diretrizes de Ética, Integridade, Governança e Responsabilidade Corporativa para Colaboradores, Parceiros e Fornecedores.", cover_subtitle_style))
    
    # Espaçamento para o bloco de metadados ficar mais abaixo (puxado 50px a mais para baixo e balanceando a centralização)
    story.append(Spacer(1, 170))
    
    # Info de Versão e Data
    story.append(Paragraph("<b>Versão:</b> 2026.1<br/><b>Data de Publicação:</b> Junho de 2026<br/><b>Responsável:</b> Comitê de Ética e Compliance", cover_meta_style))
    
    story.append(PageBreak())
    
    # ==========================================
    # SUMÁRIO (Página 2)
    # ==========================================
    story.append(Paragraph("SUMÁRIO", h1_style))
    story.append(Spacer(1, 15))
    
    # Criação do Sumário Formatado
    toc_data = [
        ["Introdução", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 3"],
        ["1. Integridade Corporativa & Ambiente de Trabalho", "", ""],
        ["   1.1. Saúde e Segurança", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 3"],
        ["   1.2. Conflito de Interesse", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 3"],
        ["   1.3. Contratação de Familiares e Parentes", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 4"],
        ["   1.4. Informações Confidenciais", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 4"],
        ["2. Relações Societárias e Conselho Consultivo", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 4"],
        ["3. Relações com Clientes e Fornecedores", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 5"],
        ["4. Relações com o Setor Público", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 5"],
        ["5. Relações com a Concorrência", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 5"],
        ["6. Relações com a Comunidade", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 5"],
        ["7. Relações com a Mídia", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 6"],
        ["8. Sustentabilidade (ESG)", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 6"],
        ["9. Proteção de Dados (LGPD)", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 6"],
        ["10. Respeito no Ambiente de Trabalho", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 7"],
        ["11. Transparência", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 7"],
        ["12. Cumprimento e Penalidades", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 7"],
        ["13. Canal de Ética e Denúncias", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", "Pág. 7"]
    ]
    
    toc_table_data = []
    for item in toc_data:
        if item[1] == "" and item[2] == "":
            # Título de Categoria (negrito)
            toc_table_data.append([
                Paragraph(f"<b>{item[0]}</b>", ParagraphStyle('TOCCat', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, textColor=primary)),
                "", ""
            ])
        else:
            # Item normal
            toc_table_data.append([
                Paragraph(item[0], ParagraphStyle('TOCItem', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=text_color)),
                Paragraph(item[1], ParagraphStyle('TOCDot', parent=styles['Normal'], fontName='Helvetica', fontSize=8, textColor=colors.HexColor("#a0aec0"), alignment=1)),
                Paragraph(item[2], ParagraphStyle('TOCPage', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=primary, alignment=2))
            ])
            
    toc_table = Table(toc_table_data, colWidths=[240, 214, 50], rowHeights=[26]*len(toc_data)) # Aumentado de 20 para 26 para espaçar as linhas do sumário
    toc_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    
    story.append(toc_table)
    story.append(PageBreak())
    
    # ==========================================
    # INTRODUÇÃO & SEÇÃO 1 (Página 3)
    # ==========================================
    story.append(Paragraph("INTRODUÇÃO", h1_style))
    story.append(Paragraph(
        "O Código de Conduta da Axia Group expressa nossos compromissos com a ética, a integridade e a responsabilidade em todas as nossas ações e relacionamentos. Ele orienta o comportamento de todos os colaboradores, parceiros, sócios, fornecedores e demais partes interessadas, reforçando os valores que sustentam nossa atuação.",
        body_style
    ))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("1. Integridade Corporativa & Ambiente de Trabalho", h1_style))
    
    story.append(Paragraph("1.1. Saúde e Segurança", h2_style))
    story.append(Paragraph(
        "A Axia Group promove um ambiente de trabalho mais seguro e saudável, adotando práticas que previnem acidentes e protegem a integridade física e mental dos colaboradores. Cumprimos todas as normas regulamentadoras e incentivamos uma cultura de prevenção.",
        body_style
    ))
    story.append(Paragraph(
        "No ambiente de trabalho apresentamos as normas de moralidade (embriaguez, uso de drogas e desavenças). O uso de drogas ilícitas compromete a atuação do profissional e é crime, além de prejudicar a saúde e a vida de seus usuários, comprometendo o ambiente de trabalho e causando risco aos demais.",
        body_style
    ))
    story.append(Paragraph(
        "Será reportado à liderança quaisquer condições inseguras e atos desagradáveis no ambiente de trabalho. Para garantirmos as tratativas e ações necessárias em quaisquer riscos, ocorrências ou situações inseguras, utilizamos o formulário disponível para registrar a ação.",
        body_style
    ))
    
    story.append(Paragraph("1.2. Conflito de Interesse", h2_style))
    story.append(Paragraph(
        "É responsabilidade de todos os colaboradores evitar situações em que interesses pessoais possam interferir nas decisões profissionais. Todos os interesses pessoais devem compor-se com interesses da Axia Group e vice-versa.",
        body_style
    ))
    story.append(Paragraph(
        "Qualquer situação que configure ou possa configurar conflito de interesse deve ser imediatamente comunicada à liderança ou ao comitê de ética.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # ==========================================
    # SEÇÃO 1 (Continuação) & SEÇÃO 2 (Página 4)
    # ==========================================
    story.append(Paragraph("1.3. Contratação de Familiares e Parentes", h2_style))
    story.append(Paragraph(
        "A contratação de familiares e parentes é permitida, desde que respeitados critérios de meritocracia e não haja relação direta de subordinação ou influência nas decisões de contratação, promoção ou avaliação de desempenho. A contratação será analisada pela diretoria da empresa desde que não haja grau de parentesco direto gerando influências negativas.",
        body_style
    ))
    story.append(Paragraph(
        "Estes princípios de contratação justa serão aplicados a todos os aspectos profissionais, incluindo remuneração, promoções e transferências. Filhos de colaboradores da Axia Group poderão ter prioridade para vagas de estágio ou de curta duração (temporários de férias), desde que sejam igualmente qualificados em relação aos outros candidatos.",
        body_style
    ))
    
    story.append(Paragraph("1.4. Informações Confidenciais", h2_style))
    story.append(Paragraph(
        "As relações da Axia Group e seus prestadores de serviços e colaboradores são fundamentadas no princípio da confiança. As informações confidenciais consistem em toda e qualquer informação que não seja de conhecimento público.",
        body_style
    ))
    story.append(Paragraph(
        "Nelas se incluem: segredos comerciais, patentes, planos de negócios, planos de marketing e serviços, pesquisas com consumidores, ideias de processos de fabricação, design, dados contábeis, tokens e senhas, identidade de clientes, base de dados, registros, informações salariais e quaisquer dados financeiros ou bancários.",
        body_style
    ))
    story.append(Paragraph(
        "Adiciona-se ainda a cláusula de \"non compete\" (não concorrência) por toda a vigência da relação de prestação de serviços e por até 2 (dois) anos após o término da mesma.",
        body_style
    ))
    
    story.append(Paragraph("2. Relações Societárias e Conselho Consultivo", h1_style))
    story.append(Paragraph(
        "Prezamos pela transparência, equidade, responsabilidade, empatia e convergência de interesse. As deliberações são sempre formalizadas por escrito e em observância à decisão da maioria em assembleia ou reunião corporativa.",
        body_style
    ))
    story.append(Paragraph(
        "Qualquer divergência será dirimida em respeito ao melhor interesse da Axia Group. Esses princípios garantem uma governança e gestão empresarial íntegra, livre de práticas ilícitas.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # ==========================================
    # SEÇÕES 3, 4, 5, 6 (Página 5)
    # ==========================================
    story.append(Paragraph("3. Relações com Clientes e Fornecedores", h1_style))
    story.append(Paragraph(
        "Nossa relação com os fornecedores e parceiros de negócios é pautada por boa-fé, honestidade, ética, transparência e respeito, buscando contribuir positivamente para o desenvolvimento social e econômico das regiões onde atuamos.",
        body_style
    ))
    story.append(Paragraph("<b>Brindes e Presentes:</b>", h3_style))
    story.append(Paragraph(
        "A troca de presentes e hospitalidades não é incentivada, mas é permitida em contextos corporativos desde que não seja utilizada para influenciar decisões ou obter vantagens. É proibida a aceitação de dinheiro ou equivalentes. A aceitação do presente deve ser comunicada imediatamente ao superior.",
        body_style
    ))
    story.append(Paragraph("<b>Interações com Clientes:</b>", h3_style))
    story.append(Paragraph(
        "Refeições ou coffee breaks com clientes devem ocorrer de forma transparente e oportuna. Não é permitido o consumo de bebidas alcoólicas ou drogas ilícitas nesses encontros corporativos, visando manter a postura profissional e mitigar riscos.",
        body_style
    ))
    
    story.append(Paragraph("4. Relações com o Setor Público", h1_style))
    story.append(Paragraph(
        "A interação com agentes públicos deve ser conduzida com absoluta integridade e em conformidade com as leis anticorrupção vigentes, especialmente a Lei nº 12.846/2013 (Lei Anticorrupção Brasileira). É vedada qualquer forma de facilitação, suborno ou desvirtuamento ético.",
        body_style
    ))
    
    story.append(Paragraph("5. Relações com a Concorrência", h1_style))
    story.append(Paragraph(
        "Atuamos de forma leal e transparente no mercado. Repudiamos veementemente práticas anticompetivas como a formação de cartéis, concorrência desleal (dumping), espionagem industrial ou difamação comercial. Respeitamos a livre concorrência como valor essencial de mercado.",
        body_style
    ))
    
    story.append(Paragraph("6. Relações com a Comunidade", h1_style))
    story.append(Paragraph(
        "A Axia Group contribui ativamente para o desenvolvimento social das comunidades onde está presente. Incentivamos ações voluntárias, projetos sociais e práticas que promovam a inclusão, diversidade e o bem-estar coletivo, porque acreditamos que a Educação é o único caminho para termos uma sociedade justa.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # ==========================================
    # SEÇÕES 7, 8, 9 (Página 6)
    # ==========================================
    story.append(Paragraph("7. Relações com a Mídia", h1_style))
    story.append(Paragraph(
        "A comunicação com a imprensa deve ser feita exclusivamente por porta-vozes autorizados. Não permitimos a utilização de sistemas eletrônicos corporativos para transmitir ou armazenar conteúdos que prejudiquem as atividades de trabalho.",
        body_style
    ))
    story.append(Paragraph(
        "As redes sociais pessoais ou profissionais não devem ser utilizadas para expor informações privadas e confidenciais da Axia Group ou de seus clientes. Participações em eventos representando a instituição devem ser validadas previamente. Evitamos discussões polêmicas ou debates pessoais em grupos formais de trabalho.",
        body_style
    ))
    
    story.append(Paragraph("8. Sustentabilidade (ESG)", h1_style))
    story.append(Paragraph(
        "Comprometemo-nos com a sustentabilidade em todas as nossas operações, baseando-nos no tripé (ESG):",
        body_style
    ))
    story.append(Paragraph("• <b>Ambiental:</b> Operações em conformidade legal com a legislação ambiental.", bullet_style))
    story.append(Paragraph("• <b>Social:</b> Relações baseadas na confiança, respeito mútuo e compromisso social comunitário.", bullet_style))
    story.append(Paragraph("• <b>Econômica:</b> Foco em alta performance e entrega constante de valor e excelência aos clientes.", bullet_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("9. Proteção de Dados (LGPD)", h1_style))
    story.append(Paragraph(
        "Cumprimos rigorosamente a Lei Geral de Proteção de Dados (LGPD - Lei nº 13.709/2018), além das leis antiterrorismo (Lei nº 13.260/2016) e anticorrupção aplicáveis. Os dados obtidos dentro da empresa não podem ser compartilhados com terceiros a qualquer título.",
        body_style
    ))
    story.append(Paragraph(
        "É dever de todos adotar precauções de segurança: evitar o uso de pen drives ou dispositivos de armazenamento externos não autorizados, utilizar soluções em nuvem homologadas pela empresa, guardar sigilo de senhas e bloquear o computador em caso de ausência. O monitoramento de ambientes virtuais corporativos é expressamente aceito pelos colaboradores.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # ==========================================
    # SEÇÕES 10, 11, 12, 13 (Página 7)
    # ==========================================
    story.append(Paragraph("10. Respeito no Ambiente de Trabalho", h1_style))
    story.append(Paragraph(
        "Repudiamos qualquer forma de discriminação baseada em origem, nacionalidade, religião, raça, sexo, idade ou orientação afetiva. Garantimos um ambiente livre de assédio moral, sexual ou pressões de qualquer natureza.",
        body_style
    ))
    story.append(Paragraph(
        "Praticamos diálogos e não imposições; ouvimos e respeitamos as opiniões alheias. Não são permitidos relacionamentos íntimos nas dependências da empresa durante o horário laboral. Preservamos a imagem pessoal com cuidados com a linguagem nas redes sociais e grupos corporativos.",
        body_style
    ))
    
    story.append(Paragraph("11. Transparência", h1_style))
    story.append(Paragraph(
        "Agimos com clareza e honestidade. A transparência é um valor inegociável. Reconhecemos que erros acontecem; nesses casos, somos transparentes e trazemos o problema imediatamente à liderança para mitigação de danos e aprendizado.",
        body_style
    ))
    
    story.append(Paragraph("12. Cumprimento e Penalidades", h1_style))
    story.append(Paragraph(
        "O cumprimento deste Código é obrigatório para todos. Violações podem resultar em sanções disciplinares, incluindo advertência por escrito, suspensão ou desligamento motivado, além de medidas legais cabíveis.",
        body_style
    ))
    
    story.append(Paragraph("13. Canal de Ética e Denúncias", h1_style))
    story.append(Paragraph(
        "A empresa oferece canais confidenciais para reportar desvios ou condutas em desacordo com nossas normas, com a garantia de não-retaliação e sigilo absoluto das informações prestadas.",
        body_style
    ))
    story.append(Paragraph(
        "Os relatos podem ser formalizados pelo Canal de Ética oficial, por e-mail corporativo de compliance ou através do formulário eletrônico de reporte na página da Axia Group.",
        body_style
    ))
    
    # Gera o PDF usando o NumberedCanvas personalizado e o callback de fundo da capa
    doc.build(story, onFirstPage=draw_cover_background, canvasmaker=NumberedCanvas)
    print("PDF gerado com sucesso em:", pdf_path)

if __name__ == "__main__":
    create_conduct_pdf()
