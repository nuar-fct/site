"""
╔══════════════════════════════════════════════════════════════╗
║         GESTOR DE ATIVIDADES — NuAr                          ║
║  Compatível com o novo sistema de páginas individuais        ║
║                                                              ║
║  Ficheiros geridos:                                          ║
║    activities.html        — lista de atividades              ║
║    atividade-<id>.html    — página de cada atividade         ║
║    css/activity-page.css  — (não alterado pelo script)       ║
╚══════════════════════════════════════════════════════════════╝
"""

import re
import shutil
from pathlib import Path
from datetime import datetime
from turtle import pos


# ──────────────────────────────────────────────────────────────
# CONFIGURAÇÃO — ajusta os caminhos se necessário
# ──────────────────────────────────────────────────────────────
ACTIVITIES_HTML   = "activities.html"        # ficheiro da lista
TEMPLATE_HTML     = "atividade-template.html" # template de cada atividade

# Marcadores no activities.html
MARKER_UPCOMING  = "<!-- ATIVIDADES_POR_VIR_MARKER -->"
MARKER_PAST      = "<!-- ATIVIDADES_PASSADAS_MARKER -->"

# SVGs reutilizáveis (mesmos do HTML)
SVG_CALENDAR = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                                    <line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>
                                </svg>"""

SVG_CLOCK = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
                                </svg>"""

SVG_PIN = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>
                                </svg>"""

SVG_PEOPLE = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                                    <circle cx="9" cy="7" r="4"/>
                                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                                </svg>"""

SVG_ARROW_LEFT = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>
                </svg>"""

SVG_ARROW_RIGHT = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
                    </svg>"""


# ──────────────────────────────────────────────────────────────
# UTILITÁRIOS
# ──────────────────────────────────────────────────────────────

def criar_id(titulo: str, data: str) -> str:
    """Gera um ID de ficheiro a partir do título + data."""
    base = f"{titulo}-{data}"
    return re.sub(r'[^a-z0-9]+', '-', base.lower()).strip('-')


def drive_url_para_thumbnail(url: str, tamanho: str = "w1000") -> str:
    """Converte qualquer link do Google Drive num URL de thumbnail."""
    if not url:
        return ""
    if "http" not in url:
        return f"https://drive.google.com/thumbnail?id={url.strip()}&sz={tamanho}"
    for pattern in [r'/file/d/([^/\?]+)', r'[?&]id=([^&]+)', r'[-\w]{20,}']:
        m = re.search(pattern, url)
        if m:
            return f"https://drive.google.com/thumbnail?id={m.group(1)}&sz={tamanho}"
    return url


def ler_ficheiro(caminho: str) -> str | None:
    try:
        return Path(caminho).read_text(encoding='utf-8')
    except FileNotFoundError:
        print(f"\n❌ Ficheiro '{caminho}' não encontrado.")
        return None


def escrever_ficheiro(caminho: str, conteudo: str) -> bool:
    try:
        Path(caminho).write_text(conteudo, encoding='utf-8')
        return True
    except Exception as e:
        print(f"\n❌ Erro ao escrever '{caminho}': {e}")
        return False


def fazer_backup(caminho: str):
    """Cria um backup .bak antes de qualquer alteração."""
    src = Path(caminho)
    if src.exists():
        shutil.copy2(src, src.with_suffix('.bak'))


# ──────────────────────────────────────────────────────────────
# INPUT INTERATIVO
# ──────────────────────────────────────────────────────────────

def obter_fotos() -> list[dict]:
    """Pede os links das fotos da galeria (Google Drive)."""
    fotos = []
    print("\n📸 Fotos da galeria (Google Drive)")
    print("   Cole o link completo ou apenas o ID. Enter em branco para terminar.")
    while True:
        url = input(f"\n   Foto {len(fotos) + 1} — URL: ").strip()
        if not url:
            break
        fotos.append({"url": url, "thumbnail": drive_url_para_thumbnail(url, "w800")})
    return fotos


