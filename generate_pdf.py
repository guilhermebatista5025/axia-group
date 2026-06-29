import os
import sys
import shutil

# Garante a instalação do reportlab se não estiver presente
try:
    import reportlab
except ImportError:
    print("ReportLab não encontrado. Instalando via pip...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

TEXTS = {
    "pt": {
        "cover_title": "CÓDIGO DE CONDUTA E ÉTICA",
        "cover_subtitle": "Diretrizes de Ética, Integridade, Governança e Responsabilidade Corporativa para Colaboradores, Parceiros e Fornecedores.",
        "meta_version": "Versão",
        "meta_date_label": "Data de Publicação",
        "meta_date_val": "Junho de 2026",
        "meta_resp_label": "Responsável",
        "meta_resp_val": "Comitê de Ética e Compliance",
        "toc_title": "SUMÁRIO",
        "toc_intro": "Introdução",
        "toc_p": "Pág.",
        "intro_title": "INTRODUÇÃO",
        "intro_p": "O Código de Conduta da Axia Group expressa nossos compromissos com a ética, a integridade e a responsabilidade em todas as nossas ações e relacionamentos. Ele orienta o comportamento de todos os colaboradores, parceiros, sócios, fornecedores e demais partes interessadas, reforçando os valores que sustentam nossa atuação.",
        "s1_title": "1. Integridade Corporativa & Ambiente de Trabalho",
        "s1_1_title": "1.1. Saúde e Segurança",
        "s1_1_p1": "A Axia Group promove um ambiente de trabalho mais seguro e saudável, adotando práticas que previnem acidentes e protegem a integridade física e mental dos colaboradores. Cumprimos todas as normas regulamentadoras e incentivamos uma cultura de prevenção.",
        "s1_1_p2": "No ambiente de trabalho apresentamos as normas de moralidade (embriaguez, uso de drogas e desavenças). O uso de drogas ilícitas compromete a atuação do profissional e é crime, além de prejudicar a saúde e a vida de seus usuários, comprometendo o ambiente de trabalho e causando risco aos demais.",
        "s1_1_p3": "Será reportado à liderança quaisquer condições inseguras e atos desagradáveis no ambiente de trabalho. Para garantirmos as tratativas e ações necessárias em quaisquer riscos, ocorrências ou situações inseguras, utilizamos o formulário disponível para registrar a ação.",
        "s1_2_title": "1.2. Conflito de Interesse",
        "s1_2_p1": "É responsabilidade de todos os colaboradores evitar situações em que interesses pessoais possam interferir nas decisões profissionais. Todos os interesses pessoais devem compor-se com interesses da Axia Group e vice-versa.",
        "s1_2_p2": "Qualquer situação que configure ou possa configurar conflito de interesse deve ser imediatamente comunicada à liderança ou ao comitê de ética.",
        "s1_3_title": "1.3. Contratação de Familiares e Parentes",
        "s1_3_p1": "A contratação de familiares e parentes é permitida, desde que respeitados critérios de meritocracia e não haja relação direta de subordinação ou influência nas decisões de contratação, promoção ou avaliação de desempenho. A contratação será analisada pela diretoria da empresa desde que não haja grau de parentesco direto gerando influências negativas.",
        "s1_3_p2": "Estes princípios de contratação justa serão aplicados a todos os aspectos profissionais, incluindo remuneração, promoções e transferências. Filhos de colaboradores da Axia Group poderão ter prioridade para vagas de estágio ou de curta duração (temporários de férias), desde que sejam igualmente qualificados em relação aos outros candidatos.",
        "s1_4_title": "1.4. Informações Confidenciais",
        "s1_4_p1": "As relações da Axia Group e seus prestadores de serviços e colaboradores são fundamentadas no princípio da confiança. As informações confidenciais consistem em toda e qualquer informação que não seja de conhecimento público.",
        "s1_4_p2": "Nelas se incluem: segredos comerciais, patentes, planos de negócios, planos de marketing e serviços, pesquisas com consumidores, ideias de processos de fabricação, design, dados contábeis, tokens e senhas, identidade de clientes, base de dados, registros, informações salariais e quaisquer dados financeiros ou bancários.",
        "s1_4_p3": "Adiciona-se ainda a cláusula de 'non compete' (não concorrência) por toda a vigência da relação de prestação de serviços e por até 2 (dois) anos após o término da mesma.",
        "s2_title": "2. Relações Societárias e Conselho Consultivo",
        "s2_p1": "Prezamos pela transparência, equidade, responsabilidade, empatia e convergência de interesse. As deliberações são sempre formalizadas por escrito e em observância à decisão da maioria em assembleia ou reunião corporativa.",
        "s2_p2": "Qualquer divergência será dirimida em respeito ao melhor interesse da Axia Group. Esses princípios garantem uma governança e gestão empresarial íntegra, livre de práticas ilícitas.",
        "s3_title": "3. Relações com Clientes e Fornecedores",
        "s3_p1": "Nossa relação com os fornecedores e parceiros de negócios é pautada por boa-fé, honestidade, ética, transparência e respeito, buscando contribuir positivamente para o desenvolvimento social e econômico das regiões onde atuamos.",
        "s3_sub1": "Brindes e Presentes:",
        "s3_p2": "A troca de presentes e hospitalidades não é incentivada, mas é permitida em contextos corporativos desde que não seja utilizada para influenciar decisões ou obter vantagens. É proibida a aceitação de dinheiro ou equivalentes. A aceitação do presente deve ser comunicada imediatamente ao superior.",
        "s3_sub2": "Interações com Clientes:",
        "s3_p3": "Refeições ou coffee breaks com clientes devem ocorrer de forma transparente e oportuna. Não é permitido o consumo de bebidas alcoólicas ou drogas ilícitas nesses encontros corporativos, visando manter a postura profissional e mitigar riscos.",
        "s4_title": "4. Relações com o Setor Público",
        "s4_p1": "A interação com agentes públicos deve ser conduzida com absoluta integridade e em conformidade com as leis anticorrupção vigentes, especialmente a Lei nº 12.846/2013 (Lei Anticorrupção Brasileira). É vedada qualquer forma de facilitação, suborno ou desvirtuamento ético.",
        "s5_title": "5. Relações com a Concorrência",
        "s5_p1": "Atuamos de forma leal e transparente no mercado. Repudiamos veementemente práticas anticompetivas como a formação de cartéis, concorrência desleal (dumping), espionagem industrial ou difamação comercial. Respeitamos a livre concorrência como valor essencial de mercado.",
        "s6_title": "6. Relações com a Comunidade",
        "s6_p1": "A Axia Group contribui ativamente para o desenvolvimento social das comunidades onde está presente. Incentivamos ações voluntárias, projetos sociais e práticas que promovam a inclusão, diversidade e o bem-estar coletivo, porque acreditamos que a Educação é o único caminho para termos uma sociedade justa.",
        "s7_title": "7. Relações com a Mídia",
        "s7_p1": "A comunicação com a imprensa deve ser feita exclusivamente por porta-vozes autorizados. Não permitimos a utilização de sistemas eletrônicos corporativos para transmitir ou armazenar conteúdos que prejudiquem as atividades de trabalho.",
        "s7_p2": "As redes sociais pessoais ou profissionais não devem ser utilizadas para expor informações privadas e confidenciais da Axia Group ou de seus clientes. Participações em eventos representando a instituição devem ser validadas previamente. Evitamos discussões polêmicas ou debates pessoais em grupos formais de trabalho.",
        "s8_title": "8. Sustentabilidade (ESG)",
        "s8_p1": "Comprometemo-nos com a sustentabilidade em todas as nossas operações, baseando-nos no tripé (ESG):",
        "s8_b1": "Ambiental: Operações em conformidade legal com a legislação ambiental.",
        "s8_b2": "Social: Relações baseadas na confiança, respeito mútuo e compromisso social comunitário.",
        "s8_b3": "Econômica: Foco em alta performance e entrega constante de valor e excelência aos clientes.",
        "s9_title": "9. Proteção de Dados (LGPD)",
        "s9_p1": "Cumprimos rigorosamente a Lei Geral de Proteção de Dados (LGPD - Lei nº 13.709/2018), além das leis antiterrorismo (Lei nº 13.260/2016) e anticorrupção aplicáveis. Os dados obtidos dentro da empresa não podem ser compartilhados com terceiros a qualquer título.",
        "s9_p2": "É dever de todos adotar precauções de segurança: evitar o uso de pen drives ou dispositivos de armazenamento externos não autorizados, utilizar soluções em nuvem homologadas pela empresa, guardar sigilo de senhas e bloquear o computador em caso de ausência. O monitoramento de ambientes virtuais corporativos é expressamente aceito pelos colaboradores.",
        "s10_title": "10. Respeito no Ambiente de Trabalho",
        "s10_p1": "Repudiamos qualquer forma de discriminação baseada em origem, nacionalidade, religião, raça, sexo, idade ou orientação afetiva. Garantimos um ambiente livre de assédio moral, sexual ou pressões de qualquer natureza.",
        "s10_p2": "Praticamos diálogos e não imposições; ouvimos e respeitamos as opiniões alheias. Não são permitidos relacionamentos íntimos nas dependências da empresa durante o horário laboral. Preservamos a imagem pessoal com cuidados com a linguagem nas redes sociais e grupos corporativos.",
        "s11_title": "11. Transparência",
        "s11_p1": "Agimos com clareza e honestidade. A transparência é um valor inegociável. Reconhecemos que erros acontecem; nesses casos, somos transparentes e trazemos o problema imediatamente à liderança para mitigação de danos e aprendizado.",
        "s12_title": "12. Cumprimento e Penalidades",
        "s12_p1": "O cumprimento deste Código é obrigatório para todos. Violações podem resultar em sanções disciplinares, incluindo advertência por escrito, suspensão ou desligamento motivado, além de medidas legais cabíveis.",
        "s13_title": "13. Canal de Ética e Denúncias",
        "s13_p1": "A empresa oferece canais confidenciais para reportar desvios ou condutas em desacordo com nossas normas, com a garantia de não-retaliação e sigilo absoluto das informações prestadas.",
        "s13_p2": "Os relatos podem ser formalizados pelo Canal de Ética oficial, por e-mail corporativo de compliance ou através do formulário eletrônico de reporte na página da Axia Group."
    },
    "es": {
        "cover_title": "CÓDIGO DE CONDUCTA Y ÉTICA",
        "cover_subtitle": "Directrices de Ética, Integridad, Gobernanza y Responsabilidad Corporativa para Colaboradores, Socios y Proveedores.",
        "meta_version": "Versión",
        "meta_date_label": "Fecha de Publicación",
        "meta_date_val": "Junio de 2026",
        "meta_resp_label": "Responsable",
        "meta_resp_val": "Comité de Ética y Cumplimiento",
        "toc_title": "ÍNDICE",
        "toc_intro": "Introducción",
        "toc_p": "Pág.",
        "intro_title": "INTRODUCCIÓN",
        "intro_p": "El Código de Conducta de Axia Group expresa nuestros compromisos con la ética, la integridad y la responsabilidad en todas nuestras acciones y relaciones. Orienta el comportamiento de todos los colaboradores, socios, proveedores y partes interesadas, reforzando los valores que sustentan nuestra actuación.",
        "s1_title": "1. Integridad Corporativa y Entorno Laboral",
        "s1_1_title": "1.1. Salud y Seguridad",
        "s1_1_p1": "Axia Group promueve un ambiente de trabajo seguro y saludable, adoptando prácticas que previenen accidentes y protegen la integridad física y mental de los colaboradores. Cumplimos con todas las normas reglamentarias e incentivamos una cultura de prevención.",
        "s1_1_p2": "En el entorno laboral aplicamos normas de moralidad (embriaguez, uso de drogas y altercados). El uso de drogas ilícitas compromete el desempeño profesional y es un delito, además de perjudicar la salud de los usuarios, afectar el ambiente de trabajo y poner en riesgo a los demás.",
        "s1_1_p3": "Cualquier condición insegura o acto inapropiado en el lugar de trabajo debe ser reportado a la dirección. Para garantizar el tratamiento y las acciones necesarias ante cualquier riesgo o incidente, se utilizará el formulario de registro disponible.",
        "s1_2_title": "1.2. Conflicto de Interés",
        "s1_2_p1": "Es responsabilidad de todos los colaboradores evitar situaciones en las que los intereses personales puedan interferir con las decisiones profesionales. Todos los intereses personales deben estar alineados con los intereses de Axia Group y viceversa.",
        "s1_2_p2": "Cualquier situación que configure o pueda configurar un conflicto de intereses debe comunicarse de inmediato a la dirección o al comité de ética.",
        "s1_3_title": "1.3. Contratación de Familiares y Parientes",
        "s1_3_p1": "La contratación de familiares y parientes está permitida, siempre que se respeten los criterios de meritocracia y no exista una relación directa de subordinación o influencia en las decisiones de contratación, promoción o evaluación de desempeño. La contratación será analizada por la dirección de la empresa siempre que no exista un grado de parentesco directo que genere influencias negativas.",
        "s1_3_p2": "Estos principios de contratación justa se aplicarán a todos los aspectos profesionales, incluyendo remuneración, promociones y traslados. Los hijos de los colaboradores de Axia Group podrán tener prioridad para puestos de prácticas o de corta duración (temporales de vacaciones), siempre que estén igualmente calificados en relación con los demás candidatos.",
        "s1_4_title": "1.4. Información Confidencial",
        "s1_4_p1": "Las relaciones de Axia Group con sus proveedores de servicios y colaboradores se fundamentan en el principio de confianza. La información confidencial consiste en toda aquella información que no sea de conocimiento público.",
        "s1_4_p2": "Esto incluye: secretos comerciales, patentes, planes de negocio, planes de marketing y servicios, investigaciones de consumo, ideas de procesos de fabricación, diseño, datos contables, tokens y contraseñas, identidad de clientes, bases de datos, registros, información salarial y cualquier dato financiero o bancario.",
        "s1_4_p3": "Se añade además la cláusula de 'non compete' (no competencia) durante toda la vigencia de la relación de prestación de servicios y hasta por 2 (dos) años después de la finalización de la misma.",
        "s2_title": "2. Relaciones con Socios/Acionistas y Consejo Consultivo",
        "s2_p1": "Valoramos la transparencia, la equidad, la responsabilidad, la empatía y la convergencia de intereses. Las deliberaciones siempre se formalizan por escrito y en observancia de la decisión de la mayoría en asambleas o reuniones corporativas.",
        "s2_p2": "Cualquier discrepancia se resolverá respetando el mejor interés de Axia Group. Estos principios garantizan una gobernanza y gestión empresarial íntegra, libre de prácticas ilícitas.",
        "s3_title": "3. Relaciones con Clientes y Proveedores",
        "s3_p1": "Nuestra relación con los proveedores y socios comerciales se basa en la buena fe, la honestidad, la ética, la transparencia y el respeto, buscando contribuir positivamente al desarrollo social y económico de las regiones donde operamos.",
        "s3_sub1": "Regalos y Obsequios:",
        "s3_p2": "El intercambio de regalos y hospitalidades no se fomenta, pero está permitido en contextos corporativos siempre que no se utilice para influir en decisiones o conseguir ventajas. Está prohibida la aceptación de dinero o equivalentes. La aceptación del regalo debe comunicarse de inmediato al superior.",
        "s3_sub2": "Interacciones con Clientes:",
        "s3_p3": "Las comidas o coffee breaks con clientes deben realizarse de forma transparente y oportuna. No se permite el consumo de bebidas alcohólicas o drogas ilícitas en estos encuentros corporativos, con el fin de mantener la postura profesional y mitigar riesgos.",
        "s4_title": "4. Relaciones con el Sector Público",
        "s4_p1": "La interacción con agentes públicos debe realizarse con absoluta integridad y de conformidad con las leyes anticorrupción vigentes, especialmente la Ley brasileña Nº 12.846/2013 (Ley Anticorrupción Brasileña). Se prohíbe cualquier forma de facilitación, soborno o desviación ética.",
        "s5_title": "5. Relaciones con la Competencia",
        "s5_p1": "Actuamos de forma leal y transparente en el mercado. Rechazamos enérgicamente las prácticas anticompetitivas como la formación de cárteles, la competencia desleal (dumping), el espionaje industrial o la difamación comercial. Respetamos la libre competencia como un valor esencial del mercado.",
        "s6_title": "6. Relaciones con la Comunidad",
        "s6_p1": "Axia Group contribuye activamente al desarrollo social de las comunidades donde está presente. Fomentamos acciones voluntarias, proyectos sociales y prácticas que promuevan la inclusión, la diversidad y el bienestar colectivo, porque creemos que la Educación es el único camino para lograr una sociedad justa.",
        "s7_title": "7. Relaciones con los Medios",
        "s7_p1": "La comunicación con la prensa debe realizarse exclusivamente a través de voceros autorizados. No permitimos el uso de sistemas electrónicos corporativos para transmitir o almacenar contenidos que perjudiquen las actividades laborales.",
        "s7_p2": "Las redes sociales personales o profesionales no deben utilizarse para exponer información privada y confidencial de Axia Group o de sus clientes. La participación en eventos en representación de la institución debe ser validada previamente. Evitamos discusiones polémicas o debates personales en grupos formales de trabajo.",
        "s8_title": "8. Sostenibilidad (ESG)",
        "s8_p1": "Nos comprometemos con la sostenibilidad en todas nuestras operaciones, basándonos en el trípode (ESG):",
        "s8_b1": "Ambiental: Operaciones en cumplimiento legal con la legislación ambiental.",
        "s8_b2": "Social: Relaciones basadas en la confianza, el respeto mutuo y el compromiso social comunitario.",
        "s8_b3": "Económica: Enfoque en alto rendimiento y entrega constante de valor y excelencia a los clientes.",
        "s9_title": "9. Protección de Datos (LGPD)",
        "s9_p1": "Cumplimos estrictamente con la Ley General de Protección de Datos (LGPD - Ley brasileña Nº 13.709/2018), además de las leyes antiterrorismo (Ley Nº 13.260/2016) y anticorrupción aplicables. Los datos obtenidos dentro de la empresa no se pueden compartir con terceros bajo ningún título.",
        "s9_p2": "Es deber de todos adoptar precauciones de seguridad: evitar el uso de memorias USB o dispositivos de almacenamiento externos no autorizados, utilizar soluciones en la nube aprobadas por la empresa, mantener la confidencialidad de las contraseñas y bloquear el ordenador en caso de ausencia. El monitoreo de los entornos virtuales corporativos es expresamente aceptado por los colaboradores.",
        "s10_title": "10. Respeto en el Entorno Laboral",
        "s10_p1": "Rechazamos cualquier forma de discriminación basada en origen, nacionalidad, religión, raza, sexo, edad u orientación afectiva. Garantizamos un ambiente libre de acoso moral, sexual o presiones de cualquier índole.",
        "s10_p2": "Practicamos el diálogo y no las imposiciones; escuchamos y respetamos las opiniones ajenas. No se permiten relaciones íntimas en las instalaciones de la empresa durante el horario de trabajo. Preservamos la imagen personal cuidando el lenguaje en las redes sociales y grupos corporativos.",
        "s11_title": "11. Transparencia",
        "s11_p1": "Actuamos con claridad y honestidad. La transparencia es un valor innegociable. Reconocemos que se cometen errores; en esos casos, somos transparentes y reportamos el problema de inmediato a la dirección para mitigar daños y aprender.",
        "s12_title": "12. Cumplimiento y Penalidades",
        "s12_p1": "El cumplimiento de este Código es obligatorio para todos. Las violaciones pueden resultar en sanciones disciplinarias, incluyendo advertencias por escrito, suspensión o despido justificado, además de las medidas legales aplicables.",
        "s13_title": "13. Canal de Ética y Denuncias",
        "s13_p1": "La empresa ofrece canales confidenciales para reportar desviaciones o conductas que no estén de acuerdo con nuestras normas, con la garantía de no represalias y confidencialidad absoluta de la información brindada.",
        "s13_p2": "Los informes pueden formalizarse a través del Canal de Ética oficial, por correo electrónico corporativo de cumplimiento o mediante el formulario electrónico de reporte en la página de Axia Group."
    },
    "en": {
        "cover_title": "CODE OF CONDUCT AND ETHICS",
        "cover_subtitle": "Guidelines for Ethics, Integrity, Governance, and Corporate Responsibility for Employees, Partners, and Suppliers.",
        "meta_version": "Version",
        "meta_date_label": "Publication Date",
        "meta_date_val": "June 2026",
        "meta_resp_label": "Responsible",
        "meta_resp_val": "Ethics and Compliance Committee",
        "toc_title": "TABLE OF CONTENTS",
        "toc_intro": "Introduction",
        "toc_p": "Page",
        "intro_title": "INTRODUCTION",
        "intro_p": "The Axia Group Code of Conduct expresses our commitments to ethics, integrity, and responsibility in all our actions and relationships. It guides the behavior of all employees, partners, shareholders, suppliers, and other stakeholders, reinforcing the values that support our operations.",
        "s1_title": "1. Corporate Integrity & Work Environment",
        "s1_1_title": "1.1. Health and Safety",
        "s1_1_p1": "Axia Group promotes a safe and healthy work environment by adopting practices that prevent accidents and protect the physical and mental integrity of employees. We comply with all regulatory standards and encourage a culture of prevention.",
        "s1_1_p2": "In the work environment, we enforce code of conduct standards (prohibiting drunkenness, drug use, and altercations). The use of illegal drugs compromises professional performance, constitutes a crime, damages the user's health, compromises the workplace, and poses risks to others.",
        "s1_1_p3": "Any unsafe conditions or inappropriate behaviors in the workplace must be reported to leadership. To ensure the necessary responses to any risks or incidents, the available reporting form must be used.",
        "s1_2_title": "1.2. Conflict of Interest",
        "s1_2_p1": "It is the responsibility of all employees to avoid situations where personal interests may interfere with professional decisions. All personal interests must align with the interests of Axia Group and vice versa.",
        "s1_2_p2": "Any situation that constitutes or may constitute a conflict of interest must be immediately communicated to leadership or the ethics committee.",
        "s1_3_title": "1.3. Hiring of Relatives",
        "s1_3_p1": "The hiring of family members and relatives is permitted, provided that meritocracy criteria are respected and there is no direct relationship of subordination or influence in decisions regarding hiring, promotion, or performance evaluation. Hiring will be analyzed by the company's board of directors, ensuring that no direct family relationship generates negative influences.",
        "s1_3_p2": "These fair hiring principles will apply to all professional aspects, including compensation, promotions, and transfers. Children of Axia Group employees may have priority for internship or short-term (summer/temporary) positions, provided they are equally qualified compared to other candidates.",
        "s1_4_title": "1.4. Confidential Information",
        "s1_4_p1": "The relations of Axia Group with its service providers and employees are based on the principle of trust. Confidential information consists of any and all information that is not public knowledge.",
        "s1_4_p2": "This includes: trade secrets, patents, business plans, marketing and service plans, consumer research, manufacturing process ideas, design, accounting data, tokens and passwords, customer identities, databases, records, salary information, and any financial or banking data.",
        "s1_4_p3": "A 'non-compete' clause is also added for the entire duration of the service contract and for up to 2 (two) years after its termination.",
        "s2_title": "2. Corporate Relations and Advisory Board",
        "s2_p1": "We value transparency, equity, responsibility, empathy, and convergence of interests. Deliberations are always formalized in writing and in compliance with majority decisions in assemblies or corporate meetings.",
        "s2_p2": "Any discrepancy will be resolved in accordance with the best interests of Axia Group. These principles ensure integral corporate governance and management, free from illegal practices.",
        "s3_title": "3. Relations with Customers and Suppliers",
        "s3_p1": "Our relationship with suppliers and business partners is guided by good faith, honesty, ethics, transparency, and respect, aiming to contribute positively to the social and economic development of the regions where we operate.",
        "s3_sub1": "Gifts and Favors:",
        "s3_p2": "The exchange of gifts and hospitalities is not encouraged, but is permitted in corporate contexts as long as it is not used to influence decisions or gain advantages. Accepting money or its equivalent is strictly prohibited. The acceptance of any gift must be immediately reported to a supervisor.",
        "s3_sub2": "Interactions with Customers:",
        "s3_p3": "Meals or coffee breaks with clients must occur transparently and appropriately. The consumption of alcohol or illegal drugs is not permitted during these corporate meetings, in order to maintain a professional stance and mitigate risks.",
        "s4_title": "4. Relations with the Public Sector",
        "s4_p1": "Interaction with public officials must be conducted with absolute integrity and in compliance with applicable anti-corruption laws, especially Law No. 12,846/2013 (Brazilian Anti-Corruption Law). Any form of facilitation, bribery, or ethical deviation is strictly prohibited.",
        "s5_title": "5. Relations with Competitors",
        "s5_p1": "We act fairly and transparently in the market. We strongly reject anti-competitive practices such as cartels, dumping, industrial espionage, or commercial defamation. We respect free competition as an essential market value.",
        "s6_title": "6. Relations with the Community",
        "s6_p1": "Axia Group actively contributes to the social development of the communities where it operates. We encourage volunteering, social projects, and practices that promote inclusion, diversity, and collective well-being, because we believe that Education is the only way to build a fair society.",
        "s7_title": "7. Relations with the Media",
        "s7_p1": "Communication with the press must be conducted exclusively by authorized spokespersons. We do not permit the use of corporate electronic systems to transmit or store content that interferes with work activities.",
        "s7_p2": "Personal or professional social media accounts must not be used to expose private and confidential information of Axia Group or its clients. Participation in events representing the institution must be validated in advance. We avoid controversial discussions or personal debates in formal work groups.",
        "s8_title": "8. Sustainability (ESG)",
        "s8_p1": "We commit to sustainability in all our operations, based on the triple bottom line (ESG):",
        "s8_b1": "Environmental: Operations in legal compliance with environmental legislation.",
        "s8_b2": "Social: Relationships based on trust, mutual respect, and community social commitment.",
        "s8_b3": "Economic: Focus on high performance and the consistent delivery of value and excellence to clients.",
        "s9_title": "9. Data Protection (LGPD)",
        "s9_p1": "We strictly comply with the General Data Protection Regulation (LGPD - Law No. 13,709/2018), as well as applicable anti-terrorism (Law No. 13,260/2016) and anti-corruption laws. Data obtained within the company cannot be shared with third parties under any circumstances.",
        "s9_p2": "It is everyone's duty to adopt security precautions: avoid using unauthorized flash drives or external storage devices, use cloud solutions approved by the company, maintain password confidentiality, and lock the computer when away. The monitoring of corporate virtual environments is expressly accepted by employees.",
        "s10_title": "10. Respect in the Work Environment",
        "s10_p1": "We reject any form of discrimination based on origin, nationality, religion, race, sex, age, or sexual orientation. We guarantee an environment free from moral harassment, sexual harassment, or pressure of any kind.",
        "s10_p2": "We practice dialogue, not imposition; we listen to and respect the opinions of others. Intimate relationships are not permitted on company premises during working hours. We preserve our personal image by caring for our language on social networks and corporate groups.",
        "s11_title": "11. Transparency",
        "s11_p1": "We act with clarity and honesty. Transparency is a non-negotiable value. We recognize that mistakes happen; in these cases, we are transparent and bring the issue immediately to leadership to mitigate damage and promote learning.",
        "s12_title": "12. Compliance and Penalties",
        "s12_p1": "Compliance with this Code is mandatory for all. Violations can lead to disciplinary actions, including written warnings, suspension, or dismissal for cause, in addition to appropriate legal actions.",
        "s13_title": "13. Ethics and Whistleblowing Channel",
        "s13_p1": "The company offers confidential channels to report deviations or behaviors inconsistent with our standards, guaranteeing non-retaliation and absolute confidentiality of the information provided.",
        "s13_p2": "Reports can be formalized through the official Ethics Channel, corporate compliance email, or via the electronic reporting form on the Axia Group website."
    }
}

def draw_cover_background(canvas, doc, lang):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#0a1d3a"))
    canvas.rect(0, 0, 612, 792, fill=1, stroke=0) # Fundo azul escuro da capa
    canvas.setFillColor(colors.HexColor("#008f7a"))
    canvas.rect(0, 0, 18, 792, fill=1, stroke=0) # Barra vertical verde-água à esquerda
    
    logo_path = os.path.join("assets", "images", "logo", "logo.png")
    if os.path.exists(logo_path):
        canvas.drawImage(logo_path, 44, 646, width=180, height=122, mask='auto')
    canvas.restoreState()

def get_numbered_canvas_class(lang):
    class NumberedCanvas(canvas.Canvas):
        def __init__(self, *args, **kwargs):
            super(NumberedCanvas, self).__init__(*args, **kwargs)
            self._saved_page_states = []
            self.lang = lang

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
            
            primary_color = colors.HexColor("#0a1d3a")
            accent_color = colors.HexColor("#008f7a")
            grey_color = colors.HexColor("#718096")
            
            # Cabeçalho
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(primary_color)
            self.drawString(54, 750, "AXIA GROUP | ACADEMY")
            self.setFont("Helvetica", 8)
            self.setFillColor(grey_color)
            
            header_right_text = {
                "pt": "Código de Conduta e Ética",
                "es": "Código de Conducta y Ética",
                "en": "Code of Conduct and Ethics"
            }.get(self.lang, "Código de Conduta e Ética")
            
            self.drawRightString(558, 750, header_right_text)
            
            # Linha do Cabeçalho
            self.setStrokeColor(accent_color)
            self.setLineWidth(1)
            self.line(54, 742, 558, 742)
            
            # Rodapé
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.line(54, 55, 558, 55)
            
            self.setFont("Helvetica", 8)
            self.setFillColor(grey_color)
            
            copyright_text = {
                "pt": "© 2026 AXIA GROUP. Todos os direitos reservados.",
                "es": "© 2026 AXIA GROUP. Todos los derechos reservados.",
                "en": "© 2026 AXIA GROUP. All rights reserved."
            }.get(self.lang, "© 2026 AXIA GROUP. Todos os direitos reservados.")
            
            page_template = {
                "pt": "Página {} de {}",
                "es": "Página {} de {}",
                "en": "Page {} of {}"
            }.get(self.lang, "Página {} de {}")
            
            self.drawString(54, 40, copyright_text)
            self.drawRightString(558, 40, page_template.format(self._pageNumber, page_count))
            
            self.restoreState()

    return NumberedCanvas

def create_conduct_pdf(lang):
    pdf_dir = "pdf"
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, f"codigo_de_conduta_{lang}.pdf")
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    primary = colors.HexColor("#0a1d3a")
    accent = colors.HexColor("#008f7a")
    text_color = colors.HexColor("#2d3748")
    
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=32,
        leading=38,
        textColor=colors.white,
        alignment=0,
        spaceAfter=15
    )
    
    cover_subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=20,
        textColor=colors.HexColor("#e2e8f0"),
        alignment=0,
        spaceAfter=30
    )
    
    cover_meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=16,
        textColor=colors.HexColor("#94a3b8")
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=16,
        textColor=text_color,
        spaceAfter=16
    )
    
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary,
        spaceBefore=24,
        spaceAfter=16,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=accent,
        spaceBefore=20,
        spaceAfter=12,
        keepWithNext=True
    )
    
    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=primary,
        spaceBefore=14,
        spaceAfter=10,
        keepWithNext=True
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=body_style,
        leftIndent=20,
        bulletIndent=10,
        spaceAfter=10
    )
    
    story = []
    t = TEXTS[lang]
    
    # ==========================================
    # CAPA (Página 1)
    # ==========================================
    story.append(Spacer(1, 260))
    story.append(Paragraph(t["cover_title"], cover_title_style))
    
    decorative_line = Table([[""]], colWidths=[504], rowHeights=[4])
    decorative_line.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), accent),
        ('PADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(decorative_line)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph(t["cover_subtitle"], cover_subtitle_style))
    story.append(Spacer(1, 170))
    
    meta_text = f"<b>{t['meta_version']}:</b> 2026.1<br/><b>{t['meta_date_label']}:</b> {t['meta_date_val']}<br/><b>{t['meta_resp_label']}:</b> {t['meta_resp_val']}"
    story.append(Paragraph(meta_text, cover_meta_style))
    story.append(PageBreak())
    
    # ==========================================
    # SUMÁRIO (Página 2)
    # ==========================================
    story.append(Paragraph(t["toc_title"], h1_style))
    story.append(Spacer(1, 15))
    
    toc_data = [
        [t["toc_intro"], ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 3"],
        [t["s1_title"], "", ""],
        [f"   {t['s1_1_title']}", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 3"],
        [f"   {t['s1_2_title']}", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 3"],
        [f"   {t['s1_3_title']}", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 4"],
        [f"   {t['s1_4_title']}", ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 4"],
        [t["s2_title"], ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 4"],
        [t["s3_title"], ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 5"],
        [t["s4_title"], ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 5"],
        [t["s5_title"], ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 5"],
        [t["s6_title"], ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 5"],
        [t["s7_title"], ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 6"],
        [t["s8_title"], ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 6"],
        [t["s9_title"], ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 6"],
        [t["s10_title"], ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 7"],
        [t["s11_title"], ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 7"],
        [t["s12_title"], ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 7"],
        [t["s13_title"], ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", f"{t['toc_p']} 7"]
    ]
    
    toc_table_data = []
    for item in toc_data:
        if item[1] == "" and item[2] == "":
            toc_table_data.append([
                Paragraph(f"<b>{item[0]}</b>", ParagraphStyle('TOCCat', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, textColor=primary)),
                "", ""
            ])
        else:
            toc_table_data.append([
                Paragraph(item[0], ParagraphStyle('TOCItem', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=text_color)),
                Paragraph(item[1], ParagraphStyle('TOCDot', parent=styles['Normal'], fontName='Helvetica', fontSize=8, textColor=colors.HexColor("#a0aec0"), alignment=1)),
                Paragraph(item[2], ParagraphStyle('TOCPage', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=primary, alignment=2))
            ])
            
    toc_table = Table(toc_table_data, colWidths=[240, 214, 50], rowHeights=[26]*len(toc_data))
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
    story.append(Paragraph(t["intro_title"], h1_style))
    story.append(Paragraph(t["intro_p"], body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph(t["s1_title"], h1_style))
    
    story.append(Paragraph(t["s1_1_title"], h2_style))
    story.append(Paragraph(t["s1_1_p1"], body_style))
    story.append(Paragraph(t["s1_1_p2"], body_style))
    story.append(Paragraph(t["s1_1_p3"], body_style))
    
    story.append(Paragraph(t["s1_2_title"], h2_style))
    story.append(Paragraph(t["s1_2_p1"], body_style))
    story.append(Paragraph(t["s1_2_p2"], body_style))
    
    story.append(PageBreak())
    
    # ==========================================
    # SEÇÃO 1 (Continuação) & SEÇÃO 2 (Página 4)
    # ==========================================
    story.append(Paragraph(t["s1_3_title"], h2_style))
    story.append(Paragraph(t["s1_3_p1"], body_style))
    story.append(Paragraph(t["s1_3_p2"], body_style))
    
    story.append(Paragraph(t["s1_4_title"], h2_style))
    story.append(Paragraph(t["s1_4_p1"], body_style))
    story.append(Paragraph(t["s1_4_p2"], body_style))
    story.append(Paragraph(t["s1_4_p3"], body_style))
    
    story.append(Paragraph(t["s2_title"], h1_style))
    story.append(Paragraph(t["s2_p1"], body_style))
    story.append(Paragraph(t["s2_p2"], body_style))
    
    story.append(PageBreak())
    
    # ==========================================
    # SEÇÕES 3, 4, 5, 6 (Página 5)
    # ==========================================
    story.append(Paragraph(t["s3_title"], h1_style))
    story.append(Paragraph(t["s3_p1"], body_style))
    
    story.append(Paragraph(f"<b>{t['s3_sub1']}</b>", h3_style))
    story.append(Paragraph(t["s3_p2"], body_style))
    
    story.append(Paragraph(f"<b>{t['s3_sub2']}</b>", h3_style))
    story.append(Paragraph(t["s3_p3"], body_style))
    
    story.append(Paragraph(t["s4_title"], h1_style))
    story.append(Paragraph(t["s4_p1"], body_style))
    
    story.append(Paragraph(t["s5_title"], h1_style))
    story.append(Paragraph(t["s5_p1"], body_style))
    
    story.append(Paragraph(t["s6_title"], h1_style))
    story.append(Paragraph(t["s6_p1"], body_style))
    
    story.append(PageBreak())
    
    # ==========================================
    # SEÇÕES 7, 8, 9 (Página 6)
    # ==========================================
    story.append(Paragraph(t["s7_title"], h1_style))
    story.append(Paragraph(t["s7_p1"], body_style))
    story.append(Paragraph(t["s7_p2"], body_style))
    
    story.append(Paragraph(t["s8_title"], h1_style))
    story.append(Paragraph(t["s8_p1"], body_style))
    story.append(Paragraph(f"&bull; <b>{t['s8_b1'].split(':', 1)[0]}:</b>{t['s8_b1'].split(':', 1)[1]}", bullet_style))
    story.append(Paragraph(f"&bull; <b>{t['s8_b2'].split(':', 1)[0]}:</b>{t['s8_b2'].split(':', 1)[1]}", bullet_style))
    story.append(Paragraph(f"&bull; <b>{t['s8_b3'].split(':', 1)[0]}:</b>{t['s8_b3'].split(':', 1)[1]}", bullet_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph(t["s9_title"], h1_style))
    story.append(Paragraph(t["s9_p1"], body_style))
    story.append(Paragraph(t["s9_p2"], body_style))
    
    story.append(PageBreak())
    
    # ==========================================
    # SEÇÕES 10, 11, 12, 13 (Página 7)
    # ==========================================
    story.append(Paragraph(t["s10_title"], h1_style))
    story.append(Paragraph(t["s10_p1"], body_style))
    story.append(Paragraph(t["s10_p2"], body_style))
    
    story.append(Paragraph(t["s11_title"], h1_style))
    story.append(Paragraph(t["s11_p1"], body_style))
    
    story.append(Paragraph(t["s12_title"], h1_style))
    story.append(Paragraph(t["s12_p1"], body_style))
    
    story.append(Paragraph(t["s13_title"], h1_style))
    story.append(Paragraph(t["s13_p1"], body_style))
    story.append(Paragraph(t["s13_p2"], body_style))
    
    doc.build(story, onFirstPage=lambda c, d: draw_cover_background(c, d, lang), canvasmaker=get_numbered_canvas_class(lang))
    print(f"PDF [{lang}] gerado com sucesso em: {pdf_path}")

def generate_all_pdfs():
    pdf_dir = "pdf"
    for lang in ["pt", "es", "en"]:
        create_conduct_pdf(lang)
    
    # Copia o de português como o padrão "codigo_de_conduta.pdf"
    src = os.path.join(pdf_dir, "codigo_de_conduta_pt.pdf")
    dest = os.path.join(pdf_dir, "codigo_de_conduta.pdf")
    shutil.copyfile(src, dest)
    print("Copia do PDF padrão criada em:", dest)

if __name__ == "__main__":
    generate_all_pdfs()
