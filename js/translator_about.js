// Dicionário de traduções completo para todas as páginas (incluindo about.html)
const dictionary = {
    // ─── NAVBAR & MENU ───
    "Início": "Home",
    "Sobre Nós": "About Us",
    "Projetos": "Projects",
    "Ver Todos": "See All",
    "Atividades": "Activities",
    "Programa Educativo": "Educational Program",
    "Contactos": "Contacts",

    // ─── ABOUT HERO ───
    "Sobre o NuAr": "About NuAr",
    "Mostramos que o espaço é de todos!": "Showing that space belongs to everyone!",

    // ─── MISSÃO E VISÃO ───
    "A Nossa Missão": "Our Mission",
    "Queremos mostrar que a área aeroespacial é para todos, reunindo estudantes de diferentes áreas da engenharia e das ciências para desenvolver ideias além da sala de aula.": 
        "We aim to show that aerospace is for everyone, bringing together students from different engineering and science fields to develop ideas beyond the classroom.",
    "Para isto organizamos vários tipos de eventos e competições para todos os estudantes e ajudamos os nossos membros a desenvolver projetos que proporcionam experiências práticas.": 
        "To achieve this, we organize various events and competitions for all students and help our members develop projects that provide practical experience.",
    "A Nossa Visão": "Our Vision",
    "Aspiramos tornar-nos numa organização estudantil de referência em aeroespacial tanto em Portugal quanto na Europa, reconhecida pela inovação e pelo contributo para a indústria e comunidade científica aeroespacial, tanto universitária como pré-universitária.": 
        "We aspire to become a reference student organization in aerospace in Portugal and Europe, recognized for innovation and contribution to the aerospace industry and scientific community, both university and pre-university.",

    // ─── VALORES ───
    "Os Nossos Valores": "Our Values",
    "Os princípios que orientam o nosso trabalho e moldam a nossa comunidade": "The principles that guide our work and shape our community",
    "Inovação": "Innovation",
    "Promovemos a criatividade e o pensamento crítico em cada projeto que desenvolvemos.": "We foster creativity and critical thinking in every project we develop.",
    "Colaboração": "Collaboration",
    "Trabalhamos em equipa para alcançar um objetivo comum e impactante.": "We work as a team to reach a common, impactful goal.",
    "Educação": "Education",
    "Partilhamos conhecimento através de atividades práticas e iniciativas inclusivas.": "We share knowledge through hands-on activities and inclusive initiatives.",

    // ─── HISTÓRIA ───
    "A Nossa História": "Our History",
    "O início de uma jornada aeroespacial na NOVA FCT": "The beginning of an aerospace journey at NOVA FCT",
    "Fundados para inovar": "Founded to innovate",
    "O NuAr foi fundado por um grupo de estudantes interessados por engenharia aeroespacial da Universidade NOVA de Lisboa, quando este curso ainda não existia na mesma. Unidos pela visão comum de promover o conhecimento em aeroespacial e criar oportunidades de aprendizagem prática para além do ambiente tradicional de sala de aula foi": 
        "NuAr was founded by a group of students passionate about aerospace engineering at Universidade NOVA de Lisboa, back when the course didn't exist at the university. United by the shared vision of promoting aerospace knowledge and creating practical learning opportunities beyond the classroom, NuAr was",
    "fundado o NuAr no dia 8 de junho de 2023": "founded on June 8, 2023",
    ".":".",
    "Desde a nossa fundação, crescemos e tornámo-nos numa comunidade de": "Since our foundation, we have grown into a community of ",
    "estudantes de várias áreas da engenharia e das ciências":"students from various engineering and science fields",
    ", todos unidos pela fascínio pelas tecnologias aeroespaciais e pela vontade de ajudar os estudantes.":", all united by a fascination with aerospace technologies and a desire to help students.",
    "Atualmente, o NuAr continua a expandir o seu impacto com:": "Currently, NuAr continues to expand its impact with:",
    "Projetos inovadores": "Innovative projects",
    "- onde os nossos membros têm liberdade criativa e apoio técnico para desenvolver as suas ideias em equipa.": 
        "- where our members have creative freedom and technical support to develop their ideas as a team.",
    "Iniciativas educativas": "Educational initiatives",
    "- através de visitas a várias escolas e empresas, mostramos aos jovens que a engenharia é algo que todos podemos alcançar e que o céu não é o limite.": 
        "- through visits to schools and companies, we show young people that engineering is achievable for everyone and that the sky is not the limit.",

    // ─── FOOTER & LEGAL ───
    "Os Nossos Contactos": "Our Contacts",
    "Tornamos aeroespacial acessível a todos.": "Making aerospace accessible to everyone.",
    "Termos de Serviço": "Terms of Service",
    "Política de Privacidade": "Privacy Policy",
    "FCT - Universidade NOVA de Lisboa": "SST - NOVA University of Lisbon",
    "© 2026 NuAr - Núcleo de Aeroespacial NOVA FCT. Todos os direitos reservados.": 
        "© 2026 NuAr - Aerospace Student Organization NOVA SST. All rights reserved."
};

// Mapa para guardar os nós e os textos originais em Português
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

    // Atualiza o texto visual de todos os botões de idioma para o estado oposto
    document.querySelectorAll('.lang-toggle, .lang-link').forEach(btn => {
        btn.textContent = targetLang === "pt" ? "EN" : "PT";
    });

    localStorage.setItem("preferred_lang", targetLang);
}

document.addEventListener("DOMContentLoaded", () => {
    const currentLang = localStorage.getItem("preferred_lang") || "pt";

    // Adiciona o evento de clique aos botões de alternância
    document.querySelectorAll('.lang-toggle, .lang-link').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const activeLang = localStorage.getItem("preferred_lang") || "pt";
            const newLang = activeLang === "pt" ? "en" : "pt";
            translatePage(newLang);
        });
    });

    // Se o idioma ativo for o inglês, aplica logo a tradução ao carregar
    if (currentLang === "en") {
        translatePage("en");
    }
});