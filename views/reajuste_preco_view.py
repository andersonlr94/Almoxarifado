import flet as ft
from controllers.reajuste_preco_controller import criar_controller, COLUNAS

def tela_reajuste_preco(page: ft.Page):
    
    # ================= TÍTULO =================
    titulo = ft.Text(
        "Reajuste de preços pelos fornecedores",
        size=26,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_800,
    )
    
    # ================= CONTADOR =================
    txt_contador = ft.Text(
        "Total: 0 itens",
        size=13,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_700,
    )
    
    # ================= CAMPOS DE TEXTO =================
    # NOVO CAMPO: Fornecedor (primeiro)
    txt_fornecedor = ft.TextField(
        label="Fornecedor",
        hint_text="Digite o Fornecedor",
        width=200,
        height=50,
    )
    
    txt_kardex = ft.TextField(
        label="Kardex",
        hint_text="Digite o Kardex",
        width=200,
        height=50,
    )
    
    txt_item = ft.TextField(
        label="Item",
        hint_text="Digite o Item",
        width=200,
        height=50,
    )
    
    txt_descricao = ft.TextField(
        label="Descrição",
        hint_text="Digite a Descrição",
        width=250,
        height=50,
    )
    
    txt_preco_antigo = ft.TextField(
        label="Preço antigo",
        hint_text="Digite o preço antigo",
        width=150,
        height=50,
    )
    
    # ================= BOTÕES =================
    btn_inserir = ft.ElevatedButton(
        "Inserir",
        bgcolor=ft.Colors.GREEN_600,
        color=ft.Colors.WHITE,
    )
    
    btn_excluir = ft.ElevatedButton(
        "Excluir",
        bgcolor=ft.Colors.RED_600,
        color=ft.Colors.WHITE,
        visible=False,
    )
    
    # ================= TABELA =================
    colunas_widgets = [
        ft.DataColumn(ft.Text(col, size=11, weight=ft.FontWeight.BOLD))
        for col in COLUNAS
    ]
    
    tabela = ft.DataTable(
        columns=colunas_widgets,
        rows=[],
        column_spacing=10,
        heading_row_height=40,
        data_row_min_height=35,
        data_row_max_height=35,
        vertical_lines=ft.border.BorderSide(0.5, ft.Colors.GREY_300),
        horizontal_lines=ft.border.BorderSide(0.5, ft.Colors.GREY_300),
    )
    
    # ================= SCROLL DA TABELA =================
    tabela_scroll = ft.ListView(
        expand=True,
        spacing=0,
        controls=[
            ft.Row(
                controls=[tabela],
                scroll=ft.ScrollMode.ALWAYS,
            )
        ],
    )
    
    # ================= CRIAR CONTROLLER =================
    inserir, excluir, carregar = criar_controller(
        page, tabela, txt_fornecedor, txt_kardex, txt_item, txt_descricao, txt_preco_antigo, btn_excluir
    )
    
    # Conectar botões
    btn_inserir.on_click = inserir
    btn_excluir.on_click = excluir
    
    # ================= LAYOUT =================
    return ft.Column(
        [
            titulo,
            
            # Linha dos campos de texto e botões
            ft.Container(
                content=ft.Row(
                    [
                        ft.Row(
                            [txt_fornecedor, txt_kardex, txt_item, txt_descricao, txt_preco_antigo],
                            spacing=10,
                            wrap=True,
                        ),
                        ft.Row(
                            [btn_inserir, btn_excluir],
                            spacing=10,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=ft.padding.only(bottom=10),
            ),
            
            ft.Divider(),
            
            # Contador
            ft.Container(
                content=ft.Row(
                    [txt_contador],
                    alignment=ft.MainAxisAlignment.END,
                ),
                padding=ft.padding.only(top=5, bottom=5),
            ),
            
            # Tabela
            tabela_scroll,
        ],
        expand=True,
        spacing=10,
    )