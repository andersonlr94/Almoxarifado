import flet as ft
from models.estoque_model import carregar_itens_almoxarifado, filtrar_itens

def criar_linha(item, colunas):
    return ft.Container(
        padding=6,
        bgcolor=ft.Colors.WHITE,
        content=ft.Row(
            controls=[
                ft.Text(
                    str(item.get(col, "")),
                    size=11,
                    no_wrap=True,
                    width=140
                )
                for col in colunas
            ],
            spacing=5,
        ),
    )

def criar_controller(page, lista_linhas, txt_filtro, lbl_total):
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
        print("=== popular_tabela() EXECUTADA ===")
        todos_itens = carregar_itens_almoxarifado()
        print(f"Quantidade de itens lidos do JSON: {len(todos_itens)}")

        termo = txt_filtro.value or ""
        itens_filtrados = filtrar_itens(todos_itens, termo)

        lista_linhas.controls.clear()

        for item in itens_filtrados:
            lista_linhas.controls.append(
                criar_linha(item, colunas)
            )

        lbl_total.value = f"Total: {len(itens_filtrados)} itens"
        page.update()
    
    def filtrar_tabela(e):
        """
        Função chamada quando o filtro é alterado
        """
        print(f"=== FILTRANDO TABELA: {txt_filtro.value} ===")
        popular_tabela()
    
    async def atualizar_estoque(e=None):
        """
        Atualiza a tabela de estoque colando dados copiados de uma JTable.
        Garante que cada DataRow tenha exatamente o mesmo número de colunas
        da DataTable, completando com valores vazios quando necessário.
        """
        texto = (await page.clipboard.get() or "").strip()

        if not texto:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Área de transferência vazia!"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        linhas = [ln for ln in texto.splitlines() if ln.strip()]

        if not linhas:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Nada para atualizar."),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        # Número total de colunas da tabela (ex.: 40)
        total_colunas = len(tabela.columns)

        for ln in linhas:
            # JTable normalmente vem separada por TAB
            colunas = ln.split("\t")

            celulas = []

            # Garante que cada linha tenha exatamente 'total_colunas' células
            for i in range(total_colunas):
                valor = colunas[i].strip() if i < len(colunas) else ""
                celulas.append(
                    ft.DataCell(
                        ft.Text(valor, size=11, no_wrap=False)
                    )
                )


        lbl_total.value = f"Total: {len(tabela.rows)} itens (JTable)"
        page.update()


    return popular_tabela, filtrar_tabela, atualizar_estoque