import flet as ft
from models.config_model import obter_pasta_dados, obter_pasta_itens
from controllers.config_controller import criar_controller

def tela_config_geral(page: ft.Page):
    
    txt_pasta_dados = ft.TextField(
        label="Caminho da pasta de Programação de Agulhas",
        hint_text=r"Ex: C:\Almoxarifado\Dados",
        value=obter_pasta_dados(),
        expand=True
    )
    
    txt_pasta_itens = ft.TextField(
        label="Caminho da pasta de Itens Almoxarifado",
        hint_text=r"Ex: C:\Almoxarifado\Itens",
        value=obter_pasta_itens(),
        expand=True
    )
    
    lbl_status = ft.Text("")
    
    salvar = criar_controller(page, txt_pasta_dados, txt_pasta_itens, lbl_status)
    
    return ft.Column(
        [
            ft.Text("Configuração Geral", size=26, weight="bold"),
            ft.Text("Os arquivos pedidos.json serão buscados nesta pasta:"),
            txt_pasta_dados,
            ft.Text("Os itensAlmoxarifado.json serão buscados nesta pasta:"),
            txt_pasta_itens,
            lbl_status,
            ft.ElevatedButton(
                "Salvar",
                icon=ft.Icons.SAVE,
                bgcolor="green",
                color="white",
                on_click=salvar
            )
        ],
        expand=True,
        spacing=15
    )