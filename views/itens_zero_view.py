# views/transferencia_view.py
import flet as ft
# from controllers.transferencia_controller import criar_controller


def tela_itens_zero(page: ft.Page):

    # =========================================================
    # CONTEÚDO PRINCIPAL
    # =========================================================
    conteudo = ft.Container(
        expand=True,
        padding=10,
        content=ft.Column(
            [
                
                ft.Text("Itens Zero"),
                
            ],
            expand=True,
        ),
    )

    return conteudo
