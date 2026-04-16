import flet as ft
from controllers.itens_zero_controller import (
    inserir_da_jtable,
    carregar_itens_zero,
    COLUNAS_VISIVEIS,
)


def tela_itens_zero(page: ft.Page):

    titulo = ft.Text(
        "Estoque Zero",
        size=26,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_800,
    )

    txt_contador = ft.Text(
        "Total: 0 itens",
        size=13,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_700,
    )


    tabela = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(c)) for c in COLUNAS_VISIVEIS],
        rows=[],
        expand=True,
        column_spacing=1,        
        data_row_min_height=16,
        data_row_max_height=20,        
        heading_row_height=20,
    )

    
    async def confirmar_insercao(e):

        async def confirmar_e_inserir(ev):
            dialog.open = False
            page.update()
            await inserir_da_jtable(page, tabela, txt_contador)

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
            on_click=lambda e: carregar_itens_zero(tabela, txt_contador, page),
        )

    tabela_scroll = ft.ListView(
        expand=True,
        spacing=0,
        controls=[
            ft.Row(
                controls=[tabela],
                scroll=ft.ScrollMode.ALWAYS,  # ✅ horizontal
            )
        ],
    )

    return ft.Column(
        [
            titulo,

            ft.Container(
                content=ft.Row(
                    [
                        ft.Row([btn_inserir, btn_carregar], spacing=20),
                        txt_contador,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=6,   # ajuste fino da altura da barra
            ),

            ft.Divider(),
            tabela_scroll,
        ],
        expand=True,
        spacing=8,
    )