def obter_paragrafos() -> list[str]:
    """Pede parágrafos de descrição da página da atividade."""
    paragrafos = []
    print("\n   Escreve cada parágrafo e pressiona Enter. Enter em branco para terminar.")
    while True:
        p = input(f"\n   Parágrafo {len(paragrafos) + 1}: ").strip()
        if not p:
            break
        paragrafos.append(p)
    return paragrafos


# ──────────────────────────────────────────────────────────────
# GERAÇÃO DE HTML
# ──────────────────────────────────────────────────────────────

def gerar_card_html(atividade: dict) -> str:
    """Gera o bloco <a class="activity-card"> para a lista activities.html."""
    return f"""
            <div class="activity-card" id="{atividade['pagina']}">
                <div class="activity-card-image">
                    <img src="{atividade['thumb']}" alt="{atividade['titulo']}" loading="lazy">
                </div>
                <div class="activity-content">
                    <h3 class="activity-title">{atividade['titulo']}</h3>
                    <div class="activity-details">
                        <div class="detail-item">
                            <span class="detail-icon">{SVG_CALENDAR}</span>
                            <span>{atividade['data']}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-icon">{SVG_CLOCK}</span>
                            <span>{atividade['hora']}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-icon">{SVG_PIN}</span>
                            <span>{atividade['local']}</span>
                        </div>
                    </div>
                    <a href="{atividade['pagina']}" class="register-btn">Ver mais</a>
                </div>
            </div>"""


def gerar_card_passado_html(atividade: dict) -> str:
    """Card simplificado para atividades passadas (sem hora)."""
    return f"""
            <div class="activity-card activity-card--past" id="{atividade['pagina']}">
                <div class="activity-card-image">
                    <img src="{atividade['thumb']}" alt="{atividade['titulo']}" loading="lazy">
                </div>
                <div class="activity-content">
                    <h3 class="activity-title">{atividade['titulo']}</h3>
                    <div class="activity-details">
                        <div class="detail-item">
                            <span class="detail-icon">{SVG_CALENDAR}</span>
                            <span>{atividade['data']}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-icon">{SVG_PIN}</span>
                            <span>{atividade['local']}</span>
                        </div>
                    </div>
                    <a href="{atividade['pagina']}" class="register-btn">Ver mais</a>
                </div>
            </div>"""


