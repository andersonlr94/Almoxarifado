import flet as ft
from models.anotacao_model import salvar_anotacao, carregar_anotacao

def criar_controller(page, txt_anotacao):
    """
    Cria o controller para gerenciar anotações
    
    Args:
        page: Página do Flet
        txt_anotacao: Campo de texto onde a anotação é digitada
    
    Returns:
        tuple: (função para salvar, função para carregar)
    """
    
    def salvar_anotacao_automatico(e):
        """
        Salva a anotação automaticamente quando o texto é alterado
        """
        # Usar um timer para não salvar a cada tecla (opcional)
        # Mas por simplicidade, vamos salvar direto
        texto = txt_anotacao.value or ""
        
        sucesso, mensagem, caminho = salvar_anotacao(texto)
            
    def carregar_anotacao_hoje():
        """
        Carrega a anotação do dia atual quando a tela é aberta
        """
        texto = carregar_anotacao()
        txt_anotacao.value = texto
        page.update()
    
    return salvar_anotacao_automatico, carregar_anotacao_hoje