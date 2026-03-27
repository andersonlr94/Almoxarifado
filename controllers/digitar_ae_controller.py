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
        
        # ================= NOVA LÓGICA DE AGRUPAMENTO =================
        # Dicionário para agrupar por item (coluna 1)
        agrupados = {}
        
        for linha in linhas:
            colunas = linha.split("\t")
            
            # Garantir que tenha 9 colunas
            while len(colunas) < 9:
                colunas.append("")
            
            # Tratar C-M (coluna 8)
            cm_val = (colunas[8] or "").strip().upper()
            if not cm_val:
                cm_val = "C"
            colunas[8] = cm_val
            
            # Pegar o item (coluna 1 - índice 1) e quantidade (coluna 4 - índice 4)
            item = colunas[1].strip()
            quantidade = colunas[3].strip()  # Qtde está na coluna 3? Vou verificar
            
            # Converter quantidade para número
            try:
                qtde_num = float(quantidade) if quantidade else 0
            except ValueError:
                qtde_num = 0
            
            if item not in agrupados:
                # Guarda a linha original e a quantidade
                agrupados[item] = {
                    "colunas": colunas.copy(),
                    "qtde_total": qtde_num,
                    "qtde_original": colunas[3]  # Guarda o valor original para referência
                }
            else:
                # Item duplicado: soma a quantidade
                agrupados[item]["qtde_total"] += qtde_num
        
        # Limpar tabela atual
        tabela.rows.clear()
        
        # Criar linhas agrupadas
        for item, dados in agrupados.items():
            colunas = dados["colunas"]
            
            # Atualizar a quantidade com o valor somado
            qtde_total = dados["qtde_total"]
            # Formatar sem decimais se for inteiro
            if qtde_total.is_integer():
                colunas[3] = str(int(qtde_total))
            else:
                colunas[3] = str(qtde_total)
            
            # Criar DataRow com DataCells
            nova_linha = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(colunas[0])),  # Gerar
                    ft.DataCell(ft.Text(colunas[1])),  # Item
                    ft.DataCell(ft.Text(colunas[2])),  # Descrição
                    ft.DataCell(ft.Text(colunas[3])),  # Qtde (somada)
                    ft.DataCell(ft.Text(colunas[4])),  # UM
                    ft.DataCell(ft.Text(colunas[5])),  # Custo
                    ft.DataCell(ft.Text(colunas[6])),  # Classificação fiscal
                    ft.DataCell(ft.Text(colunas[7])),  # Classe de imposto
                    ft.DataCell(ft.Text(colunas[8])),  # C-M
                ]
            )
            tabela.rows.append(nova_linha)
        
        # Mostrar mensagem com informações de agrupamento
        total_original = len(linhas)
        total_agrupado = len(agrupados)
        if total_agrupado < total_original:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"{total_original} linha(s) colada(s) → {total_agrupado} linha(s) após agrupar itens duplicados!"),
                bgcolor="orange"
            )
        else:
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
            # Reforçar a regra do C-M
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