def gerar_pagina_atividade(atividade: dict, template: str) -> str:
    """
    Gera o HTML completo da página individual da atividade,
    substituindo os placeholders do template.
    """
    # Parágrafos de descrição
    paragrafos_html = "\n                    ".join(
        f"<p>{p}</p>" for p in atividade.get('paragrafos', ["Descrição em breve."])
    )

    # Galeria de fotos
    if atividade.get('fotos'):
        items_galeria = "\n                        ".join(
            f'<div class="gallery-item">\n'
            f'                            <img src="{f["thumbnail"]}" alt="Foto {i+1}" loading="lazy">\n'
            f'                        </div>'
            for i, f in enumerate(atividade['fotos'])
        )
        botao_galeria = ""
        if atividade.get('link_galeria'):
            botao_galeria = f"""
                        <a href="{atividade['link_galeria']}" class="gallery-all-btn" target="_blank">
                            Ver todas as fotos
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                                <polyline points="15 3 21 3 21 9"/>
                                <line x1="10" y1="14" x2="21" y2="3"/>
                            </svg>
                        </a>"""
        secao_galeria = f"""
                    <!-- Galeria -->
                    <section class="activity-section">
                        <h2 class="activity-section-title">Galeria</h2>
                        <div class="activity-gallery">
                            {items_galeria}
                        </div>
                        {botao_galeria}
                    </section>"""
    else:
        secao_galeria = ""

    # Vagas (opcional)
    if atividade.get('vagas'):
        sidebar_vagas = f"""
                        <div class="sidebar-detail-item">
                            <span class="detail-icon">{SVG_PEOPLE}</span>
                            <div>
                                <span class="sidebar-detail-label">Vagas</span>
                                <span class="sidebar-detail-value">{atividade['vagas']}</span>
                            </div>
                        </div>"""
    else:
        sidebar_vagas = ""

    # Botão de inscrição (só para atividades futuras)
    if atividade.get('inscricao_email'):
        assunto = f"Inscrição — {atividade['titulo']}"
        sidebar_cta = f"""
                    <a href="mailto:{atividade['inscricao_email']}?subject={assunto}" class="sidebar-cta">
                        Confirmar presença
                        {SVG_ARROW_RIGHT}
                    </a>"""
    else:
        sidebar_cta = ""

    html = f"""<!DOCTYPE html>
<html lang="pt">
<head>
    <link rel="icon" type="image/png" href="images/LogoPequeno_2.png" sizes="45x45">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NuAr - {atividade['titulo']}</title>
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/activity-page.css">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
</head>

<body>

    <!-- ===================== NAVBAR ===================== -->
    <nav class="navbar" role="navigation" aria-label="Navegação principal">
        <div class="nav-container">
            <a href="index.html" class="logo" aria-label="NuAr - Página Inicial">
                <img src="images/logo_cor.png" alt="NuAr Logo">
            </a>
            <button class="hamburger" id="hamburger" aria-label="Abrir menu" aria-expanded="false">
                <span></span><span></span><span></span>
            </button>
            <ul class="nav-menu" id="nav-menu">
                <li class="nav-item"><a href="index.html" class="nav-link">Início</a></li>
                <li class="nav-item"><a href="about.html" class="nav-link">Sobre Nós</a></li>
                <li class="nav-item dropdown" id="dropdown">
                    <a href="projects.html" class="nav-link dropdown-toggle">Projetos <span class="arrow-down">▼</span></a>
                    <div class="dropdown-content">
                        <a href="projeto_astro.html" class="dropdown-item">🚀 ASTRO</a>
                        <a href="projeto_star.html" class="dropdown-item">🔭 STAR</a>
                        <a href="projeto_nss.html" class="dropdown-item">🎯 NSS</a>
                        <a href="projects.html" class="dropdown-item">Ver Todos →</a>
                    </div>
                </li>
                <li class="nav-item"><a href="activities.html" class="nav-link">Atividades</a></li>
                <li class="nav-item"><a href="educativa.html" class="nav-link">Programa Educativo</a></li>
                <li class="nav-item"><a href="contacts.html" class="nav-link">Contactos</a></li>
            </ul>
            <div class="language-switcher language-switcher-desktop">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/>
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                </svg>
                <span class="lang-divider-mobile"></span>
                <a href="#" class="lang-link" aria-label="English">EN</a>
            </div>
        </div>
    </nav>


    <!-- Hero -->
    <section class="activity-hero">
        <img src="{atividade['thumb']}" alt="{atividade['titulo']}" class="activity-hero-img">
        <div class="activity-hero-overlay"></div>
        <div class="activity-hero-content">
            <a href="activities.html" class="activity-back-link">
                {SVG_ARROW_LEFT}
                Voltar às atividades
            </a>
            <h1 class="activity-hero-title">{atividade['titulo']}</h1>
        </div>
    </section>


    <!-- Conteúdo -->
    <main class="activity-main">
        <div class="activity-container">

            <!-- Corpo -->
            <div class="activity-body">
                <section class="activity-section">
                    <h2 class="activity-section-title">Sobre a atividade</h2>
                    {paragrafos_html}
                </section>
                {secao_galeria}
            </div>

            <!-- Sidebar -->
            <aside class="activity-sidebar">
                <div class="sidebar-card">
                    <h3 class="sidebar-title">Detalhes</h3>
                    <div class="sidebar-details">
                        <div class="sidebar-detail-item">
                            <span class="detail-icon">{SVG_CALENDAR}</span>
                            <div>
                                <span class="sidebar-detail-label">Data</span>
                                <span class="sidebar-detail-value">{atividade['data']}</span>
                            </div>
                        </div>
                        <div class="sidebar-detail-item">
                            <span class="detail-icon">{SVG_CLOCK}</span>
                            <div>
                                <span class="sidebar-detail-label">Hora</span>
                                <span class="sidebar-detail-value">{atividade['hora']}</span>
                            </div>
                        </div>
                        <div class="sidebar-detail-item">
                            <span class="detail-icon">{SVG_PIN}</span>
                            <div>
                                <span class="sidebar-detail-label">Local</span>
                                <span class="sidebar-detail-value">{atividade['local']}</span>
                            </div>
                        </div>
                        {sidebar_vagas}
                    </div>
                    {sidebar_cta}
                </div>
            </aside>

        </div>
    </main>


    <!-- Lightbox -->
    <div id="lightbox" class="lightbox" onclick="closeLightbox()">
        <span class="lightbox-close">&times;</span>
        <span class="lightbox-arrow lightbox-arrow-left" onclick="event.stopPropagation(); navigateLightbox(-1)">&#10094;</span>
        <span class="lightbox-arrow lightbox-arrow-right" onclick="event.stopPropagation(); navigateLightbox(1)">&#10095;</span>
        <div class="lightbox-content" onclick="event.stopPropagation()">
            <img id="lightbox-img" src="" alt="">
        </div>
        <div class="lightbox-counter" id="lightbox-counter"></div>
    </div>


    <script>
        // Navbar
        const hamburger = document.getElementById('hamburger');
        const navMenu   = document.getElementById('nav-menu');
        const dropdown  = document.getElementById('dropdown');
        const dropdownToggle = document.querySelector('.dropdown-toggle');
        hamburger.addEventListener('click', (e) => {{
            e.stopPropagation();
            const isOpen = navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
            hamburger.setAttribute('aria-expanded', isOpen);
        }});
        if (dropdownToggle) {{
            dropdownToggle.addEventListener('click', (e) => {{
                if (window.innerWidth <= 900) {{ e.preventDefault(); dropdown.classList.toggle('active'); }}
            }});
        }}
        document.querySelectorAll('.nav-link:not(.dropdown-toggle)').forEach(n => {{
            n.addEventListener('click', () => {{
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
                if (dropdown) dropdown.classList.remove('active');
            }});
        }});
        window.addEventListener('resize', () => {{
            if (window.innerWidth > 900) {{
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
                if (dropdown) dropdown.classList.remove('active');
            }}
        }});
        document.addEventListener('click', (e) => {{
            if (!navMenu.contains(e.target) && !hamburger.contains(e.target)) {{
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
                if (dropdown) dropdown.classList.remove('active');
            }}
        }});

        // Galeria / Lightbox
        let currentIndex = 0;
        const galleryItems = document.querySelectorAll('.gallery-item img');
        galleryItems.forEach((img, i) => img.addEventListener('click', () => openLightbox(i)));

        function openLightbox(index) {{
            currentIndex = index;
            const lb = document.getElementById('lightbox');
            document.getElementById('lightbox-img').src = galleryItems[index].src;
            document.getElementById('lightbox-counter').textContent = `${{index + 1}} / ${{galleryItems.length}}`;
            lb.classList.add('active');
            document.body.style.overflow = 'hidden';
        }}
        function closeLightbox() {{
            document.getElementById('lightbox').classList.remove('active');
            document.body.style.overflow = '';
        }}
        function navigateLightbox(dir) {{
            currentIndex = (currentIndex + dir + galleryItems.length) % galleryItems.length;
            openLightbox(currentIndex);
        }}
        document.addEventListener('keydown', (e) => {{
            const lb = document.getElementById('lightbox');
            if (!lb.classList.contains('active')) return;
            if (e.key === 'Escape')     closeLightbox();
            if (e.key === 'ArrowRight') navigateLightbox(1);
            if (e.key === 'ArrowLeft')  navigateLightbox(-1);
        }});
    </script>

</body>

<footer class="footer">
    <div class="footer-container">
        <div class="footer-content">
            <div class="footer-brand">
                <div class="footer-logo">
                    <img src="images/logo_branco.png" alt="NuAr Logo">
                    <img src="images/Logo_AEFCT_CMYK_PNG_horizontal_monocromático.png" alt="AEFCT Logo">
                </div>
                <p class="footer-description">Tornamos Aeroespacial acessível a todos!</p>
                <div class="footer-social">
                    <a href="https://www.instagram.com/nuarfct/" class="footer-social-link" aria-label="Instagram" target="_blank">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
                            <path d="m16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/>
                            <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/>
                        </svg>
                    </a>
                    <a href="https://www.linkedin.com/company/nuarfct/" class="footer-social-link" aria-label="LinkedIn" target="_blank">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/>
                            <rect x="2" y="9" width="4" height="12"/>
                            <circle cx="4" cy="4" r="2"/>
                        </svg>
                    </a>
                </div>
            </div>
            <div class="footer-links">
                <h3>Páginas</h3>
                <ul>
                    <li><a href="about.html">Sobre Nós</a></li>
                    <li><a href="projects.html">Projetos</a></li>
                    <li><a href="activities.html">Atividades</a></li>
                    <li><a href="educativa.html">Programa Educativo</a></li>
                </ul>
            </div>
            <div class="footer-links">
                <h3>Legal</h3>
                <ul>
                    <li><a href="TermosServicos.html">Termos de Serviço</a></li>
                    <li><a href="PoliticaPrivacidade.html">Política de Privacidade</a></li>
                </ul>
            </div>
            <div class="footer-contact">
                <h3>Contactos</h3>
                <div class="contact-info">
                    <p>FCT — Universidade NOVA de Lisboa</p>
                    <p>2829-516 Caparica, Portugal</p>
                    <p><a href="mailto:nuar@ae.fct.unl.pt">nuar@ae.fct.unl.pt</a></p>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <div class="footer-divider"></div>
            <p class="copyright">© 2026 NuAr - Núcleo de Aeroespacial NOVA FCT. Todos os direitos reservados.</p>
        </div>
    </div>
</footer>

</html>"""

    return html


