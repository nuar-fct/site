import re
from pathlib import Path

HTML_PATH = Path("recrutamento.html")

SECTIONS = {
    "1": {"name": "Informações básicas", "marker": "<!-- BASIC_MARKER -->", "prefix": "basic", "section_id": "BASIC-section"},
    "2": {"name": "Projeto ASTRO",        "marker": "<!-- ASTRO_MARKER -->", "prefix": "astro", "section_id": "ASTRO-section"},
    "3": {"name": "Projeto NSS",          "marker": "<!-- NSS_MARKER -->",   "prefix": "nss",   "section_id": "NSS-section"},
    "4": {"name": "Projeto STAR",         "marker": "<!-- STAR_MARKER -->",  "prefix": "star",  "section_id": "STAR-section"},
}


def carregar_html() -> str:
    return HTML_PATH.read_text(encoding="utf-8")


def gravar_html(conteudo: str) -> None:
    HTML_PATH.write_text(conteudo, encoding="utf-8")


def slugify(texto: str) -> str:
    base = texto.strip().lower()
    base = re.sub(r"[^a-z0-9]+", "_", base)
    return base.strip("_") or "pergunta"


def escolher_secao() -> dict:
    while True:
        print("\nLocal a inserir/remover:")
        for key, sec in SECTIONS.items():
            print(f"{key}. {sec['name']}")
        op = input("Opção: ").strip()
        if op in SECTIONS:
            return SECTIONS[op]
        print("Opção inválida.")


def escolher_tipo() -> str:
    while True:
        print("\nTipo de pergunta:")
        print("1. Resposta curta")
        print("2. Resposta longa")
        print("3. Checkboxes")
        print("4. Dropdown")
        op = input("Opção (1-4): ").strip()

        if op == "1":
            return "short"
        if op == "2":
            return "long"
        if op == "3":
            return "checkbox"
        if op == "4":
            return "dropdown"
        print("Opção inválida.")


def obter_opcoes() -> list[str]:
    opcoes = []
    print("\nOpções (uma por linha, Enter para terminar):")
    while True:
        opt = input(f"  Opção {len(opcoes) + 1}: ").strip()
        if not opt:
            break
        opcoes.append(opt)
    return opcoes


def criar_pergunta():
    print("\n=== NOVA PERGUNTA ===")
    secao = escolher_secao()
    tipo = escolher_tipo()
    label = input("Texto da pergunta (label): ").strip()
    obrigatoria = input("Obrigatória? (s/n): ").strip().lower() == "s"

    qid_base = slugify(label)
    qid = f"{secao['prefix']}_{qid_base}"

    opcoes = []
    if tipo in ("checkbox", "dropdown"):
        opcoes = obter_opcoes()

    pergunta = {
        "id": qid,
        "label": label,
        "required": obrigatoria,
        "tipo": tipo,
        "options": opcoes,
        "section": secao,
    }
    return pergunta


# ------- geradores HTML -------

def gerar_html_short(p: dict) -> str:
    req_star = " *" if p["required"] else ""
    req_attr = " required" if p["required"] else ""
    return f'''
        <div class="form-group">
            <label>{p["label"]}{req_star}</label>
            <input type="text" id="{p["id"]}" name="{p["id"]}"{req_attr}>
        </div>
    '''.rstrip()


def gerar_html_long(p: dict) -> str:
    req_star = " *" if p["required"] else ""
    req_attr = " required" if p["required"] else ""
    return f'''
        <div class="form-group">
            <label>{p["label"]}{req_star}</label>
            <textarea id="{p["id"]}" name="{p["id"]}" rows="4"{req_attr}></textarea>
        </div>
    '''.rstrip()


def gerar_html_dropdown(p: dict) -> str:
    req_star = " *" if p["required"] else ""
    req_attr = " required" if p["required"] else ""
    options_html = "\n".join(
        f'                <option value="{opt}">{opt}</option>'
        for opt in p["options"]
    )
    return f'''
        <div class="form-group">
            <label>{p["label"]}{req_star}</label>
            <select id="{p["id"]}" name="{p["id"]}"{req_attr}>
                <option value="">-- Seleciona --</option>
{options_html}
            </select>
        </div>
    '''.rstrip()


def gerar_html_checkbox(p: dict) -> str:
    options_html = "\n".join(
        f'''                        <label class="checkbox-label">
                            <input type="checkbox" name="{p["id"]}" value="{opt}">
                            <span class="checkbox-text">{opt}</span>
                        </label>'''
        for opt in p["options"]
    )

    return f'''
        <div class="form-group">
            <label>{p["label"]}</label>
            <div class="checkbox-group">
{options_html}
            </div>
        </div>
    '''.rstrip()


