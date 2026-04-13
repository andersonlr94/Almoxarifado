import flet as ft
from models.reajuste_preco_model import (
    ler_reajustes,
    adicionar_reajuste,
    excluir_reajuste,
    atualizar_campo,
    salvar_reajustes
)

# Colunas da tabela (Fornecedor agora é a primeira coluna)
COLUNAS = [
    "Fornecedor",
    "Kardex",
    "Item", 
    "Descrição",
    "Preço antigo",
    "Data pedido reajuste",
    "Status",
    "Observação"
]

def criar_celula_editavel(campo, valor_atual, indice, tabela, page, largura=150):
    """Cria uma célula editável para Status e Observação"""
    
    container = ft.Container(
        content=ft.Text(valor_atual or "", size=12),
        padding=5,
        border=ft.border.all(0.5, ft.Colors.GREY_300),
        border_radius=3,
    )
    
    def entrar_edicao(e):
        campo_texto = ft.TextField(
            value=valor_atual or "",
            autofocus=True,
            width=largura,
            text_size=12,
            height=35,
            dense=True,
            border=ft.InputBorder.OUTLINE,
        )
        
        async def salvar_edicao(ev):
            novo_valor = campo_texto.value.strip()
            if novo_valor != valor_atual:
                atualizar_campo(indice, campo, novo_valor)
            dados = ler_reajustes()
            popular_tabela(tabela, dados, page)
            page.update()
        
        campo_texto.on_submit = salvar_edicao
        campo_texto.on_blur = salvar_edicao
        
        container.content = campo_texto
        page.update()
    
    container.on_click = entrar_edicao
    return container

def popular_tabela(tabela: ft.DataTable, dados, page: ft.Page):
    """Popula a tabela com os dados"""
    tabela.rows.clear()
    
    for idx, item in enumerate(dados):
        cells = []
        
        for col in COLUNAS:
            valor = item.get(col, "")
            
            if col in ["Status", "Observação"]:
                # Células editáveis
                largura = 150 if col == "Status" else 250
                cell_content = criar_celula_editavel(col, valor, idx, tabela, page, largura)
                cells.append(ft.DataCell(cell_content))
            else:
                # Células não editáveis
                cells.append(
                    ft.DataCell(
                        ft.Text(str(valor) if valor else "", size=11, no_wrap=False)
                    )
                )
        
        linha = ft.DataRow(cells=cells)
        tabela.rows.append(linha)
    
    page.update()

def criar_controller(page, tabela, txt_fornecedor, txt_kardex, txt_item, txt_descricao, txt_preco_antigo, btn_excluir):
    """Cria o controller para a tela de reajuste de preços"""
    
    linha_atual_selecionada = None
    
    def carregar_tabela():
        """Carrega os dados na tabela"""
        nonlocal linha_atual_selecionada
        dados = ler_reajustes()
        
        # Verificar se a linha selecionada ainda existe
        if linha_atual_selecionada is not None and linha_atual_selecionada >= len(dados):
            linha_atual_selecionada = None
        
        popular_tabela(tabela, dados, page)
        
        # Restaurar seleção visual
        for idx, row in enumerate(tabela.rows):
            row.color = ft.Colors.LIGHT_BLUE_100 if idx == linha_atual_selecionada else None
        
        # Atualizar visibilidade do botão excluir
        btn_excluir.visible = linha_atual_selecionada is not None
        page.update()
    
    def on_row_click(row_index):
        """Evento chamado quando uma linha é clicada"""
        nonlocal linha_atual_selecionada
        
        if linha_atual_selecionada == row_index:
            linha_atual_selecionada = None
        else:
            linha_atual_selecionada = row_index
        
        # Atualizar cores das linhas
        for idx, row in enumerate(tabela.rows):
            if idx == linha_atual_selecionada:
                row.color = ft.Colors.LIGHT_BLUE_100
            else:
                row.color = None
        
        btn_excluir.visible = linha_atual_selecionada is not None
        page.update()
    
    def adicionar_eventos_clique():
        """Adiciona eventos de clique a todas as linhas da tabela"""
        for idx, row in enumerate(tabela.rows):
            def criar_clique_handler(i):
                return lambda e: on_row_click(i)
            
            novas_celulas = []
            for cell in row.cells:
                conteudo_original = cell.content
                detector = ft.GestureDetector(
                    content=conteudo_original,
                    on_tap=criar_clique_handler(idx),
                )
                novas_celulas.append(ft.DataCell(detector))
            row.cells = novas_celulas
        
        page.update()
    
    def inserir_reajuste(e):
        """Insere um novo reajuste"""
        nonlocal linha_atual_selecionada
        
        fornecedor = txt_fornecedor.value.strip()
        kardex = txt_kardex.value.strip()
        item = txt_item.value.strip()
        descricao = txt_descricao.value.strip()
        preco_antigo = txt_preco_antigo.value.strip()
        
        # Validação básica (Fornecedor agora é obrigatório)
        if not fornecedor or not kardex or not item or not descricao or not preco_antigo:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Preencha todos os campos!"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return
        
        # Adicionar reajuste
        adicionar_reajuste(fornecedor, kardex, item, descricao, preco_antigo)
        
        # Limpar campos (exceto Fornecedor)
        txt_kardex.value = ""
        txt_item.value = ""
        txt_descricao.value = ""
        txt_preco_antigo.value = ""
        # txt_fornecedor NÃO é limpo!
        
        # Limpar seleção
        linha_atual_selecionada = None
        
        # Recarregar tabela
        carregar_tabela()
        adicionar_eventos_clique()
        
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Reajuste adicionado com sucesso!"),
            bgcolor="green"
        )
        page.snack_bar.open = True
        page.update()
    
    def excluir_reajuste_selecionado(e):
        """Exclui o reajuste selecionado"""
        nonlocal linha_atual_selecionada
        
        if linha_atual_selecionada is None:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Selecione um item para excluir!"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return
        
        def confirmar_exclusao(ev):
            nonlocal linha_atual_selecionada
            dialog.open = False
            page.update()
            
            sucesso, removido = excluir_reajuste(linha_atual_selecionada)
            if sucesso:
                linha_atual_selecionada = None
                carregar_tabela()
                adicionar_eventos_clique()
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Item excluído com sucesso!"),
                    bgcolor="green"
                )
                page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Erro ao excluir item!"),
                    bgcolor="red"
                )
                page.snack_bar.open = True
            page.update()
        
        def cancelar_exclusao(ev):
            dialog.open = False
            page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar exclusão"),
            content=ft.Text("Tem certeza que deseja excluir este reajuste?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_exclusao),
                ft.ElevatedButton(
                    "Excluir",
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE,
                    on_click=confirmar_exclusao,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.overlay.clear()
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
    
    carregar_tabela()
    adicionar_eventos_clique()
    
    return inserir_reajuste, excluir_reajuste_selecionado, carregar_tabela