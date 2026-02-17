import flet as ft
import json
import os

from views.home_view import tela_home
from views.digitar_ae_view import tela_digitar_ae
from views.config_view import tela_config_geral 
from views.prog_agulhas_view import tela_prog_agulhas

from models.pedidos_model import ler_dados, salvar_no_arquivo
from models.config_model import obter_pasta_dados

# =====================================================
# CAMINHO DA CONFIGURAÇÃO (Documents/Almoxarifado)
# =====================================================
PASTA_CONFIG = os.path.join(
    os.path.expanduser("~"),
    "Documents",
    "Almoxarifado")

def main(page: ft.Page):
    page.title = "Controle de Almoxarifado"
    page.window_width = 1100
    page.window_height = 700
    
    # =================================================
    # COMPONENTE CENTRAL
    # =================================================
    conteudo = ft.Container(expand=True)

    # =================================================
    # TELAS
    # =================================================
    
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
