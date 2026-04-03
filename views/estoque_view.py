import flet as ft
from controllers.estoque_controller import criar_controller

def tela_estoque(page: ft.Page):

    # ================= FILTRO =================
    txt_filtro = ft.TextField(
        label="Filtrar",
        hint_text="Digite código, descrição ou kardex...",
        width=400,
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
    tabela = ft.DataTable(
        columns=colunas_widgets,
        rows=[],
        column_spacing=15,
        heading_row_height=40,  
        data_row_min_height=35,
        data_row_max_height=35,
        vertical_lines=ft.border.BorderSide(0.5, ft.Colors.GREY_300),
        horizontal_lines=ft.border.BorderSide(0.5, ft.Colors.GREY_300),
    )

    # ================= SCROLL VERTICAL =================
    scroll_vertical = ft.Container(
        content=ft.Column(
            [tabela],
            scroll=ft.ScrollMode.ALWAYS,
        ),
        height=400,
    )

    # ================= SCROLL HORIZONTAL =================
    scroll_horizontal = ft.Row(
        controls=[scroll_vertical],
        scroll=ft.ScrollMode.ALWAYS,
    )

    # ================= CONTAINER FINAL =================
    tabela_container = ft.Column(
        [
            scroll_horizontal  # 👈 conteúdo rolável
        ],
        spacing=0,
    )

    container_borda = ft.Container(
        content=tabela_container,
        expand=True,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=5,
        padding=5,
    )

    # ================= CONTROLLER =================
    popular_tabela, filtrar_tabela = criar_controller(
        page, tabela, txt_filtro, lbl_total
    )

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
                [txt_filtro, lbl_total],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Divider(),

            # Tabela
            container_borda,
        ],
        expand=True,
        spacing=10,
    )
