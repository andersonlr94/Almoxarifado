
import flet as ft
from datetime import datetime


def tela_prog_agulhas(page, ler_dados, salvar_no_arquivo, obter_pasta_dados):

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Sel")),
            ft.DataColumn(ft.Text("Pedido")),
            ft.DataColumn(ft.Text("Kardex")),
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Descrição")),
            ft.DataColumn(ft.Text("Qtde")),
            ft.DataColumn(ft.Text("Status")),
        ],
        rows=[]
    )

    btn_programar = ft.ElevatedButton(
        "Mudar p/ Programado",
        bgcolor="blue",
        color="white",
        visible=False
    )

    btn_separar = ft.ElevatedButton(
        "Mudar p/ Separando",
        bgcolor="orange",
        color="white",
        visible=False
    )

    btn_entregar = ft.ElevatedButton(
        "Mudar p/ Entregue",
        bgcolor="green",
        color="white",
        visible=False
    )

    # =================================================
    # FUNÇÕES INTERNAS
    # =================================================

    def carregar_tabela(filtro_status="Pendente"):
        dados = ler_dados()
        tabela.rows.clear()

        btn_programar.visible = (filtro_status == "Pendente")
        btn_separar.visible = (filtro_status in ["Pendente", "Programado"])
        btn_entregar.visible = (filtro_status == "Separando")

        for item in dados:
            status_item = str(item.get("status", ""))

            mostrar = False
            if filtro_status == "Entregue":
                mostrar = status_item.startswith("Entregue")
            elif status_item == filtro_status:
                mostrar = True

            if mostrar:
                tabela.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Checkbox(value=False)),
                            ft.DataCell(ft.Text(item.get("pedido", ""))),
                            ft.DataCell(ft.Text(item.get("kardex", ""))),
                            ft.DataCell(ft.Text(item.get("codigo", ""))),
                            ft.DataCell(ft.Text(item.get("descricao", ""))),
                            ft.DataCell(ft.Text(item.get("qtde", ""))),
                            ft.DataCell(ft.Text(status_item)),
                        ]
                    )
                )

        page.update()

    def atualizar_status(novo_status):
        dados = ler_dados()
        alterou = False
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

        for row in tabela.rows:
            if row.cells[0].content.value:
                pedido = row.cells[1].content.value
                codigo = row.cells[3].content.value

                for item in dados:
                    if str(item.get("pedido")) == str(pedido) and str(item.get("codigo")) == str(codigo):

                        if novo_status == "Entregue":
                            item["status"] = f"Entregue em {data_hora}"
                        else:
                            item["status"] = novo_status

                        alterou = True

        if alterou:
            salvar_no_arquivo(dados)
            carregar_tabela()
            page.snack_bar = ft.SnackBar(ft.Text(f"Status atualizado para: {novo_status}"))
            page.snack_bar.open = True
            page.update()

    # Conectar botões às funções
    btn_programar.on_click = lambda _: atualizar_status("Programado")
    btn_separar.on_click = lambda _: atualizar_status("Separando")
    btn_entregar.on_click = lambda _: atualizar_status("Entregue")

    # =================================================
    # LAYOUT
    # =================================================

    if not obter_pasta_dados():
        return ft.Text(
            "Configure a pasta de dados primeiro.",
            size=18,
            color="red"
        )

    carregar_tabela("Pendente")

    return ft.Column(
        [
            ft.Row(
                [
                    ft.ElevatedButton("Pendentes", on_click=lambda _: carregar_tabela("Pendente")),
                    ft.ElevatedButton("Programados", on_click=lambda _: carregar_tabela("Programado")),
                    ft.ElevatedButton("Separando", on_click=lambda _: carregar_tabela("Separando")),
                    ft.ElevatedButton("Entregues", on_click=lambda _: carregar_tabela("Entregue")),
                ],
                scroll=ft.ScrollMode.ADAPTIVE
            ),
            ft.Divider(),
            ft.ListView([tabela], expand=True),
            ft.Divider(),
            ft.Row([btn_programar, btn_separar, btn_entregar], alignment="center")
        ],
        expand=True
    )
