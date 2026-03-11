import flet as ft
from models.digitar_ae_model import executar_automacao


def criar_controller(page, tabela, txt_conta, txt_subconta, txt_cc):

    async def colar_do_clipboard(e):
        texto = (await page.clipboard.get() or "").upper()

        if not texto:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Área de transferência vazia!"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        linhas = texto.strip().splitlines()
        
        # Limpar tabela atual
        tabela.rows.clear()

        # Adicionar novas linhas
        for linha in linhas:
            colunas = linha.split("\t")

            # Garantir que tenha 9 colunas (0..8)
            while len(colunas) < 9:
                colunas.append("")

            # --- Regra solicitada: se a coluna "C-M" (índice 8) vier vazia, preencher com "C"
            cm_val = (colunas[8] or "").strip().upper()
            if not cm_val:
                cm_val = "C"
            colunas[8] = cm_val
            # ------------------------------------------------------------------------------

            # Criar DataRow com DataCells
            nova_linha = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(colunas[0])),  # Gerar
                    ft.DataCell(ft.Text(colunas[1])),  # Item
                    ft.DataCell(ft.Text(colunas[2])),  # Descrição
                    ft.DataCell(ft.Text(colunas[3])),  # Qtde
                    ft.DataCell(ft.Text(colunas[4])),  # UM
                    ft.DataCell(ft.Text(colunas[5])),  # Custo
                    ft.DataCell(ft.Text(colunas[6])),  # Classificação fiscal
                    ft.DataCell(ft.Text(colunas[7])),  # Classe de imposto
                    ft.DataCell(ft.Text(colunas[8])),  # C-M (já normalizado)
                ]
            )
            tabela.rows.append(nova_linha)

        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"{len(linhas)} linha(s) colada(s) com sucesso!"),
            bgcolor="green"
        )
        page.snack_bar.open = True
        page.update()

    def executar(e):
        linhas = []
        for row in tabela.rows:
            linha = []
            for cell in row.cells:
                linha.append(cell.content.value)
            # (Opcional) Reforçar a regra também no momento de execução
            if len(linha) >= 9:
                cm_val = (linha[8] or "").strip().upper()
                if not cm_val:
                    linha[8] = "C"
            linhas.append(linha)

        sucesso, mensagem = executar_automacao(
            linhas,
            txt_conta.value or "",
            txt_subconta.value or "",
            txt_cc.value or "",
        )

        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensagem),
            bgcolor="green" if sucesso else "red"
        )
        page.snack_bar.open = True
        page.update()

    def limpar(e):
        tabela.rows.clear()
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Tabela limpa!"),
            bgcolor="blue"
        )
        page.snack_bar.open = True
        page.update()

    return colar_do_clipboard, executar, limpar