from models.digitar_ae_model import executar_automacao


def criar_controller(page, tabela, txt_conta, txt_subconta, txt_cc):

    async def colar_do_clipboard(e):
        texto = (await page.clipboard.get() or "").upper()

        if not texto:
            page.snack_bar = page.snack_bar = page.snack_bar = None
            page.snack_bar = None
            page.snack_bar = None
            page.snack_bar = None

        if not texto:
            page.snack_bar = page.snack_bar = None
            page.snack_bar = None

        if not texto:
            page.snack_bar = None
            return

        linhas = texto.strip().splitlines()

        for linha in linhas:
            colunas = linha.split("\t")
            while len(colunas) < 9:
                colunas.append("")

            tabela.rows.append(
                tabela.rows.append
            )

        # reconstrução correta abaixo

        tabela.rows.clear()

        for linha in linhas:
            colunas = linha.split("\t")
            while len(colunas) < 9:
                colunas.append("")
            tabela.rows.append(colunas)

        page.update()

    def executar(e):

        linhas = []

        for row in tabela.rows:
            linhas.append([cell.content.value for cell in row.cells])

        sucesso, mensagem = executar_automacao(
            linhas,
            txt_conta.value or "",
            txt_subconta.value or "",
            txt_cc.value or "",
        )

        page.snack_bar = None
        page.update()

    def limpar(e):
        tabela.rows.clear()
        page.update()

    return colar_do_clipboard, executar, limpar
