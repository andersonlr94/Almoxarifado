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
            # Criar checkbox com evento para atualizar contador
            checkbox = ft.Checkbox(value=False)
            
            # Função para lidar com o evento do checkbox
            def on_checkbox_change(e):
                atualizar_contador()
            
            checkbox.on_change = on_checkbox_change
            
            linha = ft.DataRow(
                cells=[
                    ft.DataCell(checkbox),                                # Coluna 0: Sel
                    ft.DataCell(ft.Text(item.get("pedido", ""))),       # Coluna 1: Pedido
                    ft.DataCell(ft.Text(item.get("kardex", ""))),       # Coluna 2: Kardex
                    ft.DataCell(ft.Text(item.get("codigo", ""))),       # Coluna 3: Código
                    ft.DataCell(ft.Text(item.get("qtde", ""))),         # Coluna 4: Qtde
                    ft.DataCell(ft.Text(item.get("fornecedor", ""))),   # Coluna 5: Fornecedor
                    ft.DataCell(ft.Text(item.get("requisitante", ""))), # Coluna 6: Requisitante
                    ft.DataCell(ft.Text(item.get("status", ""))),       # Coluna 7: Status
                ]
            )
            tabela.rows.append(linha)

        # Atualizar contador
        atualizar_contador()
        page.update()

    def atualizar_status(novo_status):
        dados = ler_dados()

        selecionados = []

        for row in tabela.rows:
            if row.cells[0].content.value:
                pedido = row.cells[1].content.value
                codigo = row.cells[3].content.value
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