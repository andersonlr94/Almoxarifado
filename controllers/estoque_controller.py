import flet as ft
from models.estoque_model import carregar_itens_almoxarifado, filtrar_itens


def criar_controller(page, tabela, txt_filtro, lbl_total):
    """
    Controller para a página de estoque
    """
    
    print("=== CRIANDO CONTROLLER ESTOQUE ===")
    
    # Mapeamento dos campos do JSON (com acentos e espaços) para os nomes da tabela
    # AGORA USANDO OS NOMES EXATOS DO SEU JSON
    mapeamento_campos = {
        "Id": "Id",
        "Kardex": "Kardex",
        "Código": "Código",
        "Descrição": "Descrição",
        "Loc novo": "Loc novo",
        "Qtde novo": "Qtde novo",
        "Loc retorno": "Loc retorno",
        "Qtde retorno": "Qtde retorno",
        "Fornecedor": "Fornecedor",
        "Provável fornecedor": "Provável fornecedor",
        "Ordem": "Ordem",
        "Lote Pedido": "Lote Pedido",
        "Lote Compra": "Lote Compra",
        "Leadtime": "Leadtime",
        "Fator Segurança": "Fator Segurança",
        "UM": "UM",
        "Pendente DPH": "Pendente DPH",
        "Pend. entrega compras": "Pend. entrega compras",
        "Pendente para SA": "Pendente para SA",
        "Lugar de uso": "Lugar de uso",
        "Custo": "Custo",
        "Curva custo": "Curva custo",
        "Consumo médio": "Consumo médio",
        "Curva demanda": "Curva demanda",
        "Equipamento": "Equipamento",
        "Tipo de uso": "Tipo de uso",
        "Estoque mínimo": "Estoque mínimo",
        "Estoque máximo": "Estoque máximo",
        "Estoque estratégico": "Estoque estratégico",
        "Mostrar cons. med./prog. no mês": "Mostrar cons. med./prog. no mês",
        "Separar p/ holder": "Separar p/ holder",
        "Separar p/ mesa": "Separar p/ mesa",
        "Item de estoque": "Item de estoque",
        "Pino de contato": "Pino de contato",
        "Ativo/Obsol.": "Ativo/Obsol.",
        "Classificação Fiscal": "Classificação Fiscal",
        "IPI": "IPI",
        "Observações": "Observações",
        "Doc. evidência": "Doc. evidência",
        "Descrição de evidência": "Descrição de evidência"
    }
    
    # Campos que são checkbox
    campos_checkbox = [
        "Mostrar cons. med./prog. no mês",
        "Separar p/ holder",
        "Separar p/ mesa",
        "Item de estoque",
        "Pino de contato"
    ]
    
    # Colunas da tabela
    colunas = list(mapeamento_campos.keys())
    
    def popular_tabela():
        """
        Popula a tabela com os dados filtrados
        """
        print("=== POPULANDO TABELA ===")
        
        # Carregar todos os itens
        todos_itens = carregar_itens_almoxarifado()
        print(f"Total de itens carregados: {len(todos_itens)}")
        
        # Aplicar filtro
        termo_busca = txt_filtro.value if txt_filtro.value else ""
        itens_filtrados = filtrar_itens(todos_itens, termo_busca)
        print(f"Itens após filtro: {len(itens_filtrados)}")
        
        # Limpar tabela
        tabela.rows.clear()
        
        # Adicionar linhas
        for idx, item in enumerate(itens_filtrados):
            if idx < 3:  # Mostrar apenas os 3 primeiros no debug
                print(f"Item {idx}: Código={item.get('Código')}, Descrição={item.get('Descrição')}")
            
            celulas = []
            
            for col in colunas:
                campo_json = mapeamento_campos.get(col, col)
                valor = item.get(campo_json, "")
                
                if col in campos_checkbox:
                    # Verificar valor booleano
                    is_checked = valor in [True, "True", "true", "S", "Sim", "sim", 1, "1"]
                    celulas.append(
                        ft.DataCell(
                            ft.Checkbox(value=is_checked, disabled=True)
                        )
                    )
                else:
                    # Texto normal
                    texto = str(valor) if valor not in [None, "null", ""] else ""
                    celulas.append(
                        ft.DataCell(
                            ft.Text(texto, size=11, no_wrap=False)
                        )
                    )
            
            linha = ft.DataRow(cells=celulas)
            tabela.rows.append(linha)
        
        # Atualizar contador
        lbl_total.value = f"Total: {len(itens_filtrados)} itens"
        page.update()
        print(f"✅ Tabela atualizada com {len(tabela.rows)} linhas")
    
    def filtrar_tabela(e):
        """
        Função chamada quando o filtro é alterado
        """
        print(f"=== FILTRANDO TABELA: {txt_filtro.value} ===")
        popular_tabela()
    
    # Carregar dados iniciais
    print("Carregando dados iniciais...")
    popular_tabela()
    
    return popular_tabela, filtrar_tabela