import flet as ft
from controllers.digitar_ae_controller import criar_controller


def tela_digitar_ae(page: ft.Page):

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Gerar")),
            ft.DataColumn(ft.Text("Item")),
            ft.DataColumn(ft.Text("Descrição")),
            ft.DataColumn(ft.Text("Qtde")),
            ft.DataColumn(ft.Text("UM")),
            ft.DataColumn(ft.Text("Custo")),
            ft.DataColumn(ft.Text("Classificação fiscal")),
            ft.DataColumn(ft.Text("Classe de imposto")),
            ft.DataColumn(ft.Text("C-M")),
        ],
        rows=[],
        data_row_min_height=16,
        data_row_max_height=16,
        heading_row_height=18,
    )

    txt_conta = ft.TextField(label="Conta", width=200)
    txt_subconta = ft.TextField(label="SubConta", width=200)
    txt_cc = ft.TextField(label="CC", width=200)

    colar, executar, limpar = criar_controller(
        page,
        tabela,
        txt_conta,
        txt_subconta,
        txt_cc
    )

    btn_colar = ft.ElevatedButton(
        "Colar da JTable",
        bgcolor="blue",
        color="white",
        on_click=colar
    )

    btn_executar = ft.ElevatedButton(
        "Executar",
        bgcolor="green",
        color="white",
        on_click=executar
    )

    btn_limpar = ft.ElevatedButton(
        "Limpar tabela",
        bgcolor="red",
        color="white",
        on_click=limpar
    )

    return ft.Column(
        [
            ft.Row([txt_conta, txt_subconta, txt_cc]),
            ft.Divider(),
            ft.Row([btn_colar, btn_executar, btn_limpar]),
            ft.Divider(),
            ft.ListView([tabela], expand=True),
        ],
        expand=True,
    )
