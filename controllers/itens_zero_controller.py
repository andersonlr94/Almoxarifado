import flet as ft
from models.itens_zero_model import (
    ler_itens_zero,
    salvar_itens_zero,
    sync_itens,
)

# ------------------------------------------------------------
# COLUNAS
# ------------------------------------------------------------

COLUNAS = [
    "Item de estoque",
    "Kardex",
    "Código",
    "Descrição",
    "Equipamento",
    "Total estoque",
    "Estratégico",
    "Cons Médio",
    "Estoque Máx",
    "Qtde Prog",
    "Status",
    "DPP",
    "Observação",
]

COLUNAS_VISIVEIS = [
    "Kardex",
    "Código",
    "Descrição",
    "Estratégico",
    "Cons Médio",
    "Estoque Máx",
    "Qtde Prog",
    "Status",
    "DPP",
    "Observação",
    "CorMenu",
]

# mapa: (kardex, codigo) -> DataRow
MAPA_LINHAS = {}

# ------------------------------------------------------------
# ATUALIZAR CAMPO
# ------------------------------------------------------------

def atualizar_campo(kardex, codigo, campo, novo_valor):
    dados = ler_itens_zero()
    for item in dados:
        if item.get("Kardex") == kardex and item.get("Código") == codigo:
            item[campo] = novo_valor
            salvar_itens_zero(dados)
            return True
    return False

# ------------------------------------------------------------
# COR DA LINHA
# ------------------------------------------------------------

def cor_da_linha(item):
    cor = (item.get("Cor") or "").lower().strip()
    return {
        "azul": ft.Colors.BLUE_50,
        "vermelho": ft.Colors.RED_50,
        "amarelo": ft.Colors.YELLOW_50,
        "verde": ft.Colors.GREEN_50,
    }.get(cor)

# ------------------------------------------------------------
# ATUALIZAR COR DO ITEM (única versão)
# ------------------------------------------------------------

def atualizar_cor_item(kardex, codigo, nova_cor):
    dados = ler_itens_zero()
    for item in dados:
        if item.get("Kardex") == kardex and item.get("Código") == codigo:
            item["Cor"] = nova_cor
            salvar_itens_zero(dados)
            break

# ------------------------------------------------------------
# ESCOLHER COR
# ------------------------------------------------------------

def escolher(cor, kardex, codigo, tabela):
    atualizar_cor_item(kardex, codigo, cor)

    row = MAPA_LINHAS.get((kardex, codigo))
    if row:
        row.color = cor_da_linha({"Cor": cor})
        tabela.update()

# ------------------------------------------------------------
# MENU DE CORES
# ------------------------------------------------------------

def menu_cor_item(kardex, codigo, tabela):
    # cor atual do item (vem do JSON)
    dados = ler_itens_zero()
    item = next(
        (i for i in dados if i.get("Kardex") == kardex and i.get("Código") == codigo),
        None,
    )
    cor_atual = (item.get("Cor") if item else "") or ""

    COR_ICONE = {
        "azul": ft.Colors.BLUE,
        "vermelho": ft.Colors.RED,
        "amarelo": ft.Colors.YELLOW,
        "verde": ft.Colors.GREEN,
        "": ft.Colors.GREY_600,
    }

    # botão que vamos atualizar depois
    botao = ft.PopupMenuButton(
        icon=ft.Icons.CIRCLE,
        icon_size=14,
        icon_color=COR_ICONE.get(cor_atual, ft.Colors.GREY_600),
        padding=0,
        items=[],
    )

    # função interna: escolhe cor E atualiza o ícone
    def escolher_cor(cor):
        atualizar_cor_item(kardex, codigo, cor)

        # atualiza a linha
        row = MAPA_LINHAS.get((kardex, codigo))
        if row:
            row.color = cor_da_linha({"Cor": cor})
            tabela.update()

        # atualiza o ícone do menu
        botao.icon_color = COR_ICONE.get(cor, ft.Colors.GREY_600)
        botao.update()

    # popula os itens do menu
    botao.items = [
        ft.PopupMenuItem(
            content=ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.GREEN),
            on_click=lambda e: escolher_cor("verde"),
        ),
        ft.PopupMenuItem(
            content=ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.YELLOW),
            on_click=lambda e: escolher_cor("amarelo"),
        ),
        ft.PopupMenuItem(
            content=ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.RED),
            on_click=lambda e: escolher_cor("vermelho"),
        ),
        ft.PopupMenuItem(
            content=ft.Icon(ft.Icons.CIRCLE, color=ft.Colors.BLUE),
            on_click=lambda e: escolher_cor("azul"),
        ),
        ft.PopupMenuItem(
            content=ft.Text("Sem cor"),
            on_click=lambda e: escolher_cor(""),
        ),
    ]

    return botao
