import flet as ft
from models.imprimir_model import imprimir_multiplas_etiquetas

def criar_controller(page, tabela, cb_impressora):
    """
    Cria o controller para o botão de imprimir
    
    Args:
        page: Página do Flet
        tabela: Tabela com os dados
        cb_impressora: ComboBox com as opções de destino
    
    Returns:
        function: Função que será chamada ao clicar no botão imprimir
    """
    
    def imprimir(e):
        """
        Função chamada quando o botão Imprimir é clicado
        """
        print("\n" + "="*50)
        print("=== BOTÃO IMPRIMIR CLICADO ===")
        print("="*50)
        
        # Obter o destino selecionado
        destino = cb_impressora.value
        print(f"Destino selecionado: {destino}")
        
        # Obter os itens selecionados
        itens_selecionados = []
        
        print(f"\nTotal de linhas na tabela: {len(tabela.rows)}")
        
        for i, row in enumerate(tabela.rows):
            print(f"\n--- Linha {i+1} ---")
            print(f"Checkbox valor: {row.cells[0].content.value}")
            
            if row.cells[0].content.value:  # Se o checkbox está marcado
                # IMPORTANTE: Agora são 8 colunas (0 a 7)
                pedido = row.cells[1].content.value      # Coluna 1: Pedido
                kardex = row.cells[2].content.value      # Coluna 2: Kardex
                codigo = row.cells[3].content.value      # Coluna 3: Código
                quantidade = row.cells[4].content.value  # Coluna 4: Qtde
                fornecedor = row.cells[5].content.value  # Coluna 5: Fornecedor
                requisitante = row.cells[6].content.value # Coluna 6: Requisitante
                status = row.cells[7].content.value      # Coluna 7: Status
                
                print(f"  Pedido: '{pedido}'")
                print(f"  Kardex: '{kardex}'")
                print(f"  Código: '{codigo}'")
                print(f"  Qtde: '{quantidade}'")
                print(f"  Fornecedor: '{fornecedor}'")
                print(f"  Requisitante: '{requisitante}'")
                print(f"  Status: '{status}'")
                
                itens_selecionados.append((pedido, kardex, codigo, quantidade, requisitante, fornecedor))
            else:
                print("  Linha não selecionada")
        
        if not itens_selecionados:
            print("\n❌ Nenhum item selecionado")
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Selecione pelo menos um item!"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return
        
        print(f"\n✅ Total de itens selecionados: {len(itens_selecionados)}")
        
        # Mostrar mensagem de processamento
        acao = "Salvando" if destino == "Salvar como PDF" else "Imprimindo"
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"{acao} {len(itens_selecionados)} etiqueta(s)...\nBuscando localizações..."),
            bgcolor="blue"
        )
        page.snack_bar.open = True
        page.update()
        
        # Chamar a função de impressão com o destino selecionado
        print("\n🔄 Chamando imprimir_multiplas_etiquetas...")
        sucesso, mensagem = imprimir_multiplas_etiquetas(itens_selecionados, destino)
        
        print(f"\n📋 Resultado final:")
        print(f"  Sucesso: {sucesso}")
        print(f"  Mensagem: {mensagem}")
        
        if sucesso:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(mensagem),
                bgcolor="green"
            )
        else:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(mensagem),
                bgcolor="red"
            )
        
        page.snack_bar.open = True
        page.update()
        print("="*50 + "\n")
    
    return imprimir