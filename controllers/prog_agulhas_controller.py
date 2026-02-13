import flet as ft
from models.prog_agulhas_model import filtrar_dados, atualizar_status_model


def criar_controller(page, tabela, ler_dados, salvar_no_arquivo):

    def carregar_tabela(filtro_status="Pendente"):
        dados = ler_dados()
        tabela.rows.clear()

        dados_filtrados = filtrar_dados(dados, filtro_status)

        for item in dados_filtrados:
            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Checkbox(value=False)),
                        ft.DataCell(ft.Text(item.get("pedido", ""))),
                        ft.DataCell(ft.Text(item.get("kardex", ""))),
                        ft.DataCell(ft.Text(item.get("codigo", ""))),
                        ft.DataCell(ft.Text(item.get("descricao", ""))),
                        ft.DataCell(ft.Text(item.get("qtde", ""))),
                        ft.DataCell(ft.Text(item.get("status", ""))),
                    ]
                )
            )

        page.update()

    def atualizar_status(novo_status):
        dados = ler_dados()

        selecionados = []

        for row in tabela.rows:
            if row.cells[0].content.value:
                pedido = row.cells[1].content.value
                codigo = row.cells[3].content.value
                selecionados.append((pedido, codigo))

        novos_dados, alterou = atualizar_status_model(
            dados,
            selecionados,
            novo_status
        )

        if alterou:
            salvar_no_arquivo(novos_dados)
            carregar_tabela()
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Status atualizado para: {novo_status}")
            )
            page.snack_bar.open = True
            page.update()

    return carregar_tabela, atualizar_status
