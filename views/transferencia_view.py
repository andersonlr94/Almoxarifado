# views/transferencia_view.py
import flet as ft
from controllers.transferencia_controller import criar_controller


def tela_transferencia(page: ft.Page):

    # =========================================================
    # CAMPOS - LADO ESQUERDO (ORIGEM)
    # =========================================================
    tf_de_local = ft.TextField(
        label="De Local:",
        width=260,
        dense=True,
        value="10912",
    )

    tf_de_lugar = ft.TextField(
        label="De Lugar:",
        width=260,
        dense=True,
    )

    tf_de_lote = ft.TextField(
        label="De Lote:",
        width=260,
        dense=True,
    )

    # =========================================================
    # CAMPOS - LADO DIREITO (DESTINO)
    # =========================================================
    tf_para_local = ft.TextField(
        label="Para Local:",
        width=260,
        dense=True,
        value="10912",
    )

    tf_para_lugar = ft.TextField(
        label="Para Lugar:",
        width=260,
        dense=True,
    )

    tf_para_lote = ft.TextField(
        label="Para Lote:",
        width=260,
        dense=True,
    )

    # =========================================================
    # RADIO GROUP - COMO USAR TERCEIRA COLUNA
    # =========================================================
    rg_terceira_coluna = ft.RadioGroup(
        value="formulario",  # valor padrão
        content=ft.Column(
            [
                ft.Text(
                    "Como usar terceira coluna",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Radio(
                    value="formulario",
                    label="Usar formulário",
                ),
                ft.Radio(
                    value="lote_inicial",
                    label="Usar Lote inicial",
                ),
                ft.Radio(
                    value="lote_destino",
                    label="Usar Lote destino",
                ),
            ],
            spacing=6,
        ),
    )

    # =========================================================
    # CONTROLE DE BLOQUEIO DOS CAMPOS CONFORME O RADIO
    # =========================================================
    def on_terceira_coluna_change(e):
        modo = rg_terceira_coluna.value

        if modo == "formulario":
            tf_de_lote.disabled = False
            tf_para_lote.disabled = False

        elif modo == "lote_inicial":
            tf_de_lote.disabled = True
            tf_para_lote.disabled = False

        elif modo == "lote_destino":
            tf_de_lote.disabled = False
            tf_para_lote.disabled = True

        page.update()

    rg_terceira_coluna.on_change = on_terceira_coluna_change

    # Aplica o estado inicial corretamente
    tf_de_lote.disabled = False
    tf_para_lote.disabled = False

    # =========================================================
    # TABELA - SEMPRE 3 COLUNAS
    # =========================================================
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Kardex")),
            ft.DataColumn(ft.Text("Qtde")),
            ft.DataColumn(ft.Text("Lote")),
        ],
        rows=[],
        heading_row_color=ft.Colors.BLUE_GREY_50,
        column_spacing=12,
        data_row_max_height=44,
        show_checkbox_column=False,
    )

    # =========================================================
    # BOTÕES
    # =========================================================
    btn_carregar = ft.ElevatedButton(
        "Carregar do Clipboard",
        icon=ft.Icons.CONTENT_PASTE,
    )

    btn_transferir = ft.ElevatedButton(
        "Transferir",
        icon=ft.Icons.SEND,
    )

    btn_limpar = ft.OutlinedButton(
        "Limpar",
        icon=ft.Icons.CLEAR,
    )

    # =========================================================
    # CONTROLLER
    # =========================================================
    carregar, limpar, transferir = criar_controller(
        page,
        tabela,
        tf_de_local, tf_de_lugar, tf_de_lote,
        tf_para_local, tf_para_lugar, tf_para_lote,
        rg_terceira_coluna,   # <<< radio enviado ao controller
    )

    btn_carregar.on_click = carregar
    btn_limpar.on_click = limpar
    btn_transferir.on_click = transferir

    # =========================================================
    # LAYOUT SUPERIOR
    # =========================================================
    topo = ft.Row(
        [
            ft.Container(
                expand=True,
                content=ft.Column(
                    [
                        tf_de_local,
                        tf_de_lugar,
                        tf_de_lote,
                    ],
                    spacing=8,
                ),
            ),
            ft.Container(
                expand=True,
                content=ft.Column(
                    [
                        tf_para_local,
                        tf_para_lugar,
                        tf_para_lote,
                    ],
                    spacing=8,
                ),
            ),
            ft.Container(
                expand=True,
                content=ft.Column(
                    [
                        rg_terceira_coluna,
                    ],
                    spacing=8,
                ),
            ),
            ft.Column(
                [
                    btn_carregar,
                    btn_transferir,
                    btn_limpar,
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.END,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    # =========================================================
    # CONTEÚDO PRINCIPAL
    # =========================================================
    conteudo = ft.Container(
        expand=True,
        padding=10,
        content=ft.Column(
            [
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
            expand=True,
        ),
    )

    return conteudo
