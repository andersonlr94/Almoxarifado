import flet as ft
from controllers.estoque_controller import criar_controller

def criar_cabecalho(colunas):
    return ft.Container(
        bgcolor=ft.Colors.GREY_200,
        padding=8,
        content=ft.Row(
            controls=[
                ft.Text(col, size=11, weight=ft.FontWeight.BOLD, no_wrap=True, width=140)
                for col in colunas
            ],
            spacing=5,
        ),
    )

def tela_estoque(page: ft.Page):

    # ================= FILTRO =================
    txt_filtro = ft.TextField(
        label="Filtrar",
        hint_text="Digite código, descrição ou kardex...",
        width=400,
    )

    # ================= BOTÕES =================
    
    btn_carregar = ft.ElevatedButton(
        "Carregar Itens",
        icon=ft.Icons.DOWNLOAD,
    )

    btn_atualizar = ft.ElevatedButton(
        "Atualizar estoque",
        icon=ft.Icons.CONTENT_PASTE,
    )

    lbl_total = ft.Text("Total: 0 itens", size=12, color=ft.Colors.GREY_600)

    # ================= COLUNAS =================
    colunas = [
        "Id", "Kardex", "Código", "Descrição", "Loc novo", "Qtde novo",
        "Loc retorno", "Qtde retorno", "Fornecedor", "Provável fornecedor",
        "Ordem", "Lote Pedido", "Lote Compra", "Leadtime", "Fator Segurança",
        "UM", "Pendente DPH", "Pend. entrega compras", "Pendente para SA",
        "Lugar de uso", "Custo", "Curva custo", "Consumo médio",
        "Curva demanda", "Equipamento", "Tipo de uso", "Estoque mínimo",
        "Estoque máximo", "Estoque estratégico",
        "Mostrar cons. med./prog. no mês", "Separar p/ holder", "Separar p/ mesa",
        "Item de estoque", "Pino de contato", "Ativo/Obsol.", "Classificação Fiscal",
        "IPI", "Observações", "Doc. evidência", "Descrição de evidência"
    ]

    colunas_widgets = [
        ft.DataColumn(
            ft.Text(col, size=11, weight=ft.FontWeight.BOLD, no_wrap=True)
        )
        for col in colunas
    ]

    # ================= TABELA  =================
    lista_linhas = ft.ListView(
        expand=True,
        spacing=2,
        auto_scroll=False,
    )

    cabecalho = criar_cabecalho(colunas)

    container_tabela = ft.Column(
        controls=[
            cabecalho,
            ft.Divider(height=1),
            lista_linhas,
        ],
        expand=True,
    )

    def criar_linha(item, colunas):
        return ft.Container(
            padding=6,
            bgcolor=ft.Colors.WHITE,
            content=ft.Row(
                controls=[
                    ft.Text(
                        str(item.get(col, "")),
                        size=11,
                        no_wrap=True,
                        width=140,
                    )
                    for col in colunas
                ],
                spacing=5,
            ),
        )

    # ================= CONTROLLER =================
    popular_tabela, filtrar_tabela, atualizar_estoque = criar_controller(
        page, lista_linhas, txt_filtro, lbl_total
    )

    btn_carregar.on_click = lambda e: popular_tabela()

    btn_carregar.on_click = lambda e: (
        print("BOTÃO CARREGAR CLICADO"),
        popular_tabela()
    )

    
    btn_atualizar.on_click = atualizar_estoque

    txt_filtro.on_change = filtrar_tabela

    # ================= LAYOUT =================
    return ft.Column(
        controls=[
            # Título
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(
                            "Estoque do Almoxarifado Engenharia Central",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_800,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                margin=ft.margin.only(bottom=10),
            ),

            # Filtro + total
            ft.Row(
                [txt_filtro, btn_carregar, btn_atualizar, lbl_total],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Divider(),

            # Tabela
            container_tabela
        ],
        expand=True,
        spacing=10,
    )
