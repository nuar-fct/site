// Dicionário de traduções para todas as páginas (index, about, projects, activities)
const dictionary = {
    // ─── NAVBAR & MENU ───
    "Início": "Home",
    "Sobre Nós": "About Us",
    "Projetos": "Projects",
    "Ver Todos": "See All",
    "Atividades": "Activities",
    "Programa Educativo": "Educational Program",
    "Contactos": "Contacts",

    // ─── HERO & CABEÇALHO ───
    "Termos de Serviço": "Terms of Service",
    "Última atualização: 06/02/2026": "Last updated: 06/02/2026",

    // ─── CONTEÚDO PRINCIPAL ───
    "O Núcleo de Aeroespacial da Universidade NOVA de Lisboa, NuAr está inserido na Associação dos Estudantes da Faculdade de Ciências e Tecnologia da Universidade NOVA de Lisboa, AEFCT. Enquanto entidade responsável pelo website nuarfct.com, respeitamos a tua privacidade e protegemos os teus dados pessoais em conformidade com o Regulamento (UE) 2016/679 do Parlamento Europeu e do Conselho, de 27 de abril de 2016 (“RGPD”) e demais legislação aplicável.":
        "The Aerospace Student Organization of NOVA University of Lisbon, NuAr, is part of the Student Association of the Faculty of Science and Technology of NOVA University of Lisbon, AEFCT. As the entity responsible for the website nuarfct.com, we respect your privacy and protect your personal data in accordance with Regulation (EU) 2016/679 of the European Parliament and of the Council, of 27 April 2016 (“GDPR”) and other applicable legislation.",

    // Secção 1
    "1. Disposições gerais": "1. General provisions",
    "O acesso e utilização deste website implicam a aceitação integral destes Termos de Serviço.": "Access to and use of this website imply full acceptance of these Terms of Service.",
    "Se não concordares com estes termos, abste-te de utilizar o website.": "If you do not agree with these terms, please refrain from using the website.",
    "Estes Termos podem ser atualizados; a continuação do uso implica aceitação das alterações.": "These Terms may be updated; continued use implies acceptance of the changes.",

    // Secção 2
    "2. Identificação e contactos": "2. Identification and contacts",
    "O website é gerido pelo Núcleo de Aeroespacial da Universidade NOVA de Lisboa": "The website is managed by the Aerospace Student Organization of NOVA University of Lisbon",
    "Para esclarecimento de dúvidas ou questões relacionadas com o website ou com estes Termos de Serviço, deve contactar através do email nuar@ae.fct.unl.pt": "For clarifications or questions related to the website or these Terms of Service, please contact us via email at nuar@ae.fct.unl.pt",
    "Entidade:": "Entity:",
    "NuAr - Núcleo de Aeroespacial": "NuAr - Aerospace Student Organization",
    "Morada:": "Address:",
    "Universidade NOVA de Lisboa, Lisboa, Portugal": "NOVA University of Lisbon, Lisbon, Portugal",
    "Email:": "Email:",

    // Secção 3
    "3. Objeto e finalidade do website": "3. Purpose and object of the website",
    "Divulgar atividades, projetos, eventos e conteúdos informativos do NuAr.": "Promote activities, projects, events, and informative content from NuAr.",
    "Conteúdos podem ser alterados sem aviso prévio.": "Content may be changed without prior notice.",

    // Secção 4
    "4. Utilização Responsável": "4. Responsible Use",
    "Proíbe-se: fins ilícitos, acesso não autorizado, malware, conteúdos ofensivos/discriminatórios.": "Prohibited: unlawful purposes, unauthorized access, malware, offensive/discriminatory content.",
    "Podemos suspender acesso por uso abusivo.": "We may suspend access due to abusive use.",

    // Secção 5
    "5. Propriedade Intelectual": "5. Intellectual Property",
    "Ao utilizar este website, o utilizador compromete-se a:": "By using this website, the user undertakes to:",
    "Todos os conteúdos são titularidade do NuAr/AEFCT/FCT NOVA ou licenciados.": "All content is owned by NuAr/AEFCT/FCT NOVA or licensed.",
    "Uso pessoal/não comercial permitido, mantendo créditos. Proibida reprodução comercial sem autorização.": "Personal/non-commercial use is allowed, provided credits are maintained. Commercial reproduction without authorization is prohibited.",

    // Secção 6
    "6. Formulários de Recrutamento e Inscrição": "6. Recruitment and Registration Forms",
    "Ao submeteres dados via formulários, declaras ser titular dos direitos sobre esses dados e autorizas o seu uso para recrutamento/inscrições.": "By submitting data via forms, you declare that you own the rights to that data and authorize its use for recruitment/registrations.",
    "Podemos recusar/editar conteúdos inadequados.": "We may refuse/edit inappropriate content.",

    // Secção 7
    "7. Ligações Externas": "7. External Links",
    "Hiperligações a terceiros são por conveniência; não nos responsabilizamos pelo seu conteúdo.": "Hyperlinks to third parties are provided for convenience; we are not responsible for their content.",

    // Secção 8
    "8. Responsabilidade Limitada": "8. Limited Liability",
    "Não garantimos acesso ininterrupto ou ausência total de erros.": "We do not guarantee uninterrupted access or total absence of errors.",
    "Excluímos responsabilidade por danos indiretos, na medida permitida por lei.": "We exclude liability for indirect damages to the extent permitted by law.",

    // Secção 9
    "9. Proteção de Dados": "9. Data Protection",
    "O tratamento de dados pessoais recolhidos através deste website está sujeito à nossa Política de Privacidade, disponível separadamente, em conformidade com o Regulamento Geral sobre a Proteção de Dados (RGPD).": "The processing of personal data collected through this website is subject to our Privacy Policy, available separately, in compliance with the General Data Protection Regulation (GDPR).",

    // Secção 10
    "10. Lei Aplicável": "10. Applicable Law",
    "Estes Termos de Serviço são regidos pela lei portuguesa. Qualquer litígio será submetido à jurisdição dos tribunais portugueses.": "These Terms of Service are governed by Portuguese law. Any dispute shall be submitted to the jurisdiction of the Portuguese courts.",
    // ─── FOOTER & LEGAL ───
    "Os Nossos Contactos": "Our Contacts",
    "Tornamos aeroespacial acessível a todos.": "Making aerospace accessible to everyone.",
    "Termos de Serviço": "Terms of Service",
    "Política de Privacidade": "Privacy Policy",
    "FCT - Universidade NOVA de Lisboa": "SST - NOVA University of Lisbon",
    "© 2026 NuAr - Núcleo de Aeroespacial NOVA FCT. Todos os direitos reservados.": 
        "© 2026 NuAr - Aerospace Student Organization NOVA SST. All rights reserved."
};

const originalTexts = new Map();

function translatePage(targetLang) {
    const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    let node;

    while ((node = walk.nextNode())) {
        const text = node.nodeValue.trim();
        if (!text) continue;

        if (targetLang === "en") {
            if (dictionary[text]) {
                if (!originalTexts.has(node)) {
                    originalTexts.set(node, node.nodeValue);
                }
                node.nodeValue = node.nodeValue.replace(text, dictionary[text]);
            }
        } else {
            if (originalTexts.has(node)) {
                node.nodeValue = originalTexts.get(node);
            }
        }
    }

    document.querySelectorAll('.lang-toggle, .lang-link').forEach(btn => {
        btn.textContent = targetLang === "pt" ? "EN" : "PT";
    });

    localStorage.setItem("preferred_lang", targetLang);
}

document.addEventListener("DOMContentLoaded", () => {
    const currentLang = localStorage.getItem("preferred_lang") || "pt";

    document.querySelectorAll('.lang-toggle, .lang-link').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const activeLang = localStorage.getItem("preferred_lang") || "pt";
            const newLang = activeLang === "pt" ? "en" : "pt";
            translatePage(newLang);
        });
    });

    if (currentLang === "en") {
        translatePage("en");
    }
});