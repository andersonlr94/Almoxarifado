import flet as ft
import json
import os

from views.home_view import tela_home
from views.digitar_ae_view import tela_digitar_ae
from views.config_view import tela_config_geral 
from views.prog_agulhas_view import tela_prog_agulhas
from views.transferencia_view import tela_transferencia
from views.estoque_view import tela_estoque
from views.itens_zero_view import tela_itens_zero
from views.reajuste_preco_view import tela_reajuste_preco

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

        elif destino == "transferencia":
            conteudo.content = tela_transferencia(page)

        elif destino == "estoque":
            conteudo.content = tela_estoque(page)

        elif destino == "itens_zero":
            conteudo.content = tela_itens_zero(page)

        elif destino == "reajuste_preco":
            conteudo.content = tela_reajuste_preco(page)

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
                    ft.TextButton(
                        "Transferencia",
                        icon="edit",
                        on_click=lambda _: mudar_tela("transferencia")
                    ),
                    ft.TextButton(
                        "" \
                        "Estoque",
                        icon="edit",
                        on_click=lambda _: mudar_tela("estoque")
                    ),
                    ft.TextButton(
                        "Itens 0",
                        icon="edit",
                        on_click=lambda _: mudar_tela("itens_zero")
                    ),
                    ft.TextButton(
                        "Reajuste de preços",
                        icon="edit",
                        on_click=lambda _: mudar_tela("reajuste_preco")
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

    def on_close(e):
        print("Aplicação fechando normalmente...")
        # Cancelar tarefas pendentes se necessário
    
    page.on_close = on_close

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


if __name__ == "__main__":
    try:
        ft.app(target=main)
    except KeyboardInterrupt:
        print("\nAplicação interrompida pelo usuário")
    except Exception as e:
        print(f"Erro ao fechar: {e}")