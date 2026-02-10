import flet as ft
from datetime import datetime
import json
import os

from digitar_ae import tela_digitar_ae
from config_geral import tela_config_geral


# =====================================================
# CAMINHO DA CONFIGURAÇÃO (Documents/Almoxarifado)
# =====================================================
PASTA_CONFIG = os.path.join(
    os.path.expanduser("~"),
    "Documents",
    "Almoxarifado"
)

CONFIG_FILE = os.path.join(PASTA_CONFIG, "config_geral.json")


def main(page: ft.Page):
    page.title = "Controle de Almoxarifado"
    page.window_width = 1100
    page.window_height = 700

    # =================================================
    # FUNÇÕES DE CONFIGURAÇÃO
    # =================================================
    def obter_pasta_dados():
        if not os.path.exists(CONFIG_FILE):
            return ""
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("pasta_dados", "")
        except:
            return ""

    def caminho_arquivo(nome):
        pasta = obter_pasta_dados()
        if not pasta:
            return None
        return os.path.join(pasta, nome)

    # =================================================
    # DADOS
    # =================================================
    def ler_dados():
        caminho = caminho_arquivo("pedidos.json")
        if not caminho or not os.path.exists(caminho):
            return []
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def salvar_no_arquivo(dados):
        caminho = caminho_arquivo("pedidos.json")
        if not caminho:
            return
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    # =================================================
    # COMPONENTES
    # =================================================
    conteudo = ft.Container(expand=True)

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Sel")),
            ft.DataColumn(ft.Text("Pedido")),
            ft.DataColumn(ft.Text("Kardex")),
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Descrição")),
            ft.DataColumn(ft.Text("Qtde")),
            ft.DataColumn(ft.Text("Status")),
        ],
        rows=[]
    )

    btn_programar = ft.ElevatedButton(
        "Mudar p/ Programado",
        bgcolor="blue",
        color="white",
        visible=False,
        on_click=lambda _: atualizar_status("Programado")
    )

    btn_separar = ft.ElevatedButton(
        "Mudar p/ Separando",
        bgcolor="orange",
        color="white",
        visible=False,
        on_click=lambda _: atualizar_status("Separando")
    )

    btn_entregar = ft.ElevatedButton(
        "Mudar p/ Entregue",
        bgcolor="green",
        color="white",
        visible=False,
        on_click=lambda _: atualizar_status("Entregue")
    )

    # =================================================
    # LÓGICA DA TABELA
    # =================================================
    def carregar_tabela(filtro_status="Pendente"):
        dados = ler_dados()
        tabela.rows.clear()

        btn_programar.visible = (filtro_status == "Pendente")
        btn_separar.visible = (filtro_status == "Programado")
        btn_entregar.visible = (filtro_status == "Separando")

        for item in dados:
            status_item = str(item.get("status", ""))

            mostrar = False
            if filtro_status == "Entregue":
                mostrar = status_item.startswith("Entregue")
            elif status_item == filtro_status:
                mostrar = True

            if mostrar:
                tabela.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Checkbox(value=False)),
                            ft.DataCell(ft.Text(item.get("pedido", ""))),
                            ft.DataCell(ft.Text(item.get("kardex", ""))),
                            ft.DataCell(ft.Text(item.get("codigo", ""))),
                            ft.DataCell(ft.Text(item.get("descricao", ""))),
                            ft.DataCell(ft.Text(item.get("qtde", ""))),
                            ft.DataCell(ft.Text(status_item)),
                        ]
                    )
                )

        page.update()

    def atualizar_status(novo_status):
        dados = ler_dados()
        alterou = False
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        origem = ""

        for row in tabela.rows:
            if row.cells[0].content.value:
                pedido = row.cells[1].content.value
                codigo = row.cells[3].content.value

                for item in dados:
                    if str(item["pedido"]) == str(pedido) and str(item["codigo"]) == str(codigo):
                        if novo_status == "Entregue":
                            item["status"] = f"Entregue em {data_hora}"
                            origem = "Separando"
                        else:
                            item["status"] = novo_status
                            origem = "Pendente" if novo_status == "Programado" else "Programado"
                        alterou = True

        if alterou:
            salvar_no_arquivo(dados)
            carregar_tabela(origem)
            page.snack_bar = ft.SnackBar(ft.Text("Status atualizado"))
            page.snack_bar.open = True
            page.update()

    # =================================================
    # TELAS
    # =================================================
    def tela_home():
        return ft.Column(
            [
                ft.Text("Bem-vindo ao Almoxarifado", size=30, weight="bold"),
                ft.Text("Use o menu acima para navegar")
            ],
            alignment="center",
            horizontal_alignment="center",
            expand=True
        )

    def tela_config_agulhas():
        return ft.Column(
            [
                ft.Text("Configuração de Programação de Agulhas", size=24, weight="bold"),
                ft.Text("Tela em construção")
            ],
            expand=True
        )

    def tela_manutencao():
        if not obter_pasta_dados():
            return ft.Text(
                "Configure a pasta de dados primeiro.",
                size=18,
                color="red"
            )

        return ft.Column(
            [
                ft.Row(
                    [
                        ft.ElevatedButton("Pendentes", on_click=lambda _: carregar_tabela("Pendente")),
                        ft.ElevatedButton("Programados", on_click=lambda _: carregar_tabela("Programado")),
                        ft.ElevatedButton("Separando", on_click=lambda _: carregar_tabela("Separando")),
                        ft.ElevatedButton("Entregues", on_click=lambda _: carregar_tabela("Entregue")),
                        ft.ElevatedButton(
                            "Config. Programação de Agulhas",
                            icon="build",
                            bgcolor="purple",
                            color="white",
                            on_click=lambda _: mudar_tela("config_agulhas")
                        )
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE
                ),
                ft.Divider(),
                ft.ListView([tabela], expand=True),
                ft.Divider(),
                ft.Row([btn_programar, btn_separar, btn_entregar], alignment="center")
            ],
            expand=True
        )

    # =================================================
    # NAVEGAÇÃO
    # =================================================
    def mudar_tela(destino):
        if destino == "home":
            conteudo.content = tela_home()
        elif destino == "manutencao":
            conteudo.content = tela_manutencao()
        elif destino == "config_geral":
            conteudo.content = tela_config_geral(page)
        elif destino == "config_agulhas":
            conteudo.content = tela_config_agulhas()
        elif destino == "digitar_ae":
            conteudo.content = tela_digitar_ae(page)

        page.update()

    # =================================================
    # MENU
    # =================================================
    menu = ft.Row(
        [
            ft.Row(
                [
                    ft.TextButton("Início", icon="home", on_click=lambda _: mudar_tela("home")),
                    ft.TextButton("Manutenção", icon="settings", on_click=lambda _: mudar_tela("manutencao")),
                    ft.TextButton("Digitar AE", icon="edit", on_click=lambda _: mudar_tela("digitar_ae")),
                ]
            ),
            ft.Container(expand=True),
            ft.IconButton(
                icon=ft.Icons.SETTINGS_APPLICATIONS,
                tooltip="Configuração Geral",
                on_click=lambda _: mudar_tela("config_geral")
            )
        ]
    )

    # =================================================
    # START
    # =================================================
    conteudo.content = tela_home()

    page.add(
        ft.Column(
            [
                menu,
                ft.Divider(),
                conteudo
            ],
            expand=True
        )
    )


ft.app(target=main)