# ──────────────────────────────────────────────────────────────
# OPERAÇÕES NA LISTA (activities.html)
# ──────────────────────────────────────────────────────────────

def adicionar_card_na_lista(atividade: dict, secao: str = "upcoming") -> bool:
    """
    Insere o card da atividade em activities.html.
    secao: 'upcoming' → Atividades por vir | 'past' → Atividades Passadas
    """
    conteudo = ler_ficheiro(ACTIVITIES_HTML)
    if conteudo is None:
        return False

    marker = MARKER_UPCOMING if secao == "upcoming" else MARKER_PAST
    if marker not in conteudo:
        print(f"\n❌ Marcador '{marker}' não encontrado em {ACTIVITIES_HTML}.")
        return False

    card = gerar_card_html(atividade) if secao == "upcoming" else gerar_card_passado_html(atividade)

    fazer_backup(ACTIVITIES_HTML)
    novo = conteudo.replace(marker, marker + card)
    return escrever_ficheiro(ACTIVITIES_HTML, novo)


def encontrar_card_na_lista(conteudo: str, pagina: str):
    marker = f'id="{pagina}"'
    pos = conteudo.find(marker)
    if pos == -1:
        return None, None

    start = conteudo.rfind('<div', 0, pos)
    if start == -1:
        return None, None

    depth = 0
    i = start
    n = len(conteudo)

    while i < n:
        next_open  = conteudo.find('<div', i)
        next_close = conteudo.find('</div>', i)

        if next_open == -1 and next_close == -1:
            break

        if next_close == -1 or (next_open != -1 and next_open < next_close):
            depth += 1
            i = next_open + 4
        else:
            depth -= 1
            i = next_close + 6
            if depth == 0:
                return start, i

    return None, None


