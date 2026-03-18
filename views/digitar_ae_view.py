import flet as ft
from controllers.digitar_ae_controller import criar_controller
from controllers.anotacao_controller import criar_controller as criar_anotacao_controller


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

    txt_conta = ft.TextField(label="Conta", width=200, value="6325")
    txt_subconta = ft.TextField(label="SubConta", width=200, value="CC55")
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

    # ========== SEGUNDO QUADRO ==========
    # Campo de texto livre
    txt_livre = ft.TextField(
        label="Anotações",
        multiline=True,
        min_lines=10,
        max_lines=20,
        expand=True,
        hint_text="Digite aqui...",
        border=ft.InputBorder.OUTLINE,
    )
    
    # Criar controller de anotações
    salvar_anotacao, carregar_anotacao = criar_anotacao_controller(page, txt_livre)
    
    # Configurar evento de perda de foco (on_blur) em vez de on_change
    txt_livre.on_blur = salvar_anotacao  # <-- ALTERADO: on_blur em vez de on_change
    
    # Carregar anotação do dia atual
    carregar_anotacao()

    # Container do quadro direito
    quadro_direito = ft.Container(
        content=ft.Column(
            [
                ft.Text("Anotações", size=18, weight=ft.FontWeight.BOLD),
                txt_livre,
            ],
            spacing=15,
            expand=True,
        ),
        bgcolor=ft.Colors.GREY_50,
        border=ft.border.all(1, ft.Colors.GREY_400),
        border_radius=10,
        padding=15,
        expand=1,
    )

    # Container do quadro esquerdo (conteúdo original)
    quadro_esquerdo = ft.Container(
        content=ft.Column(
            [
                ft.Row([txt_conta, txt_subconta, txt_cc]),
                ft.Divider(),
                ft.Row([btn_colar, btn_executar, btn_limpar]),
                ft.Divider(),
                ft.ListView([tabela], expand=True),
            ],
            expand=1,
        ),
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_400),
        border_radius=10,
        padding=15,
        expand=4,
    )

    # Layout principal com dois quadros lado a lado
    return ft.Row(
        [
            quadro_esquerdo,
            ft.VerticalDivider(width=1, thickness=1),
            quadro_direito,
        ],
        expand=True,
        spacing=10,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )