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

    // ─── ACTIVITIES HERO & SECTIONS ───
    "Atividades e Eventos": "Activities & Events",
    "Vem participar e conhecer as atividades que vamos desenvolvendo ao longo do ano!": 
        "Come participate and discover the activities we develop throughout the year!",
    "Atividades por vir": "Upcoming Activities",
    "Atividades Passadas": "Past Activities",

    // ─── STAY UPDATED SECTION ───
    "Informa-te sobre os nossos eventos": "Stay updated on our events",
    "Segue-nos nas nossas redes sociais para te manteres a par de todos os workshops, palestras, visitas e eventos do NuAr.": 
        "Follow us on our social networks to stay up to date with all NuAr workshops, lectures, visits, and events.",
    "Segue-nos no Instagram": "Follow us on Instagram",
    "Vê o nosso LinkedIn": "Check out our LinkedIn",

    // ─── HERO PROJECTS & CARDS ───
    "Os Nossos Projetos": "Our Projects",
    "Desenvolvemos projetos para os alunos poderem complementarem as o que aprendem nas aulas": 
        "We develop projects to complement what students learn in class",
    "Aerospace Student Team for Rocketry Operations (ASTRO)": "Aerospace Student Team for Rocketry Operations (ASTRO)",
    "O principal objetivo do projeto ASTRO é participar no European Rocketry Challenge (EuRoC), uma prestigiada competição internacional dedicada a equipas universitárias.": 
        "The main goal of the ASTRO project is to participate in the European Rocketry Challenge (EuRoC), a prestigious international competition dedicated to university teams.",
    "45 membros": "45 members",
    "Ver Projeto": "View Project",
    "NuAr Summer School (NSS)": "NuAr Summer School (NSS)",
    "A NuAr Summer School é a primeira escola de verão em Porgutal a promover, ao longo de uma semana, um programa lúdico-educativo dedicado à temática do Espaço para jovens entre os 13 e os 17 anos.": 
        "The NuAr Summer School is the first summer school in Portugal to offer a week-long educational and fun program dedicated to Space for youth aged 13 to 17.",
    "8 membros": "8 members",
    "Student UAV Experimentation Section (AirNOVA)": "Student UAV Experimentation Section (AirNOVA)",
    "Equipa multidisciplinar dedicada ao design e construção de um drone, para participar na competição AeroCup.": 
        "Multidisciplinary team dedicated to the design and construction of a drone to participate in the AeroCup competition.",
    "Secção de Telescópios e Astronomia Recreativa (STAR)": "Section of Telescopes and Recreational Astronomy (STAR)",
    "iniciativa dedicada à divulgação da astronomia e da astrofotograia junto da comunidade através de várias atividades de observação e realização de workshops.": 
        "Initiative dedicated to spreading astronomy and astrophotography to the community through observation activities and workshops.",
    "2 membros": "2 members",

    // ─── POPUP & JOIN SECTION ───
    "Queres te juntar ou criar um Projeto connosco?": "Want to join or create a Project with us?",
    "Caso estejas interessado em algum dos nossos Projetos ou tenhas uma ideia que gostasses de desenvolver, clica no botão abaixo.": 
        "If you are interested in any of our Projects or have an idea you'd like to develop, click the button below.",
    "Mais informações": "More Information",
    "Junta-te ao NuAr!": "Join NuAr!",
    "Ficamos entusiasmados por saber que gostavas de desenvolver um projeto com o NuAr.": 
        "We are excited to know you would like to develop a project with NuAr.",
    "Envia-nos um email": "Send us an email",
    "Apresenta-te e conta-nos sobre o teu interesse e os teus objetivos.": 
        "Introduce yourself and tell us about your interests and goals.",
    "Participa numa reunião informal": "Attend an informal meeting",
    "Conhece a nossa equipa e descobre mais sobre os Projetos em curso e como nós os ajudamos a crescer.": 
        "Meet our team and find out more about ongoing Projects and how we help them grow.",
    "Escolhe/Cria o teu projeto": "Choose/Create your project",
    "Com base nos teus interesses e competências, encontramos o projeto ideal para ti. Caso querias criar algo novo iremos te ajudar a arranjar uma equipa para iniciar o Projeto!": 
        "Based on your interests and skills, we find the ideal project for you. If you want to create something new, we'll help you assemble a team to launch it!",
    "Mãos à Obra": "Get to Work",
    "Integra/Cria a equipa e começa a trabalhar!": "Join or build the team and get started!",
    "Enviar Email": "Send Email",
    "Fechar": "Close",

    // ─── ABOUT PAGE ───
    "Sobre o NuAr": "About NuAr",
    "Mostramos que o espaço é de todos!": "Showing that space belongs to everyone!",
    "A Nossa Missão": "Our Mission",
    "Queremos mostrar que a área aeroespacial é para todos, reunindo estudantes de diferentes áreas da engenharia e das ciências para desenvolver ideias além da sala de aula.": 
        "We aim to show that aerospace is for everyone, bringing together students from different engineering and science fields to develop ideas beyond the classroom.",
    "Para isto organizamos vários tipos de eventos e competições para todos os estudantes e ajudamos os nossos membros a desenvolver projetos que proporcionam experiências práticas.": 
        "To achieve this, we organize various events and competitions for all students and help our members develop projects that provide practical experience.",
    "A Nossa Visão": "Our Vision",
    "Aspiramos tornar-nos numa organização estudantil de referência em aeroespacial tanto em Portugal quanto na Europa, reconhecida pela inovação e pelo contributo para a indústria e comunidade científica aeroespacial — tanto universitária como pré-universitária.": 
        "We aspire to become a reference student organization in aerospace in Portugal and Europe, recognized for innovation and contribution to the aerospace industry and scientific community — both university and pre-university.",
    "Os Nossos Valores": "Our Values",
    "Os princípios que orientam o nosso trabalho e moldam a nossa comunidade": "The principles that guide our work and shape our community",
    "Inovação": "Innovation",
    "Promovemos a criatividade e o pensamento crítico em cada projeto que desenvolvemos.": "We foster creativity and critical thinking in every project we develop.",
    "Colaboração": "Collaboration",
    "Trabalhamos em equipa para alcançar um objetivo comum e impactante.": "We work as a team to reach a common, impactful goal.",
    "Educação": "Education",
    "Partilhamos conhecimento através de atividades práticas e iniciativas inclusivas.": "We share knowledge through hands-on activities and inclusive initiatives.",
    "A Nossa História": "Our History",
    "O início de uma jornada aeroespacial na NOVA FCT": "The beginning of an aerospace journey at NOVA FCT",
    "Fundados para inovar": "Founded to innovate",
    "O NuAr foi fundado por um grupo de estudantes interessados por engenharia aeroespacial da Universidade NOVA de Lisboa, quando este curso ainda não existia na mesma. Unidos pela visão comum de promover o conhecimento em aeroespacial e criar oportunidades de aprendizagem prática para além do ambiente tradicional de sala de aula foi fundado o NuAr no dia 8 de junho de 2023.": 
        "NuAr was founded by a group of students passionate about aerospace engineering at Universidade NOVA de Lisboa, back when the course didn't exist at the university. United by the shared vision of promoting aerospace knowledge and creating practical learning opportunities beyond the classroom, NuAr was founded on June 8, 2023.",
    "Desde a nossa fundação, crescemos e tornámo-nos numa comunidade de estudantes de várias áreas da engenharia e das ciências, todos unidos pela fascínio pelas tecnologias aeroespaciais e pela vontade de ajudar os estudantes.": 
        "Since our foundation, we have grown into a community of students from various engineering and science fields, all united by a fascination with aerospace technologies and a desire to help students.",
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