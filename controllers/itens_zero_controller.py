import flet as ft
from models.itens_zero_model import ler_itens_zero, salvar_itens_zero, merge_itens


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


def popular_tabela(tabela: ft.DataTable, dados):
    tabela.rows.clear()
    for item in dados:
        tabela.rows.append(
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(item.get(c, ""))) for c in COLUNAS]
            )
        )


async def inserir_da_jtable(page: ft.Page, tabela: ft.DataTable):
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

    dados_existentes = ler_itens_zero()
    dados_atualizados = merge_itens(dados_existentes, novos_itens)

    salvar_itens_zero(dados_atualizados)
    popular_tabela(tabela, dados_atualizados)
    page.update()


def carregar_itens_zero(tabela: ft.DataTable, page: ft.Page):
    dados = ler_itens_zero()
    popular_tabela(tabela, dados)
    page.update()