import json
import re
from pathlib import Path
import re


def criar_id_atividade(titulo, data):
    """Cria um ID único baseado no título + data para evitar colisões."""
    base = f"{titulo}_{data}"
    return re.sub(r'[^a-z0-9]+', '_', base.lower()).strip('_')


def obter_fotos():
    """Obtém os links das fotos do Google Drive."""
    fotos = []
    print("\n📸 Adicionar Fotos do Google Drive")
    print("(Cole o link completo do Drive, ou apenas 'Enter' para terminar)")
    
    while True:
        url = input(f"\nFoto {len(fotos) + 1} - URL: ").strip()
        if not url:
            break
        
        caption = input(f"Foto {len(fotos) + 1} - Legenda: ").strip()
        fotos.append({"url": url, "caption": caption or f"Foto {len(fotos) + 1}"})
    
    return fotos


def obter_topicos():
    """Obtém a lista de tópicos do conteúdo estendido."""
    topicos = []
    print("\n📋 Adicionar Tópicos")
    print("(Escreve um tópico por linha, ou apenas 'Enter' para terminar)")
    
    while True:
        topico = input(f"\nTópico {len(topicos) + 1}: ").strip()
        if not topico:
            break
        topicos.append(topico)
    
    return topicos


def criar_atividade():
    """Formulário interativo para criar uma atividade."""
    print("=" * 60)
    print("🚀 GESTOR DE ATIVIDADES - NOVA ATIVIDADE")
    print("=" * 60)
    
    # Tipo de atividade
    print("\n📌 Tipo de Atividade:")
    print("1. Workshop")
    print("2. Competição")
    print("3. Palestra")
    print("4. Evento Social")
    tipo_opcao = input("Escolhe (1-4): ").strip()
    
    tipos = {
        "1": {"text": "📚 Workshop", "class": "workshop-badge"},
        "2": {"text": "🏆 Competição", "class": "competition-badge"},
        "3": {"text": "🎤 Palestra", "class": "talk-badge"},
        "4": {"text": "🎉 Evento Social", "class": "social-badge"}
    }
    badge = tipos.get(tipo_opcao, tipos["1"])
    
    # Informações básicas
    print("\n📝 Informações Básicas:")
    titulo = input("Título da atividade: ").strip()
    descricao = input("Descrição curta: ").strip()
    
    # Detalhes
    print("\n📅 Detalhes:")
    data = input("Data (ex: March 15, 2024): ").strip()
    hora = input("Horário (ex: 14:00 - 17:00): ").strip()
    local = input("Local (ex: NOVA FCT Campus): ").strip()
    
    # Fotos
    fotos = obter_fotos()
    
    # Conteúdo estendido
    print("\n📄 Conteúdo Estendido:")
    titulo_conteudo = input("Título da secção (ex: What You'll Learn): ").strip()
    conteudo_texto = input("Texto descritivo: ").strip()
    topicos = obter_topicos()
    
    # Criar ID único
    activity_id = criar_id_atividade(titulo, data)
    
    # Montar objeto da atividade
    atividade = {
        "id": activity_id,
        "badge": badge,
        "title": titulo,
        "description": descricao,
        "details": [
            {"icon": "📅", "text": data},
            {"icon": "🕐", "text": hora},
            {"icon": "📍", "text": local}
        ],
        "drivePhotos": fotos,
        "extendedContent": {
            "title": titulo_conteudo,
            "content": conteudo_texto,
            "topics": topicos
        }
    }
    
    return atividade


def gerar_html_card(atividade):
    """Gera o HTML do card da atividade."""
    return f'''
    <div class="activity-card" data-activity-id="{atividade['id']}">
        <div class="{atividade['badge']['class']} activity-badge">{atividade['badge']['text']}</div>
        <div class="activity-content">
            <h3 class="activity-title">{atividade['title']}</h3>
            <p class="activity-description">{atividade['description']}</p>
            
            <div class="activity-details">
                <div class="detail-item">
                    <span class="detail-icon">📅</span>
                    <span>{atividade['details'][0]['text']}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-icon">🕐</span>
                    <span>{atividade['details'][1]['text']}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-icon">📍</span>
                    <span>{atividade['details'][2]['text']}</span>
                </div>
            </div>
            
            <button class="register-btn" onclick="openModal('{atividade['id']}')">See More</button>
        </div>
    </div>
'''.strip("\n")


