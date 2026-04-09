import flet as ft
from controllers.itens_zero_controller import (
    inserir_da_jtable,
    carregar_itens_zero,
    COLUNAS,
)


def tela_itens_zero(page: ft.Page):

    titulo = ft.Text(
        "Estoque Zero",
        size=26,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_800,
    )

    tabela = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(c)) for c in COLUNAS],
        rows=[],
        expand=True,
        column_spacing=14,
    )

    
    async def on_inserir_click(e):
        await inserir_da_jtable(page, tabela)

    
    btn_inserir = ft.ElevatedButton(
        "Inserir itens da JTable",
        icon=ft.Icons.CONTENT_PASTE,
        on_click=on_inserir_click,
    )



    btn_carregar = ft.ElevatedButton(
        "Carregar itensZero",
        icon=ft.Icons.FOLDER_OPEN,
        on_click=lambda e: carregar_itens_zero(tabela, page),
    )

    return ft.Column(
        [
            titulo,
            ft.Row([btn_inserir, btn_carregar], spacing=20),
            ft.Divider(),
            ft.Container(tabela, expand=True),
        ],
        expand=True,
        spacing=15,
    )