def remover_card_da_lista(pagina: str) -> bool:
    """Remove o card com href=pagina de activities.html."""
    conteudo = ler_ficheiro(ACTIVITIES_HTML)
    if conteudo is None:
        return False

    start, end = encontrar_card_na_lista(conteudo, pagina)
    if start is None:
        print(f"\n❌ Card '{pagina}' não encontrado na lista.")
        return False

    fazer_backup(ACTIVITIES_HTML)
    return escrever_ficheiro(ACTIVITIES_HTML, conteudo[:start] + conteudo[end:])


def mover_card_para_passadas(pagina: str) -> bool:
    """
    Move o card de #upcomingActivities para #pastActivities em activities.html.
    Substitui também a classe para activity-card--past.
    """
    conteudo = ler_ficheiro(ACTIVITIES_HTML)
    if conteudo is None:
        return False

    # verificar que o card está em upcoming
    href_marker = f'href="{pagina}"'
    pos = conteudo.find(href_marker)
    if pos == -1:
        print(f"\n❌ Card '{pagina}' não encontrado na lista.")
        return False

    # verificar que está antes do marcador de passadas
    pos_past_marker = conteudo.find(MARKER_PAST)
    if pos_past_marker != -1 and pos > pos_past_marker:
        print(f"\n⚠️  O card '{pagina}' já está em Atividades Passadas.")
        return False

    # extrair o card
    start, end = encontrar_card_na_lista(conteudo, pagina)
    if start is None:
        return False

    card_html = conteudo[start:end]

    # alterar classe para passada (remove hora do card na lista)
    card_html = card_html.replace(
        'class="activity-card"',
        'class="activity-card activity-card--past"'
    )

    # remover do sítio atual
    sem_card = conteudo[:start] + conteudo[end:]

    # inserir em passadas
    if MARKER_PAST not in sem_card:
        print(f"\n❌ Marcador '{MARKER_PAST}' não encontrado.")
        return False

    fazer_backup(ACTIVITIES_HTML)
    novo = sem_card.replace(MARKER_PAST, MARKER_PAST + "\n" + card_html)
    ok = escrever_ficheiro(ACTIVITIES_HTML, novo)
    if ok:
        print(f"\n✅ Card '{pagina}' movido para Atividades Passadas.")
    return ok


