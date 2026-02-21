import flet as ft
import time
from models.digitar_qad_model import executar_sequencia_qad

def criar_controller(page, tabela, ler_dados):

    def transferir_qad(e):
        # Obter os pedidos selecionados
        selecionados = []
        print("Botão Transferir QAD clicado")
        
        for row in tabela.rows:
            if row.cells[0].content.value:  # Se o checkbox está marcado
                kardex = row.cells[2].content.value  # Pedido = kardex
                qtde = row.cells[4].content.value    # Quantidade
                selecionados.append((kardex, qtde))
                print(f"Item selecionado: {kardex} - Qtde: {qtde}")
        
        if not selecionados:
            print("Nenhum item selecionado")
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Selecione pelo menos um pedido!"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return
        
        # Executar direto, sem diálogo de confirmação
        print(f"Iniciando transferência de {len(selecionados)} item(ns)")
        
        # Pequena pausa para o usuário posicionar o cursor no QAD
        time.sleep(2)
        
        for i, (kardex, qtde) in enumerate(selecionados):
            print(f"Processando item {i+1}: {kardex} - {qtde}")
            
            # Mostrar snackbar informando início
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Transferindo pedido {kardex}..."),
                bgcolor="blue"
            )
            page.snack_bar.open = True
            page.update()
            
            # Executar a sequência
            sucesso, mensagem = executar_sequencia_qad(kardex, qtde)
            print(f"Resultado: {sucesso} - {mensagem}")
            
            if not sucesso:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Erro: {mensagem}"),
                    bgcolor="red"
                )
                page.snack_bar.open = True
                page.update()
                break
            else:
                # Pequena pausa entre transferências
                time.sleep(1)
        
        # Mensagem final
        if sucesso:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"{len(selecionados)} transferência(s) concluída(s)!"),
                bgcolor="green"
            )
            page.snack_bar.open = True
            page.update()
    
    return transferir_qad