def gerar_html_pergunta(p: dict) -> str:
    if p["tipo"] == "short":
        return gerar_html_short(p)
    if p["tipo"] == "long":
        return gerar_html_long(p)
    if p["tipo"] == "checkbox":
        return gerar_html_checkbox(p)
    if p["tipo"] == "dropdown":
        return gerar_html_dropdown(p)
    raise ValueError("Tipo de pergunta inválido")


# ------- inserção / remoção -------

def inserir_na_secao(pergunta: dict, bloco_html: str) -> None:
    marker = pergunta["section"]["marker"]
    conteudo = carregar_html()

    idx = conteudo.find(marker)
    if idx == -1:
        raise RuntimeError(f"Marcador {marker} não encontrado no HTML.")

    indent = " " * 8  # ajusta aqui se quiseres outro nível
    bloco_indentado = "\n".join(
        indent + linha if linha.strip() else linha
        for linha in bloco_html.splitlines()
    )

    novo_conteudo = conteudo[:idx] + bloco_indentado + "\n" + conteudo[idx:]
    gravar_html(novo_conteudo)


def remover_pergunta_por_label(secao: dict, label_text: str) -> bool:
    """
    Remove o <div class="form-group"> cujo <label>Texto</label> corresponde
    ao label_text, dentro da secção indicada.
    """
    conteudo = carregar_html()

    # localizar início e fim aproximados da secção (pelo id do <section>)
    sec_id = secao["section_id"]
    sec_start = conteudo.find(f'<section id="{sec_id}"')
    if sec_start == -1:
        print(f"⚠ Secção '{secao['name']}' (id={sec_id}) não encontrada.")
        return False

    sec_end = conteudo.find("</section>", sec_start)
    if sec_end == -1:
        print(f"⚠ Fecho </section> não encontrado para '{secao['name']}'.")
        return False
    sec_end += len("</section>")

    sec_html = conteudo[sec_start:sec_end]

    # procurar o label dentro da secção
    label_pattern = f"<label>{label_text}</label>"
    label_pos = sec_html.find(label_pattern)
    if label_pos == -1:
        print(f"⚠ Pergunta com label '{label_text}' não encontrada na secção '{secao['name']}'.")
        return False

    # recuar até ao início do <div class="form-group">
    div_start = sec_html.rfind('<div class="form-group"', 0, label_pos)
    if div_start == -1:
        print("⚠ Não foi encontrado <div class=\"form-group\"> antes do label.")
        return False

    # avançar até fechar esse div (balanceando <div> / </div>)
    i = div_start
    depth = 0
    n = len(sec_html)
    div_end = None

    while i < n:
        next_open = sec_html.find("<div", i)
        next_close = sec_html.find("</div", i)

        if next_open == -1 and next_close == -1:
            break

        if next_close == -1 or (next_open != -1 and next_open < next_close):
            depth += 1
            i = next_open + 4
        else:
            depth -= 1
            i = next_close + 5  # len("</div") = 5
            if depth == 0:
                # fecha o div inicial
                end_tag = sec_html.find(">", next_close)
                if end_tag == -1:
                    end_tag = next_close + 5
                div_end = end_tag + 1
                break

    if div_end is None:
        print("⚠ Não foi possível determinar o fim do bloco <div class=\"form-group\">.")
        return False

    # remover o bloco dessa secção
    novo_sec_html = sec_html[:div_start] + sec_html[div_end:]

    # limpar linhas em branco duplicadas resultantes da remoção
    # (remove linhas que só tenham espaços/tabs entre \n\n)
    # novo_sec_html = re.sub(r"\n[ \t]*\n[ \t]*\n[ \t]*\n", "\n\n", novo_sec_html)
    novo_sec_html = re.sub(r"\n[ \t]*\n+", "\n", novo_sec_html)


    # remontar o HTML completo
    novo_conteudo = conteudo[:sec_start] + novo_sec_html + conteudo[sec_end:]
    gravar_html(novo_conteudo)
    return True


def menu():
    while True:
        print("\n=== GESTOR FORMULÁRIO NUAR ===")
        print("1. Adicionar pergunta")
        print("2. Remover pergunta")
        print("3. Sair")
        op = input("Opção: ").strip()

        if op == "1":
            pergunta = criar_pergunta()
            bloco = gerar_html_pergunta(pergunta)
            inserir_na_secao(pergunta, bloco)
            print(f"\n✅ Pergunta '{pergunta['label']}' adicionada em {pergunta['section']['name']}.")
        elif op == "2":
            print("\n=== REMOVER PERGUNTA ===")
            secao = escolher_secao()
            label = input("Texto exato do label da pergunta a remover: ").strip()
            ok = remover_pergunta_por_label(secao, label)
            if ok:
                print(f"\n✅ Pergunta '{label}' removida de {secao['name']}.")
            else:
                print(f"\n❌ Não foi possível remover '{label}' de {secao['name']}.")
        elif op == "3":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