# ──────────────────────────────────────────────────────────────
# FLUXOS PRINCIPAIS
# ──────────────────────────────────────────────────────────────

def criar_atividade():
    """Formulário interativo para criar uma nova atividade."""
    print("=" * 60)
    print("  ➕ NOVA ATIVIDADE")
    print("=" * 60)

    titulo = input("\nTítulo: ").strip()
    data   = input("Data (ex: 15 de Março de 2025): ").strip()
    hora   = input("Hora (ex: 14h00): ").strip()
    local  = input("Local: ").strip()
    vagas  = input("Vagas (ex: 30 | deixa em branco para omitir): ").strip()

    print("\n🖼  Foto principal (Google Drive)")
    foto_url = input("   URL ou ID da foto: ").strip()
    thumb = drive_url_para_thumbnail(foto_url)

    print("\n📝 Descrição da página da atividade")
    paragrafos = obter_paragrafos()

    fotos = obter_fotos()

    link_galeria = input(
        "\n📁 Link da pasta Google Drive com todas as fotos (Enter para omitir): "
    ).strip()

    email_inscricao = input(
        "\n📧 Email de inscrição (Enter para omitir botão de inscrição): "
    ).strip()

    activity_id = criar_id(titulo, data)
    pagina = f"atividade-{activity_id}.html"

    atividade = {
        "id":              activity_id,
        "titulo":          titulo,
        "data":            data,
        "hora":            hora,
        "local":           local,
        "vagas":           vagas,
        "thumb":           thumb,
        "paragrafos":      paragrafos if paragrafos else ["Descrição em breve."],
        "fotos":           fotos,
        "link_galeria": link_galeria,
        "inscricao_email": email_inscricao,
        "pagina":          pagina,
    }

    return atividade


