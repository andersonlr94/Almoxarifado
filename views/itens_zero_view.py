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
        column_spacing=1,        
        data_row_min_height=6,        
        heading_row_height=20,
    )

    
    async def confirmar_insercao(e):

        async def confirmar_e_inserir(ev):
            dialog.open = False
            page.update()
            await inserir_da_jtable(page, tabela)

        def cancelar(ev):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmação"),
            content=ft.Text(
                "Você tem certeza que deseja inserir os itens copiados da JTable?\n\n"
                "⚠️ Essa ação pode adicionar novos itens ao estoque zero."
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.ElevatedButton(
                    "Confirmar",
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE,
                    on_click=confirmar_e_inserir,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.clear()
        page.overlay.append(dialog)
        dialog.open = True
        page.update()


    btn_inserir = ft.ElevatedButton(
        "Inserir itens",
        icon=ft.Icons.CONTENT_PASTE,
        on_click=confirmar_insercao,
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