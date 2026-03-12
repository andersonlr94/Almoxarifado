# views/transferencia_view.py
import flet as ft
from controllers.transferencia_controller import criar_controller

def tela_transferencia(page: ft.Page):
    # ---------------------------
    # Campos de filtro (topo)
    # ---------------------------
    # Esquerda
    tf_documento = ft.TextField(label="Documento", width=260, dense=True)
    tf_kardex    = ft.TextField(label="Kardex",    width=260, dense=True)

    # Direita
    tf_depo_de   = ft.TextField(label="De depósito",   width=260, dense=True)
    tf_depo_para = ft.TextField(label="Para depósito", width=260, dense=True)

    # ---------------------------
    # Tabela (embaixo)
    # ---------------------------
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Sel.")),
            ft.DataColumn(ft.Text("Documento")),
            ft.DataColumn(ft.Text("Kardex")),
            ft.DataColumn(ft.Text("Qtde")),
            ft.DataColumn(ft.Text("De")),
            ft.DataColumn(ft.Text("Para")),
            ft.DataColumn(ft.Text("Data")),
        ],
        rows=[],
        heading_row_color=ft.Colors.BLUE_GREY_50,
        column_spacing=12,
        data_row_max_height=44,
        show_checkbox_column=False,  # usaremos CheckBox na 1ª coluna manualmente
    )

    # ---------------------------
    # Botões (ações)
    # ---------------------------
    btn_carregar = ft.ElevatedButton("Carregar", icon=ft.Icons.SEARCH)
    btn_limpar   = ft.OutlinedButton("Limpar", icon=ft.Icons.CLEAR)

    # ---------------------------
    # Controller (liga eventos)
    # ---------------------------
    carregar, limpar = criar_controller(
        page,
        tabela,
        tf_documento, tf_kardex, tf_depo_de, tf_depo_para
    )
    btn_carregar.on_click = carregar
    btn_limpar.on_click   = limpar

    # ---------------------------
    # Layout superior: 2 colunas (esq/dir) + coluna de botões
    # ---------------------------
    topo = ft.Row(
        controls=[
            
            ft.Container(
                expand=True,
                content=ft.Column(
                    controls=[tf_documento, tf_kardex],
                    spacing=8
                )
            ),
            ft.Container(
                expand=True,
                content=ft.Column(
                    controls=[tf_depo_de, tf_depo_para],
                    spacing=8
                )
            ),
            ft.Column(
                controls=[btn_carregar, btn_limpar],
                spacing=8,
                alignment=ft.MainAxisAlignment.END
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    # ---------------------------
    # Monta a página
    # ---------------------------
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