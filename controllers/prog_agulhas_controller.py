import flet as ft
from models.prog_agulhas_model import (
    filtrar_dados,
    atualizar_status_model,
    inserir_novo_pedido,
    buscar_fornecedor_por_codigo,
    buscar_kardex_por_codigo
)
from controllers.transferir_qad_controller import criar_controller as criar_qad_controller

def criar_controller(
    page,
    tabela,
    btn_programar,
    btn_separar,
    btn_entregar,
    btn_transferir_qad,
    btn_imprimir,
    cb_impressora,
    ler_dados,
    salvar_no_arquivo,
    txt_codigo_field,
    atualizar_contador  # <--- 12º PARÂMETRO ADICIONADO
):

    # Criar controller do QAD
    transferir_qad = criar_qad_controller(page, tabela, ler_dados)

    linha_selecionada = None

    async def inserir_pedido(e, pedido_field, codigo_field, qtde_field, requisitante_field):
        pedido_base = pedido_field.value.strip()
        codigo = codigo_field.value.strip()
        qtde = qtde_field.value.strip()
        requisitante_digitado = requisitante_field.value.strip().lower()

        if not pedido_base or not codigo or not qtde:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Preencha todos os campos obrigatórios!"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            
            await codigo_field.focus()
            page.update()
            return

        fornecedor = buscar_fornecedor_por_codigo(codigo)
        kardex = buscar_kardex_por_codigo(codigo)
        
        if not fornecedor:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Código {codigo} não encontrado no itensAlmoxarifado.json!"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            
            await codigo_field.focus()
            page.update()
            return
        
        if not kardex:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Código {codigo} não encontrado no itensAlmoxarifado.json!"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            
            await codigo_field.focus()
            page.update()
            return

        mapa_requisitante = {
            "p": "Almoxarifado PARAISO",
            "1": "Almoxarifado PARAISO",
            "paraiso": "Almoxarifado PARAISO",
            "o": "PLANTA DE OUROS",
            "2": "PLANTA DE OUROS",
            "ouros": "PLANTA DE OUROS",
            "i": "PLANTA ITAJUBA",
            "3": "PLANTA ITAJUBA",
            "itajuba": "PLANTA ITAJUBA"
        }

        requisitante = mapa_requisitante.get(
            requisitante_digitado,
            requisitante_field.value.strip()
        )

        dados = ler_dados()

        novos_dados = inserir_novo_pedido(
            dados,
            pedido_base,
            kardex,
            codigo,
            qtde,
            requisitante,
            fornecedor
        )

        salvar_no_arquivo(novos_dados)

        codigo_field.value = ""
        qtde_field.value = ""
        requisitante_field.value = ""

        carregar_tabela("Pendente")
        
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Pedido inserido com sucesso!"),
            bgcolor="green"
        )
        page.snack_bar.open = True
        
        codigo_field.value = "PIN"
        await codigo_field.focus()
        
        page.update()

      
    def carregar_tabela(filtro_status="Pendente"):
        dados = ler_dados()
        tabela.rows.clear()
        
        # Controle de visibilidade dos botões e comboBox
        is_separando = (filtro_status == "Separando")
        
        cb_impressora.visible = is_separando
        btn_programar.visible = (filtro_status == "Pendente")
        btn_separar.visible = (filtro_status in ["Pendente", "Programado"])
        btn_entregar.visible = is_separando
        btn_transferir_qad.visible = is_separando
        btn_imprimir.visible = is_separando        

        dados_filtrados = filtrar_dados(dados, filtro_status)

        for item in dados_filtrados:
            # Criar checkbox
            checkbox = ft.Checkbox(value=False)
            
            # Função para lidar com o evento do checkbox
            def on_checkbox_change(e, cb=checkbox):
                atualizar_contador()
            
            checkbox.on_change = on_checkbox_change
            
            # Criar a linha inicialmente sem cor
            linha = ft.DataRow(
                cells=[
                    ft.DataCell(checkbox),                                # Coluna 0: Sel (será substituído)
                    ft.DataCell(ft.Text(item.get("pedido", ""))),       # Coluna 1: Pedido
                    ft.DataCell(ft.Text(item.get("kardex", ""))),       # Coluna 2: Kardex
                    ft.DataCell(ft.Text(item.get("codigo", ""))),       # Coluna 3: Código
                    ft.DataCell(ft.Text(item.get("qtde", ""))),         # Coluna 4: Qtde
                    ft.DataCell(ft.Text(item.get("fornecedor", ""))),   # Coluna 5: Fornecedor
                    ft.DataCell(ft.Text(item.get("requisitante", ""))), # Coluna 6: Requisitante
                    ft.DataCell(ft.Text(item.get("status", ""))),       # Coluna 7: Status
                ],
                color=None,
            )
            
            # Função para lidar com o clique na linha (SÓ MUDA A COR)
            def on_row_click(e, row=linha):
                nonlocal linha_selecionada  # Permite acessar a variável externa
                
                # Se já havia uma linha selecionada, remove a cor dela
                if linha_selecionada and linha_selecionada != row:
                    linha_selecionada.color = None
                
                # Alterna a cor da linha clicada
                if row.color == ft.Colors.LIGHT_BLUE_100:
                    row.color = None
                    linha_selecionada = None  # Remove a referência
                else:
                    row.color = ft.Colors.LIGHT_BLUE_100
                    linha_selecionada = row  # Guarda a referência da linha selecionada
                
                page.update()

            # Criar novas células com GestureDetector
            novas_celulas = []
            
            # Para a coluna do checkbox (índice 0), precisamos manter o checkbox acessível
            # Mas ainda queremos que o clique na área do checkbox também mude a cor
            checkbox_container = ft.GestureDetector(
                content=checkbox,
                on_tap=lambda e, r=linha: on_row_click(e, r)
            )
            novas_celulas.append(ft.DataCell(checkbox_container))
            
            # Para as demais colunas (1 a 7)
            for i in range(1, 8):  # Colunas 1 a 7
                conteudo = linha.cells[i].content
                container = ft.GestureDetector(
                    content=conteudo,
                    on_tap=lambda e, r=linha: on_row_click(e, r)
                )
                novas_celulas.append(ft.DataCell(container))
            
            # Substituir as células
            linha.cells = novas_celulas
            
            tabela.rows.append(linha)

        # Atualizar contador
        atualizar_contador()
        page.update()

        

    def atualizar_status(novo_status):
        dados = ler_dados()

        selecionados = []

        for row in tabela.rows:
            if _get_checkbox_value_from_cell(row.cells[0]):           
                pedido = _get_text_value_from_cell(row.cells[1], "")
                codigo = _get_text_value_from_cell(row.cells[3], "")
                selecionados.append((pedido, codigo))

        novos_dados, alterou = atualizar_status_model(
            dados,
            selecionados,
            novo_status
        )

        if alterou:
            salvar_no_arquivo(novos_dados)
            carregar_tabela()
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Status atualizado para: {novo_status}")
            )
            page.snack_bar.open = True
            page.update()

    return carregar_tabela, atualizar_status, inserir_pedido, transferir_qad

    
