// Dicionário de traduções mapeado por frases
const dictionary = {
    // Nav
    "Início": "Home",
    "Sobre Nós": "About Us",
    "Projetos": "Projects",
    "Ver Todos": "See All",
    "Atividades": "Activities",
    "Programa Educativo": "Educational Program",
    "Contactos": "Contacts",

    // Hero
    "O Espaço é de Todos": "Space Belongs to Everyone",
    "Somos o Núcleo de Aeroespacial da NOVA FCT, onde estudantes de engenharia e ciências constroem o futuro": 
        "We are NOVA SST's Aerospace Student Organization, where engineering and science students build the future",
    "Conhece-nos": "Get to know us",
    "Os nossos projetos": "Our projects",

    // Recrutamento
    "Em":" ", 
    "Destaque": "Highlights",
    "Recrutamento Aberto": "Recruitment Open",
    "Junta-te ao NuAr": "Join NuAr 2026",
    "Estamos a recrutar novos membros! Se gostas do espaço e tens vontade de aprender fazendo, esta é a tua oportunidade.": 
        "We are recruiting new members! If you love space and want to learn by doing, this is your opportunity.",
    "Candidaturas até 13 Março 2026": "Applications until March 13, 2026",
    "Candidata-te agora": "Apply now",

    // Missão e Explora
    "A Nossa Missão": "Our Mission",
    "Reunimos estudantes de várias áreas de engenharia para aprender fazendo através de projetos reais, competições internacionais e experiências que a sala de aula não consegue oferecer.": 
        "We bring together students from various engineering fields to learn by doing through hands-on projects, international competitions, and experiences classroom walls cannot offer.",
    "Explora o NuAr": "Explore NuAr",
    "Projetos técnicos, workshops práticos e um programa que chega às escolas de todo o país.": 
        "Technical projects, hands-on workshops, and an outreach program that reaches schools nationwide.",
    "Foguetões, satélites e muito mais iniciativas lideradas pelos próprios membros.":
        "Rockets, satellites, and much more initiatives led by students themselves.",
    "Ver projetos →": "View projects →",
    "Workshops, palestras e eventos para inspirar e ligar pessoas apaixonadas por espaço.": 
        "Workshops, talks, and events to inspire and connect space enthusiasts.",
    "Ver atividades →": "View activities →",
    "Prog. Educativo": "Edu. Program",
    "Levamos a engenharia aeroespacial a escolas de todo o país para inspirar a próxima geração.": 
        "We bring aerospace engineering to schools across the country to inspire the next generation.",
    "Saber mais →": "Learn more →",

    // Stats
    "Programa Educativo NuAr": "NuAr Educational Program",
    "Levamos atividades práticas de aeroespacial a escolas por todo o país e os números falam por si.": 
        "We bring hands-on aerospace activities to schools across the country and the numbers speak for themselves.",
    "Escolas Visitadas": "Schools Visited",
    "Alunos Inspirados": "Students Inspired",
    "Atividades Diferentes": "Different Activities",

    // Footer & Popup
    "Os Nossos Contactos": "Our Contacts",
    "Tornamos aeroespacial acessível a todos.": "Making aerospace accessible to everyone.",
    "Termos de Serviço": "Terms of Service",
    "Política de Privacidade": "Privacy Policy",
    "FCT - Universidade NOVA de Lisboa": "SST - NOVA University of Lisbon",
    "© 2026 NuAr - Núcleo de Aeroespacial NOVA FCT. Todos os direitos reservados.": 
        "© 2026 NuAr - Aerospace Student Organization NOVA SST. All rights reserved."
};

// Guarda os textos originais em Português
const originalTexts = new Map();

function translatePage(targetLang) {
    // Seleciona todos os nós de texto no documento
    const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    let node;

    while ((node = walk.nextNode())) {
        const text = node.nodeValue.trim();
        if (!text) continue;

        if (targetLang === "en") {
            if (dictionary[text]) {
                if (!originalTexts.has(node)) {
                    originalTexts.set(node, node.nodeValue); // Guarda o texto original em PT
                }
                node.nodeValue = node.nodeValue.replace(text, dictionary[text]);
            }
        } else {
            // Restaura o texto original em Português
            if (originalTexts.has(node)) {
                node.nodeValue = originalTexts.get(node);
            }
        }
    }

    // Atualiza o texto dos botões de idioma
    document.querySelectorAll('.lang-toggle, .lang-link').forEach(btn => {
        btn.textContent = targetLang === "pt" ? "EN" : "PT";
    });

    localStorage.setItem("preferred_lang", targetLang);
}

document.addEventListener("DOMContentLoaded", () => {
    const currentLang = localStorage.getItem("preferred_lang") || "pt";

    // Adiciona o evento de clique nos botões
    document.querySelectorAll('.lang-toggle, .lang-link').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const activeLang = localStorage.getItem("preferred_lang") || "pt";
            const newLang = activeLang === "pt" ? "en" : "pt";
            translatePage(newLang);
        });
    });

    // Se o idioma salvo for inglês, traduz ao carregar a página
    if (currentLang === "en") {
        translatePage("en");
    }
});