# ------------------------------------------------------------
# POPULAR TABELA
# ------------------------------------------------------------

def popular_tabela(tabela: ft.DataTable, dados, txt_contador, page: ft.Page):
    tabela.rows.clear()
    MAPA_LINHAS.clear()

    for item in dados:
        cells = []
        kardex = item.get("Kardex", "")
        codigo = item.get("Código", "")

        for coluna in COLUNAS_VISIVEIS:

            # ------------------------------------
            # COLUNA DO MENU DE CORES
            # ------------------------------------
            if coluna == "CorMenu":
                cells.append(
                    ft.DataCell(
                        ft.Row(
                            controls=[menu_cor_item(kardex, codigo, tabela)],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            expand=True,
                        )
                    )
                )
                continue

            # ------------------------------------
            # CAMPOS EDITÁVEIS (DPP / OBSERVAÇÃO)
            # ------------------------------------
            elif coluna in ("DPP", "Observação"):
                largura = 140 if coluna == "DPP" else 260
                cells.append(
                    ft.DataCell(
                        criar_celula_editavel(
                            coluna,
                            item.get(coluna, ""),
                            kardex,
                            codigo,
                            tabela,
                            txt_contador,
                            page,
                            largura,
                        )
                    )
                )

            # ------------------------------------
            # CAMPOS NORMAIS
            # ------------------------------------
            else:
                cells.append(
                    ft.DataCell(
                        ft.Text(
                            str(item.get(coluna, "")),
                            size=12,
                            no_wrap=True,
                        )
                    )
                )

        # ✅ AQUI ESTAVA FALTANDO TUDO ISSO
        row = ft.DataRow(
            color=cor_da_linha(item),
            cells=cells,
        )

        MAPA_LINHAS[(kardex, codigo)] = row
        tabela.rows.append(row)

    txt_contador.value = f"Total: {len(dados)} itens"
    page.update()

# ------------------------------------------------------------
# CARREGAR ITENS
# ------------------------------------------------------------

def carregar_itens_zero(tabela, txt_contador, page):
    dados = ler_itens_zero()
    popular_tabela(tabela, dados, txt_contador, page)

    # ------------------------------------------------------------
# INSERIR ITENS DA JTABLE (placeholder – será expandido depois)
# ------------------------------------------------------------

async def inserir_da_jtable(
    page: ft.Page,
    tabela: ft.DataTable,
    txt_contador: ft.Text,
):
    """
    Função mantida para compatibilidade com a VIEW.
    Implementação completa pode ser feita depois.
    """
    pass

# ------------------------------------------------------------
# COPIAR TABELA PARA CLIPBOARD (placeholder obrigatório)
# ------------------------------------------------------------
async def copiar_tabela_para_clipboard(
    page: ft.Page,
    tabela: ft.DataTable,
):
    """
    Função mantida para compatibilidade com a VIEW.
    Implementação real será feita depois.
    """
    pass

# ------------------------------------------------------------
# CÉLULA EDITÁVEL (DPP / OBSERVAÇÃO) – RESTAURAÇÃO NECESSÁRIA
# ------------------------------------------------------------

def criar_celula_editavel(
    campo_nome,
    valor_atual,
    kardex,
    codigo,
    tabela,
    txt_contador,
    page,
    largura=180,
):
    texto = ft.Text(valor_atual or "", size=12)

    def entrar_edicao(e):
        campo = ft.TextField(
            value=valor_atual or "",
            autofocus=True,
            width=largura,
            text_size=10,
            height=20,
            dense=True,
            content_padding=2,
        )

        async def sair_edicao(ev):
            novo_valor = campo.value.strip()
            atualizar_campo(kardex, codigo, campo_nome, novo_valor)

            # recarrega a tabela para refletir o novo valor
            carregar_itens_zero(tabela, txt_contador, page)

        campo.on_submit = sair_edicao
        campo.on_blur = sair_edicao

        e.control.content = campo
        page.update()

    return ft.Container(
        content=texto,
        padding=2,
        on_click=entrar_edicao,
    )