def _get_checkbox_value_from_cell(cell) -> bool:
    """
    Tenta retornar o valor booleano do checkbox na célula.
    Suporta:
    - Checkbox direto: DataCell(Checkbox(...))
    - Checkbox embrulhado: DataCell(GestureDetector(content=Checkbox(...)))
    Retorna False se não encontrar um checkbox válido.
    """
    if cell is None:
        return False

    ctrl = cell.content

    # Caso 1: a célula contém diretamente um Checkbox
    if isinstance(ctrl, ft.Checkbox):
        return bool(ctrl.value)

    # Caso 2: a célula contém um GestureDetector que contém um Checkbox
    if isinstance(ctrl, ft.GestureDetector):
        inner = ctrl.content
        if isinstance(inner, ft.Checkbox):
            return bool(inner.value)

    # Caso 3: outros wrappers (ex.: Container, Row, Column) – tente varrer filhos comuns
    try:
        # Tenta acessar ctrl.content repetidamente em wrappers comuns
        while hasattr(ctrl, "content") and ctrl is not getattr(ctrl, "content", None):
            ctrl = ctrl.content
            if isinstance(ctrl, ft.Checkbox):
                return bool(ctrl.value)
    except Exception:
        pass

    # Fallback: não achou
    return False

def _get_text_value_from_cell(cell, default: str = "") -> str:
    """
    Retorna o texto da célula, mesmo que esteja embrulhada em GestureDetector, Container, Row, etc.
    Suporta ft.Text, ft.TextField e tenta varrer children em Row/Column.
    """
    if cell is None:
        return default

    ctrl = cell.content

    # 1) Desembrulhar 'content' (GestureDetector, Container, etc.)
    visited = set()
    while True:
        # evita ciclos bizarros
        if id(ctrl) in visited:
            break
        visited.add(id(ctrl))

        # Casos diretos
        if isinstance(ctrl, ft.Text):
            return ctrl.value if ctrl.value is not None else default
        if isinstance(ctrl, ft.TextField):
            return ctrl.value if ctrl.value is not None else default

        # Alguns controles têm 'value'
        if hasattr(ctrl, "value") and ctrl.value is not None and not isinstance(ctrl, (ft.Checkbox,)):
            # cuidado para não confundir com Checkbox; aqui vale para TextField etc.
            return str(ctrl.value)

        # Desembrulhar .content se existir
        if hasattr(ctrl, "content") and ctrl.content is not None:
            ctrl = ctrl.content
            continue

        # Varrer filhos comuns (Row/Column/Stack)
        if hasattr(ctrl, "controls") and isinstance(ctrl.controls, list):
            # tenta encontrar o primeiro Text
            for ch in ctrl.controls:
                if isinstance(ch, ft.Text):
                    return ch.value if ch.value is not None else default
                if hasattr(ch, "content") and isinstance(ch.content, ft.Text):
                    return ch.content.value if ch.content.value is not None else default
            # se não achou, tenta o primeiro filho e continua
            if ctrl.controls:
                ctrl = ctrl.controls[0]
                continue

        # Não achou nada melhor
        break

    return default