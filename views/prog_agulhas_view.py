import flet as ft
from controllers.prog_agulhas_controller import criar_controller

def tela_prog_agulhas(page, ler_dados, salvar_no_arquivo, obter_pasta_dados):

    if not obter_pasta_dados():
        return ft.Text(
            "Configure a pasta de dados primeiro.",
            size=18,
            color="red"
        )

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Sel")),
            ft.DataColumn(ft.Text("Pedido")),
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Qtde")),
            ft.DataColumn(ft.Text("Fornecedor")),
            ft.DataColumn(ft.Text("Requisitante")),
            ft.DataColumn(ft.Text("Status")),
        ],
        rows=[],
        data_row_min_height=16,
        data_row_max_height=20,
        heading_row_height=20,
    )

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

    txt_pedido = ft.TextField(label="Pedido", width=120, height=30)
    txt_codigo = ft.TextField(label="Código", width=100, height=30)
    txt_qtde = ft.TextField(label="Qtde", width=100, height=30)
    txt_requisitante = ft.TextField(label="Requisitante", width=150, height=30)

    btn_inserir = ft.ElevatedButton(
        "Inserir",
        bgcolor="purple",
        color="white"
    )

    # Criar controller
    carregar_tabela, atualizar_status, inserir_pedido = criar_controller(
        page,
        tabela,
        btn_programar,
        btn_separar,
        btn_entregar,
        ler_dados,
        salvar_no_arquivo,
        txt_codigo
    )

    # Conectar botões
    btn_programar.on_click = lambda e: atualizar_status("Programado")
    btn_separar.on_click = lambda e: atualizar_status("Separando")
    btn_entregar.on_click = lambda e: atualizar_status("Entregue")
    
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
            ft.Row([btn_programar, btn_separar, btn_entregar], alignment="center")
        ],
        expand=True
    )