def gerar_js_data(atividade):
    """Gera o JavaScript da atividade para adicionar ao activityData."""
    fotos_js = ",\n                    ".join(
        [f'{{"url": "{foto["url"]}", "caption": "{foto["caption"]}"}}'
         for foto in atividade['drivePhotos']]
    )
    
    topicos_js = ",\n                        ".join(
        [f'"{topico}"' for topico in atividade['extendedContent']['topics']]
    )
    
    return f'''    {atividade['id']}: {{
        badge: {{ text: "{atividade['badge']['text']}", class: "{atividade['badge']['class']}" }},
        title: "{atividade['title']}",
        description: "{atividade['description']}",
        details: [
            {{ icon: "📅", text: "{atividade['details'][0]['text']}" }},
            {{ icon: "🕐", text: "{atividade['details'][1]['text']}" }},
            {{ icon: "📍", text: "{atividade['details'][2]['text']}" }}
        ],
        drivePhotos: [
            {fotos_js}
        ],
        extendedContent: {{
            title: "{atividade['extendedContent']['title']}",
            content: "{atividade['extendedContent']['content']}",
            topics: [
                {topicos_js}
            ]
        }}
    }},'''


def adicionar_ao_html(atividade, arquivo_html="activities copy.html"):
    """Adiciona a atividade ao arquivo HTML: card em 'Por vir' + JS em activityData."""
    try:
        with open(arquivo_html, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        html_card = gerar_html_card(atividade)
        js_data = gerar_js_data(atividade)

        # 1) Inserir card em 'Atividades por vir'
        card_marker = "<!-- ATIVIDADES_POR_VIR_MARKER -->"
        if card_marker in conteudo:
            # conteudo = conteudo.replace(
            #     card_marker,
            #     card_marker + "\n" + html_card
            # )
            indent = " " * 12  # 3 tabs se cada tab = 4 espaços
            card_indented = "\n".join(indent + linha if linha.strip() else linha
                                    for linha in html_card.splitlines())
            conteudo = conteudo.replace(
                card_marker,
                card_marker + "\n" + card_indented + "\n"
            )

        # 2) Inserir JS dentro de activityData
        js_marker = "// ATIVIDADES_JS_MARKER"
        if js_marker in conteudo:
            # conteudo = conteudo.replace(
            #     js_marker,
            #     js_data + "\n\n    " + js_marker
            # )
            indent = " " * 12  # 3 tabs se cada tab = 4 espaços
            card_indented = "\n".join(indent + linha if linha.strip() else linha
                                    for linha in js_data.splitlines())
            conteudo = conteudo.replace(
                js_marker,
                js_marker + "\n" + card_indented + "\n"
            )
        
        with open(arquivo_html, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        
        print(f"\n✅ Atividade adicionada com sucesso ao arquivo '{arquivo_html}'!")
        return True
    
    except FileNotFoundError:
        print(f"\n❌ Erro: Arquivo '{arquivo_html}' não encontrado!")
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        return False


# ===== Utilitários de procura / manipulação =====

def encontrar_atividade_por_titulo_data(conteudo, titulo, data):
    """
    Procura o id da atividade no JS (activityData) com base em título + data.
    Assume padrão:
        id: {
            ...
            title: "TITULO",
            ...
            details: [
                { icon: "📅", text: "DATA" },
                ...
            ],
            ...
        },
    """
    pattern = re.compile(
        r'^\s*([a-z0-9_]+):\s*\{'          # id: {
        r'(?:.|\n)*?title:\s*"' + re.escape(titulo) + r'"'  # title: "titulo"
        r'(?:.|\n)*?details:\s*\['         # details: [
        r'(?:.|\n)*?\{\s*icon:\s*"📅",\s*text:\s*"' + re.escape(data) + r'"'  # { icon:"📅", text:"data"
        r'(?:.|\n)*?\},',                  # até fechar esse objeto
        re.DOTALL | re.MULTILINE
    )
    m = pattern.search(conteudo)
    if not m:
        return None
    return m.group(1)


# Para o JS a estrutura é sempre semelhante também, por isso ele pode ir eliminando até chegar a "extendedContent: {", 
# depois elimini até encontrar "}" e depois sabe que só tem que eliminar a linha seguinte e já está tudo.
def remover_bloco_js_atividade(conteudo, activity_id):
    """
    Remove o bloco JS de uma atividade específica no activityData,
    desde 'id: {' até à vírgula após o '}' de fecho.
    """
    # 1) encontrar o início do id
    id_str = f"{activity_id}:"
    start_id = conteudo.find(id_str)
    if start_id == -1:
        print(f"⚠️ Nenhum bloco JS encontrado para id={activity_id} (id não encontrado)")
        return conteudo

    # 2) avançar até ao primeiro '{' depois do id (início do objeto)
    start_obj = conteudo.find("{", start_id)
    if start_obj == -1:
        print(f"⚠️ Nenhum '{{' encontrado após id={activity_id}")
        return conteudo

    # 3) percorrer contando { e } até fechar o objeto
    depth = 0
    i = start_obj
    n = len(conteudo)
    end_obj = None

    while i < n:
        ch = conteudo[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end_obj = i
                break
        i += 1

    if end_obj is None:
        print(f"⚠️ Não foi possível fechar o objeto JS para id={activity_id}")
        return conteudo

    # 4) incluir a vírgula e eventuais espaços / quebras de linha a seguir ao objeto
    j = end_obj + 1
    while j < n and conteudo[j].isspace():
        j += 1
    if j < n and conteudo[j] == ",":
        j += 1
        while j < n and conteudo[j].isspace():
            j += 1

    # remover desde o início do id até depois da vírgula seguinte
    return conteudo[:start_id] + conteudo[j:]

# Visto que estes blocos têm sempre a mesma estrutura, guiarmo-nos pelo numero de divs que já eliminámos
def remover_card_html(conteudo, activity_id):
    """Remove o <div class="activity-card" ...> com o data-activity-id dado, fechando pelo balanceamento de <div>."""
    marker = f'data-activity-id="{activity_id}"'
    start = conteudo.find(marker)
    if start == -1:
        print(f"⚠️ Nenhum card HTML encontrado para id={activity_id}")
        return conteudo

    # Ir até ao início do <div class="activity-card ...>
    div_start = conteudo.rfind('<div', 0, start)
    if div_start == -1:
        print(f"⚠️ Não foi encontrado <div> antes do data-activity-id para id={activity_id}")
        return conteudo

    # Contar divs até fechar o bloco
    i = div_start
    depth = 0
    n = len(conteudo)

    while i < n:
        # Próxima ocorrência de <div ou </div
        next_open = conteudo.find('<div', i)
        next_close = conteudo.find('</div', i)

        if next_open == -1 and next_close == -1:
            # Não há mais divs, aborta
            break

        # Decide qual vem primeiro
        if next_close == -1 or (next_open != -1 and next_open < next_close):
            # Encontrou um <div
            depth += 1
            i = next_open + 4
        else:
            # Encontrou um </div>
            depth -= 1
            i = next_close + 5  # len('</div') = 5

            if depth == 0:
                # Este </div> fecha o card inicial
                # avançar até ao '>' desta tag
                end_tag = conteudo.find('>', next_close)
                if end_tag == -1:
                    end_tag = next_close + 5
                end = end_tag + 1
                # remover o bloco completo
                return conteudo[:div_start] + conteudo[end:]

    print(f"⚠️ Não foi possível fechar o bloco <div> para id={activity_id}")
    return conteudo


def extrair_card_por_id(conteudo, activity_id):
    """Devolve (conteudo_sem_card, html_do_card) para o data-activity-id dado."""
    marker = f'data-activity-id="{activity_id}"'
    pos = conteudo.find(marker)
    if pos == -1:
        return conteudo, None

    # início do <div class="activity-card" ...>
    start = conteudo.rfind('<div', 0, pos)
    if start == -1:
        return conteudo, None

    # balancear <div> ... </div>
    i = start
    depth = 0
    n = len(conteudo)
    end = None

    while i < n:
        next_open = conteudo.find('<div', i)
        next_close = conteudo.find('</div', i)

        if next_open == -1 and next_close == -1:
            break

        if next_close == -1 or (next_open != -1 and next_open < next_close):
            depth += 1
            i = next_open + 4
        else:
            depth -= 1
            i = next_close + 5
            if depth == 0:
                # fechar este </div> (card completo)
                end = conteudo.find('>', next_close)
                if end == -1:
                    end = next_close + 5
                end += 1
                break

    if end is None:
        return conteudo, None

    card_html = conteudo[start:end]
    conteudo_sem = conteudo[:start] + conteudo[end:]
    return conteudo_sem, card_html


def mover_card_entre_grids(conteudo, activity_id, origem_marker, destino_marker):
    """Move o card com id de uma grid para outra."""
    conteudo_sem, card_html = extrair_card_por_id(conteudo, activity_id)
    if card_html is None:
        print(f"⚠️ Card não encontrado para id={activity_id}")
        return conteudo, False

    if destino_marker not in conteudo_sem:
        print("⚠️ Marcador de destino não encontrado.")
        return conteudo, False

    # opcional: identação (3 tabs / 12 espaços)
    indent = " " * 12
    card_indented = "\n".join(indent + linha if linha.strip() else linha
                              for linha in card_html.splitlines())

    conteudo_final = conteudo_sem.replace(
        destino_marker,
        destino_marker + "\n" + card_indented
    )
    return conteudo_final, True


def mover_para_passadas(titulo, data, arquivo_html="activities copy.html"):
    """Move uma atividade de 'Por vir' para 'Passadas' com base em título + data."""
    try:
        with open(arquivo_html, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # encontrar id pelo HTML (card)
        activity_id = encontrar_id_por_titulo_data_html(conteudo, titulo, data)
        print("DEBUG mover_para_passadas ID encontrado:", repr(activity_id))

        if not activity_id:
            print("\n❌ Atividade não encontrada (verifica título e data).")
            return False
        
        origem_marker = "<!-- ATIVIDADES_POR_VIR_MARKER -->"
        destino_marker = "<!-- ATIVIDADES_PASSADAS_MARKER -->"
        
        conteudo_novo, ok = mover_card_entre_grids(
            conteudo, activity_id, origem_marker, destino_marker
        )
        if not ok:
            print("\n❌ Não foi possível mover o card (marcadores não encontrados).")
            return False
        
        with open(arquivo_html, 'w', encoding='utf-8') as f:
            f.write(conteudo_novo)
        
        print(f"\n✅ Atividade '{titulo}' movida para 'Atividades Passadas'.")
        return True
    
    except FileNotFoundError:
        print(f"\n❌ Erro: Arquivo '{arquivo_html}' não encontrado!")
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        return False


def encontrar_id_por_titulo_data_html(conteudo, titulo, data):
    """
    Procura um <div class="activity-card" ... data-activity-id="X">
    que contenha:
      <h3 class="activity-title">titulo</h3>
      ...
      <span class="detail-icon">📅</span>
      <span>data</span>
    e devolve X.
    """
    pattern = re.compile(
        r'<div\s+class="activity-card"[^>]*data-activity-id="([^"]+)"[^>]*>'  # abre o card e captura o id
        r'(?:(?!<div\s+class="activity-card").)*?'                           # conteúdo até antes do próximo card
        r'<h3\s+class="activity-title">\s*' + re.escape(titulo) + r'\s*</h3>'  # título certo
        r'(?:(?!<div\s+class="activity-card").)*?'                           # ainda dentro do mesmo card
        r'<span\s+class="detail-icon">📅</span>\s*'
        r'<span>\s*' + re.escape(data) + r'\s*</span>',
        re.DOTALL
    )
    m = pattern.search(conteudo)
    if not m:
        return None
    return m.group(1)


def eliminar_atividade(titulo, data, arquivo_html="activities copy.html"):
    """Elimina uma atividade (card em qualquer grid + bloco JS) por título + data."""
    try:
        with open(arquivo_html, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        # 1) obter o id a partir do HTML (card)
        activity_id = encontrar_id_por_titulo_data_html(conteudo, titulo, data)
        print("DEBUG activity_id encontrado:", repr(activity_id))

        if not activity_id:
            print("\n❌ Atividade não encontrada (verifica título e data exatamente como aparecem no card).")
            return False

        # 2) remover card em qualquer secção
        conteudo = remover_card_html(conteudo, activity_id)

        # 3) remover bloco JS em activityData
        conteudo = remover_bloco_js_atividade(conteudo, activity_id)

        with open(arquivo_html, 'w', encoding='utf-8') as f:
            f.write(conteudo)

        print(f"\n✅ Atividade '{titulo}' eliminada (HTML + JS).")
        return True

    except FileNotFoundError:
        print(f"\n❌ Erro: Arquivo '{arquivo_html}' não encontrado!")
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        return False



# ===== Menu principal =====

def menu_principal():
    """Menu principal do gestor."""
    while True:
        print("\n" + "=" * 60)
        print("🚀 GESTOR DE ATIVIDADES - MENU PRINCIPAL")
        print("=" * 60)
        print("1. ➕ Adicionar nova atividade (Atividades por vir)")
        print("2. 🔁 Mover atividade de 'Por vir' para 'Passadas'")
        print("3. 🗑  Eliminar atividade")
        print("4. ❌ Sair")
        
        opcao = input("\nEscolhe uma opção (1-4): ").strip()
        
        if opcao == "1":
            atividade = criar_atividade()
            
            print("\n" + "=" * 60)
            print("📊 RESUMO DA ATIVIDADE")
            print("=" * 60)
            print(f"ID: {atividade['id']}")
            print(f"Título: {atividade['title']}")
            print(f"Tipo: {atividade['badge']['text']}")
            print(f"Data: {atividade['details'][0]['text']}")
            print(f"Fotos: {len(atividade['drivePhotos'])}")
            print(f"Tópicos: {len(atividade['extendedContent']['topics'])}")
            
            confirmar = input("\n✅ Adicionar ao HTML? (s/n): ").strip().lower()
            if confirmar == 's':
                arquivo = input("Nome do arquivo HTML (ou Enter para 'activities copy.html'): ").strip()
                if not arquivo:
                    arquivo = "activities copy.html"
                adicionar_ao_html(atividade, arquivo)
        
        elif opcao == "2":
            print("\n🔁 Mover atividade para 'Atividades Passadas':")
            titulo = input("Título exato da atividade: ").strip()
            data = input("Data exata (como aparece no card, ex: March 15, 2024): ").strip()
            arquivo = input("Nome do arquivo HTML (ou Enter para 'activities copy.html'): ").strip()
            if not arquivo:
                arquivo = "activities copy.html"
            mover_para_passadas(titulo, data, arquivo)
        
        elif opcao == "3":
            print("\n🗑 Eliminar atividade:")
            titulo = input("Título exato da atividade: ").strip()
            data = input("Data exata (como aparece no card): ").strip()
            arquivo = input("Nome do arquivo HTML (ou Enter para 'activities copy.html'): ").strip()
            if not arquivo:
                arquivo = "activities copy.html"
            eliminar_atividade(titulo, data, arquivo)
        
        elif opcao == "4":
            print("\n👋 Até breve!")
            break
        
        else:
            print("\n❌ Opção inválida!")


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido. Até breve!")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
