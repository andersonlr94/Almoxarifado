import flet as ft

def tela_home():
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Bem-vindo ao Almoxarifado", size=30, weight="bold"),
                ft.Text("Use o menu acima para navegar")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.Alignment(0, 0),  # centraliza horizontal e verticalmente
        expand=True
    )