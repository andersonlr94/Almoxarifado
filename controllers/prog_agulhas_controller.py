import flet as ft
from models.prog_agulhas_model import (
    filtrar_dados,
    atualizar_status_model,
    inserir_novo_pedido,
    buscar_fornecedor_por_codigo,
    buscar_kardex_por_codigo
)
from controllers.transferir_qad_controller import criar_controller as criar_qad_controller

def criar_controller(page,
    tabela,
    btn_programar,
    btn_separar,
    btn_entregar,
    btn_transferir_qad,
    ler_dados,
    salvar_no_arquivo,
    txt_codigo_field):

    print("=== CRIANDO CONTROLLER PROG_AGULHAS ===")
    
    # Criar controller do QAD
    transferir_qad = criar_qad_controller(page, tabela, ler_dados)
    print(f"Função transferir_qad criada: {transferir_qad}")

    async def inserir_pedido(e, pedido_field, codigo_field, qtde_field, requisitante_field):
        print("=== INSERIR PEDIDO ===")
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

        mapa_requisitante = {
            "p": "Paraiso",
            "paraiso": "Paraiso",
            "o": "Ouros",
            "ouros": "Ouros",
            "i": "Itajuba",
            "itajuba": "Itajuba"
        }

        requisitante = mapa_requisitante.get(
            requisitante_digitado,
            requisitante_field.value.strip()
        )

        dados = ler_dados()
        print(f"Dados carregados: {len(dados)} itens")

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
        print(f"Novo pedido inserido: {pedido_base}")

        pedido_field.value = ""
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
        print(f"=== CARREGAR TABELA: {filtro_status} ===")
        dados = ler_dados()
        tabela.rows.clear()
        
        btn_programar.visible = (filtro_status == "Pendente")
        btn_separar.visible = (filtro_status in ["Pendente", "Programado"])
        btn_entregar.visible = (filtro_status == "Separando")
        btn_transferir_qad.visible = (filtro_status == "Separando")
        
        print(f"Botões - Programar: {btn_programar.visible}, Separar: {btn_separar.visible}, Entregar: {btn_entregar.visible}, Transferir QAD: {btn_transferir_qad.visible}")

        dados_filtrados = filtrar_dados(dados, filtro_status)
        print(f"Total de itens filtrados: {len(dados_filtrados)}")

        for i, item in enumerate(dados_filtrados):
            print(f"Item {i+1}: {item.get('pedido')} - {item.get('status')}")
            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Checkbox(value=False)),
                        ft.DataCell(ft.Text(item.get("pedido", ""))),
                        ft.DataCell(ft.Text(item.get("kardex", ""))),
                        ft.DataCell(ft.Text(item.get("codigo", ""))),
                        ft.DataCell(ft.Text(item.get("qtde", ""))),
                        ft.DataCell(ft.Text(item.get("fornecedor", ""))),
                        ft.DataCell(ft.Text(item.get("requisitante", ""))),
                        ft.DataCell(ft.Text(item.get("status", ""))),
                    ]
                )
            )

        page.update()

    def atualizar_status(novo_status):
        print(f"=== ATUALIZAR STATUS: {novo_status} ===")
        dados = ler_dados()

        selecionados = []

        for i, row in enumerate(tabela.rows):
            if row.cells[0].content.value:
                pedido = row.cells[1].content.value
                codigo = row.cells[2].content.value
                selecionados.append((pedido, codigo))
                print(f"Selecionado: {pedido} - {codigo}")

        print(f"Total selecionados: {len(selecionados)}")

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
        else:
            print("Nenhum item foi alterado")

    print("=== CONTROLLER PROG_AGULHAS CRIADO ===")
    return carregar_tabela, atualizar_status, inserir_pedido, transferir_qad