def adicionar_atividade():
    """Cria a página individual e adiciona o card à lista."""
    atividade = criar_atividade()

    print("\n" + "=" * 60)
    print("  📊 RESUMO")
    print("=" * 60)
    print(f"  Título  : {atividade['titulo']}")
    print(f"  Data    : {atividade['data']}")
    print(f"  Hora    : {atividade['hora']}")
    print(f"  Local   : {atividade['local']}")
    print(f"  Página  : {atividade['pagina']}")
    print(f"  Fotos   : {len(atividade['fotos'])}")

    confirmar = input("\nConfirmar e criar? (s/n): ").strip().lower()
    if confirmar != 's':
        print("Operação cancelada.")
        return

    # 1. Criar ficheiro HTML da atividade
    html = gerar_pagina_atividade(atividade, "")
    if not escrever_ficheiro(atividade['pagina'], html):
        return
    print(f"\n✅ Página criada: {atividade['pagina']}")

    # 2. Adicionar card à lista
    if adicionar_card_na_lista(atividade, secao="upcoming"):
        print(f"✅ Card adicionado a {ACTIVITIES_HTML}")
    else:
        print(f"⚠️  Não foi possível adicionar o card à lista. Verifica os marcadores em {ACTIVITIES_HTML}.")


def mover_para_passadas():
    """Move uma atividade de 'Por vir' para 'Passadas'."""
    print("=" * 60)
    print("  🔁 MOVER PARA ATIVIDADES PASSADAS")
    print("=" * 60)
    pagina = input("\nNome do ficheiro da atividade (ex: atividade-churrasco-15-marco.html): ").strip()

    if not Path(pagina).exists():
        print(f"\n⚠️  O ficheiro '{pagina}' não existe. Continuas mesmo assim? (s/n): ", end="")
        if input().strip().lower() != 's':
            return

    mover_card_para_passadas(pagina)


def eliminar_atividade():
    """Remove o card da lista e apaga a página da atividade."""
    print("=" * 60)
    print("  🗑  ELIMINAR ATIVIDADE")
    print("=" * 60)
    pagina = input("\nNome do ficheiro da atividade (ex: atividade-churrasco-15-marco.html): ").strip()

    confirmar = input(f"\n⚠️  Isto eliminará o card e o ficheiro '{pagina}'. Confirmas? (s/n): ").strip().lower()
    if confirmar != 's':
        print("Operação cancelada.")
        return

    # remover card da lista
    if remover_card_da_lista(pagina):
        print(f"✅ Card removido de {ACTIVITIES_HTML}")
    else:
        print(f"⚠️  Card não encontrado em {ACTIVITIES_HTML}. Continuando...")

    # apagar ficheiro da atividade
    p = Path(pagina)
    if p.exists():
        p.unlink()
        print(f"✅ Ficheiro '{pagina}' eliminado.")
    else:
        print(f"⚠️  Ficheiro '{pagina}' não encontrado.")


# ──────────────────────────────────────────────────────────────
# MENU PRINCIPAL
# ──────────────────────────────────────────────────────────────

def menu():
    while True:
        print("\n" + "=" * 60)
        print("  🚀 GESTOR DE ATIVIDADES — NuAr")
        print("=" * 60)
        print("  1. ➕  Adicionar nova atividade")
        print("  2. 🔁  Mover atividade para 'Passadas'")
        print("  3. 🗑   Eliminar atividade")
        print("  4. ❌  Sair")

        opcao = input("\nOpção (1–4): ").strip()

        if opcao == "1":
            adicionar_atividade()
        elif opcao == "2":
            mover_para_passadas()
        elif opcao == "3":
            eliminar_atividade()
        elif opcao == "4":
            print("\n👋 Até breve!")
            break
        else:
            print("\n❌ Opção inválida.")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        raise
