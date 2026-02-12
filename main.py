import flet as ft
import json
import os

from digitar_ae import tela_digitar_ae
from config_geral import tela_config_geral
from prog_agulhas import tela_prog_agulhas


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
    # COMPONENTE CENTRAL
    # =================================================
    conteudo = ft.Container(expand=True)

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

    def tela_manutencao():
        return tela_prog_agulhas(
            page,
            ler_dados,
            salvar_no_arquivo,
            obter_pasta_dados
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

        elif destino == "digitar_ae":
            conteudo.content = tela_digitar_ae(page)

        page.update()

    # =================================================
    # MENU SUPERIOR
    # =================================================
    menu = ft.Row(
        [
            ft.Row(
                [
                    ft.TextButton(
                        "Início",
                        icon="home",
                        on_click=lambda _: mudar_tela("home")
                    ),
                    ft.TextButton(
                        "Manutenção",
                        icon="settings",
                        on_click=lambda _: mudar_tela("manutencao")
                    ),
                    ft.TextButton(
                        "Digitar AE",
                        icon="edit",
                        on_click=lambda _: mudar_tela("digitar_ae")
                    ),
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
