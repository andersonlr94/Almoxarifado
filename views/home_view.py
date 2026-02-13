import flet as ft

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
