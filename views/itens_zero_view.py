import flet as ft
from controllers.itens_zero_controller import (
    inserir_da_jtable,
    carregar_itens_zero,
    COLUNAS_VISIVEIS,
    copiar_tabela_para_clipboard
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
        column_spacing=6,        
        data_row_min_height=18,
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
            "Atualizar",
            icon=ft.Icons.REFRESH,
            on_click=lambda e: carregar_itens_zero(tabela, txt_contador, page),
        )

    btn_copiar_excel = ft.ElevatedButton(
        "Copiar p/ Excel",
        icon=ft.Icons.TABLE_VIEW,
    )
    
    async def on_copiar_excel(e):
        await copiar_tabela_para_clipboard(page, tabela)
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Tabela copiada para o Excel ✅"),
            bgcolor=ft.Colors.GREEN,
        )
        page.snack_bar.open = True
        page.update()

    btn_copiar_excel.on_click = on_copiar_excel

    tabela_scroll = ft.SelectionArea(
        content=ft.ListView(
            expand=True,
            spacing=0,
            controls=[
                ft.Row(
                    controls=[tabela],
                    scroll=ft.ScrollMode.ALWAYS,
                )
            ],
        )
    )

    carregar_itens_zero(tabela, txt_contador, page)

    return ft.Column(
        [
            titulo,

            ft.Container(
                content=ft.Row(
                    [
                        ft.Row([btn_inserir, btn_carregar, btn_copiar_excel], spacing=20),
                        txt_contador,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=6,   # ajuste fino da altura da barra
            ),

            ft.Divider(),
            ft.Container(expand=True, content=tabela_scroll),        ],
        expand=True,
        spacing=8,
    )