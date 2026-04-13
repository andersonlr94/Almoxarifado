import flet as ft

from models.itens_zero_model import (
    ler_itens_zero,
    salvar_itens_zero,
    sync_itens,
)

# ------------------------------------------------------------
# COLUNAS DA TABELA
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

# ------------------------------------------------------------
# ATUALIZAR CAMPO (DPP / OBSERVAÇÃO)
# ------------------------------------------------------------
def atualizar_campo(kardex, codigo, campo, novo_valor):
    dados = ler_itens_zero()
    alterou = False

    for item in dados:
        if item.get("Kardex") == kardex and item.get("Código") == codigo:
            item[campo] = novo_valor
            alterou = True
            break

    if alterou:
        salvar_itens_zero(dados)

    return alterou

# ------------------------------------------------------------
# CÉLULA EDITÁVEL (GENÉRICA)
# ------------------------------------------------------------
def criar_celula_editavel(
    campo_nome,
    valor_atual,
    kardex,
    codigo,
    tabela,
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
            content_padding=1,
        )

        async def sair_edicao(ev):
            novo_valor = campo.value.strip()
            atualizar_campo(kardex, codigo, campo_nome, novo_valor)

            dados = ler_itens_zero()
            popular_tabela(tabela, dados, page)
            page.update()

        campo.on_submit = sair_edicao
        campo.on_blur = sair_edicao

        e.control.content = campo
        page.update()

    return ft.Container(
        content=texto,
        padding=2,
        on_click=entrar_edicao,
    )

# ------------------------------------------------------------
# POPULAR TABELA
# ------------------------------------------------------------
def popular_tabela(tabela: ft.DataTable, dados, txt_contador, page: ft.Page):
    tabela.rows.clear()

    if not dados:
        txt_contador.value = "Total: 0 itens"
        page.update()
        return

    for item in dados:
        cells = []
        kardex = item.get("Kardex", "")
        codigo = item.get("Código", "")

        for coluna in COLUNAS:
            if coluna in ("DPP", "Observação"):
                largura = 140 if coluna == "DPP" else 260
                cells.append(
                    ft.DataCell(
                        criar_celula_editavel(
                            coluna,
                            item.get(coluna, ""),
                            kardex,
                            codigo,
                            tabela,
                            page,
                            largura,
                        )
                    )
                )
            else:
                cells.append(
                    ft.DataCell(ft.Text(item.get(coluna, ""), size=10, no_wrap=True,))
                )

        txt_contador.value = f"Total: {len(dados)} itens"
        tabela.rows.append(ft.DataRow(cells=cells))

# ------------------------------------------------------------
# INSERIR ITENS DA JTABLE
# ------------------------------------------------------------
async def inserir_da_jtable(page: ft.Page, tabela: ft.DataTable, txt_contador: ft.Text):
    texto = await page.clipboard.get()
    if not texto:
        return

    linhas = [l for l in texto.splitlines() if l.strip()]
    novos_itens = []

    for linha in linhas:
        cols = linha.split("\t")
        while len(cols) < 11:
            cols.append("")

        item = {
            "Item de estoque": cols[0],
            "Kardex": cols[1],
            "Código": cols[2],
            "Descrição": cols[3],
            "Equipamento": cols[4],
            "Total estoque": cols[5],
            "Estratégico": cols[6],
            "Cons Médio": cols[7],
            "Estoque Máx": cols[8],
            "Qtde Prog": cols[9],
            "Status": cols[10],
            "DPP": "",
            "Observação": "",
        }

        novos_itens.append(item)

    dados_existentes = ler_itens_zero() or []
    dados_atualizados = sync_itens(dados_existentes, novos_itens)

    salvar_itens_zero(dados_atualizados)
    popular_tabela(tabela, dados_atualizados, txt_contador, page)
    page.update()

# ------------------------------------------------------------
# CARREGAR ITENS SALVOS
# ------------------------------------------------------------
def carregar_itens_zero(tabela: ft.DataTable, txt_contador: ft.Text, page: ft.Page):
    dados = ler_itens_zero()
    popular_tabela(tabela, dados, txt_contador, page)
    page.update()