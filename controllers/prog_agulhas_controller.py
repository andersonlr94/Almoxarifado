import flet as ft
from models.prog_agulhas_model import filtrar_dados, atualizar_status_model

from models.prog_agulhas_model import (
    filtrar_dados,
    atualizar_status_model,
    inserir_novo_pedido
)


def criar_controller(page,
    tabela,
    btn_programar,
    btn_separar,
    btn_entregar,
    ler_dados,
    salvar_no_arquivo):

    def inserir_pedido(pedido_field, codigo_field, qtde_field, requisitante_field):

        pedido_base = pedido_field.value.strip()
        codigo = codigo_field.value.strip()
        qtde = qtde_field.value.strip()
        requisitante_digitado = requisitante_field.value.strip().lower()

        requisitante_digitado = requisitante_field.value.strip().lower()

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


        if not pedido_base:
            return

        dados = ler_dados()

        novos_dados = inserir_novo_pedido(
            dados,
            pedido_base,
            codigo,
            qtde,
            requisitante
        )

        salvar_no_arquivo(novos_dados)

        # Limpar campos
        codigo_field.value = ""
        qtde_field.value = ""
        requisitante_field.value = ""

        carregar_tabela("Pendente")
        page.update()

      
    def carregar_tabela(filtro_status="Pendente"):
        dados = ler_dados()
        tabela.rows.clear()
        
        btn_programar.visible = (filtro_status == "Pendente")
        btn_separar.visible = (filtro_status in ["Pendente", "Programado"])
        btn_entregar.visible = (filtro_status == "Separando")

        dados_filtrados = filtrar_dados(dados, filtro_status)

        for item in dados_filtrados:
            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Checkbox(value=False)),
                        ft.DataCell(ft.Text(item.get("pedido", ""))),
                        ft.DataCell(ft.Text(item.get("codigo", ""))),
                        ft.DataCell(ft.Text(item.get("qtde", ""))),
                        ft.DataCell(ft.Text(item.get("requisitante", ""))),
                        ft.DataCell(ft.Text(item.get("status", ""))),
                    ]
                )
            )

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
                ft.Text(f"Status atualizado para: {novo_status}")
            )
            page.snack_bar.open = True
            page.update()

    return carregar_tabela, atualizar_status, inserir_pedido

