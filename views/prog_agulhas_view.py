import flet as ft
from controllers.prog_agulhas_controller import criar_controller
from controllers.imprimir_controller import criar_controller as criar_imprimir_controller
from models.imprimir_model import listar_impressoras

def tela_prog_agulhas(page, ler_dados, salvar_no_arquivo, obter_pasta_dados):

    if not obter_pasta_dados():
        return ft.Text(
            "Configure a pasta de dados primeiro.",
            size=18,
            color="red"
        )

    # Definir as colunas da tabela - 8 colunas
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Sel")),           # Coluna 0
            ft.DataColumn(ft.Text("Pedido")),        # Coluna 1
            ft.DataColumn(ft.Text("Kardex")),        # Coluna 2 - NOVA COLUNA
            ft.DataColumn(ft.Text("Código")),        # Coluna 3
            ft.DataColumn(ft.Text("Qtde")),          # Coluna 4
            ft.DataColumn(ft.Text("Fornecedor")),    # Coluna 5
            ft.DataColumn(ft.Text("Requisitante")),  # Coluna 6
            ft.DataColumn(ft.Text("Status")),        # Coluna 7
        ],
        rows=[],
        data_row_min_height=16,
        data_row_max_height=20,
        heading_row_height=20,
    )

    # Botões existentes
    btn_programar = ft.ElevatedButton(
        "Mudar p/ Programado",
        bgcolor="blue",
        color="white",
        visible=False
    )

    btn_separar = ft.ElevatedButton(
        "Mudar p/ Separando",
        bgcolor="orange",
        color="white",
        visible=False
    )

    btn_entregar = ft.ElevatedButton(
        "Mudar p/ Entregue",
        bgcolor="green",
        color="white",
        visible=False
    )

    btn_transferir_qad = ft.ElevatedButton(
        "Transferir QAD",
        bgcolor="purple",
        color="white",
        visible=False
    )

    # ComboBox para selecionar impressora
    impressoras = listar_impressoras()
    print(f"Impressoras encontradas: {impressoras}")  # Debug
    
    # Garantir que impressoras é uma lista
    if impressoras is None:
        impressoras = []
    
    opcoes_impressoras = [
        ft.dropdown.Option("Salvar como PDF"),
        ft.dropdown.Option("Padrão do Sistema")
    ]
    
    # Adicionar impressoras apenas se houver
    for imp in impressoras:
        if imp:  # Verificar se não é vazio
            opcoes_impressoras.append(ft.dropdown.Option(imp))
    
    cb_impressora = ft.Dropdown(
        label="Destino da Impressão",
        options=opcoes_impressoras,
        value="Salvar como PDF",
        width=250,
        height=40,
        visible=False
    )

    # Botão Imprimir
    btn_imprimir = ft.ElevatedButton(
        "Imprimir/Salvar PDF",
        bgcolor="teal",
        color="white",
        visible=False
    )

    # Campos de entrada
    txt_pedido = ft.TextField(label="Pedido", width=100, height=30)
    txt_codigo = ft.TextField(label="Código", width=100, height=30)
    txt_qtde = ft.TextField(label="Qtde", width=100, height=30)
    txt_requisitante = ft.TextField(label="Requisitante", width=150, height=30)

    btn_inserir = ft.ElevatedButton(
        "Inserir",
        bgcolor="purple",
        color="white"
    )

    # Criar controller principal
    carregar_tabela, atualizar_status, inserir_pedido, transferir_qad = criar_controller(
        page,
        tabela,
        btn_programar,
        btn_separar,
        btn_entregar,
        btn_transferir_qad,
        btn_imprimir,
        cb_impressora,
        ler_dados,
        salvar_no_arquivo,
        txt_codigo,
    )

    # Criar controller de impressão
    imprimir = criar_imprimir_controller(page, tabela, cb_impressora)

    # Conectar botões
    btn_programar.on_click = lambda e: atualizar_status("Programado")
    btn_separar.on_click = lambda e: atualizar_status("Separando")
    btn_entregar.on_click = lambda e: atualizar_status("Entregue")
    btn_transferir_qad.on_click = lambda e: transferir_qad(e)
    btn_imprimir.on_click = lambda e: imprimir(e)
    
    async def on_inserir_click(e):
        await inserir_pedido(e, txt_pedido, txt_codigo, txt_qtde, txt_requisitante)
    
    btn_inserir.on_click = on_inserir_click

    # Carrega padrão
    carregar_tabela("Pendente")

    return ft.Column(
        [
            ft.Row(
                [
                    ft.ElevatedButton("Pendentes", on_click=lambda _: carregar_tabela("Pendente")),
                    ft.ElevatedButton("Programados", on_click=lambda _: carregar_tabela("Programado")),
                    ft.ElevatedButton("Separando", on_click=lambda _: carregar_tabela("Separando")),
                    ft.ElevatedButton("Entregues", on_click=lambda _: carregar_tabela("Entregue")),
                ]
            ),
            ft.Row(
                [
                    txt_pedido,
                    txt_codigo,
                    txt_qtde,
                    txt_requisitante,
                    btn_inserir
                ],
                wrap=True
            ),
            ft.Divider(),
            ft.ListView([tabela], expand=True),
            ft.Divider(),
            ft.Row(
                [
                    btn_programar, 
                    btn_separar, 
                    btn_entregar, 
                    btn_transferir_qad,
                    cb_impressora,
                    btn_imprimir
                ], 
                alignment="center",
                wrap=True
            ),
        ],
        expand=True
    )