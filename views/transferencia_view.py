# views/transferencia_view.py
import flet as ft
from controllers.transferencia_controller import criar_controller

def tela_transferencia(page: ft.Page):
    # --------- Campos do topo (seus labels personalizados) ----------
    tf_de_local   = ft.TextField(label="De Local:",  width=260, dense=True)
    tf_de_lugar   = ft.TextField(label="De Lugar:",  width=260, dense=True)
    tf_para_local = ft.TextField(label="Para Local:", width=260, dense=True)
    tf_para_lugar = ft.TextField(label="Para Lugar:", width=260, dense=True)

    # --------- Tabela embaixo (apenas Kardex e Qtde) ----------
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Kardex")),
            ft.DataColumn(ft.Text("Qtde")),
        ],
        rows=[],
        heading_row_color=ft.Colors.BLUE_GREY_50,
        column_spacing=12,
        data_row_max_height=44,
        show_checkbox_column=False,
    )

    # --------- Botões ----------
    btn_carregar = ft.ElevatedButton("Carregar do Clipboard", icon=ft.Icons.CONTENT_PASTE)
    btn_limpar   = ft.OutlinedButton("Limpar", icon=ft.Icons.CLEAR)

    # --------- Controller: recebe os handlers e liga nos botões ----------
    carregar, limpar = criar_controller(
        page,
        tabela,
        tf_de_local, tf_de_lugar,
        tf_para_local, tf_para_lugar,
    )
    # Ligue os handlers aqui:
    btn_carregar.on_click = carregar   # <- async def no controller
    btn_limpar.on_click   = limpar

    # --------- Layout do topo ----------
    topo = ft.Row(
        controls=[
            ft.Container(
                expand=True,
                content=ft.Column([tf_de_local, tf_de_lugar], spacing=8)
            ),
            ft.Container(
                expand=True,
                content=ft.Column([tf_para_local, tf_para_lugar], spacing=8)
            ),
            ft.Column(
                controls=[btn_carregar, btn_limpar],
                spacing=8,
                alignment=ft.MainAxisAlignment.END,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    # --------- Monta a página ----------
    conteudo = ft.Container(
        expand=True,
        padding=10,
        content=ft.Column(
            expand=True,
            controls=[
                topo,
                ft.Divider(),
                ft.Container(
                    expand=True,
                    content=ft.ListView(
                        expand=True,
                        controls=[tabela],
                    ),
                ),
            ],
        ),
    )
    return conteudo