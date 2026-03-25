import flet as ft
from controllers.digitar_ae_controller import criar_controller
from controllers.anotacao_controller import criar_controller as criar_anotacao_controller


def tela_digitar_ae(page: ft.Page):

    # ================= TABELA =================
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

    # ================= PRESETS =================
    presets = {
        "STMUCONS  ": ("STMUCONS Uso e consumo", "6325", "CC55", ""),
        "STAFINDD  ": ("STAFINDD Primeira Saida", "6325", "CC60", ""),
        "STATFIXO  ": ("STATFIXO Mais de cinco anos", "6325", "CC60", ""),
        "SRMEMPAT  ": ("SRMEMPAT Circulação de ferramentas", "3295", "99200", ""),
        "SRMTTDES  ": ("SRMTTDES Remessa de teste sem retorno para não Aptiv", "8390", "09430", "5032"),
        "SRMINDAF  ": ("SMMINDAF Remessa para industrialização", "3295", "99200", ""),
        "SRMCONSE  ": ("SRMCONSE Remessa para conserto", "3295", "99200", ""),
        "STEMBALA  ": ("STEMBALA Remessa de embalagens (Caixas plasticas)", "3295", "99200", ""),
        "SRMTTRET  ": ("SRMTTRET Remessa de produto Aptiv para teste com retorno", "2400ADA", "99200", )
    }

    # ================= CAMPOS =================
    txt_conta = ft.TextField(label="Conta", width=150, value="6325")
    txt_subconta = ft.TextField(label="SubConta", width=150, value="CC55")
    txt_cc = ft.TextField(label="CC", width=150, value="")

    # ================= TEXTO PARA EXIBIR A OPÇÃO SELECIONADA =================
    txt_selecionado = ft.Text(
        "Nenhum tipo selecionado",
        size=12,
        color=ft.Colors.GREY_600,
    )
    
    # ================= FUNÇÃO PARA APLICAR PRESET =================
    def aplicar_preset(nome_curto):
        if not nome_curto:
            return

        dados = presets.get(nome_curto)
        if not dados:
            return

        nome_completo, conta, subconta, cc = dados
        txt_conta.value = conta
        txt_subconta.value = subconta
        txt_cc.value = cc
        txt_selecionado.value = f"                                   {nome_completo}"
        txt_selecionado.color = ft.Colors.GREEN_600

        txt_conta.update()
        txt_subconta.update()
        txt_cc.update()
        txt_selecionado.update()

        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"✓ Carregado: {nome_completo}"),
            bgcolor="green",
            duration=1500
        )
        page.snack_bar.open = True
        page.update()

    # ================= MENU FLUTUANTE (POPUP) =================
    menu_items = []
    for nome in presets.keys():
        menu_items.append(
            ft.PopupMenuItem(
                content=ft.Text(nome),
                on_click=lambda e, n=nome: aplicar_preset(n)
            )
        )
    
    btn_menu = ft.PopupMenuButton(
        items=menu_items,
        content=ft.Row(
            [
                ft.Text("▼", size=14),
                ft.Text("Selecionar NOP", size=14),
            ],
            spacing=5,
        ),
        bgcolor=ft.Colors.WHITE,
        width=150,  
        height=40,
    )

    # ================= CONTROLLER =================
    colar, executar, limpar = criar_controller(
        page,
        tabela,
        txt_conta,
        txt_subconta,
        txt_cc
    )

    # ================= BOTÕES =================
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

    # ================= ANOTAÇÕES =================
    txt_livre = ft.TextField(
        label="Anotações",
        multiline=True,
        min_lines=10,
        max_lines=20,
        expand=True,
        hint_text="Digite aqui...",
        border=ft.InputBorder.OUTLINE,
    )

    salvar_anotacao, carregar_anotacao = criar_anotacao_controller(page, txt_livre)

    txt_livre.on_blur = salvar_anotacao
    carregar_anotacao()

    # ================= LAYOUT DIREITO =================
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

    # ================= LAYOUT ESQUERDO =================
    quadro_esquerdo = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Configuração de Contas", size=16, weight=ft.FontWeight.BOLD),
                        ft.Row([txt_selecionado], alignment=ft.MainAxisAlignment.START),
                    ]
                ),
                # 🔥 NOVO: Botão e campos na MESMA LINHA
                ft.Row(
                    [
                        btn_menu,                    # Botão de seleção
                        txt_conta,                   # Campo Conta
                        txt_subconta,                # Campo SubConta
                        txt_cc,                      # Campo CC
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                    wrap=True,  # Permite quebrar linha se necessário
                ),             

                ft.Divider(),

                ft.Row([btn_colar, btn_executar, btn_limpar]),

                ft.Divider(),

                ft.ListView([tabela], expand=True),
            ],
            expand=1,
            spacing=15,
        ),
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_400),
        border_radius=10,
        padding=15,
        expand=4,
    )

    # ================= FINAL =================
    return ft.Row(
        [
            quadro_esquerdo,
            ft.VerticalDivider(width=1, thickness=1),
            quadro_direito,
        ],
        expand=True,
        spacing=10,
    )