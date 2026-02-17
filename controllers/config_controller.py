import flet as ft
from models.config_model import salvar_config

def criar_controller(page, txt_pasta_dados, txt_pasta_itens, lbl_status):
    
    def salvar_configuracoes(e):
        dados = {
            "pasta_dados": txt_pasta_dados.value.strip(),
            "pasta_itens": txt_pasta_itens.value.strip()
        }
        
        try:
            salvar_config(dados)
            lbl_status.value = "Configurações salvas com sucesso!"
            lbl_status.color = "green"
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Configurações salvas!"),
                bgcolor="green"
            )
            page.snack_bar.open = True
        except Exception as erro:
            lbl_status.value = f"Erro ao salvar: {str(erro)}"
            lbl_status.color = "red"
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Erro: {str(erro)}"),
                bgcolor="red"
            )
            page.snack_bar.open = True
        
        page.update()
    
    return salvar_configuracoes