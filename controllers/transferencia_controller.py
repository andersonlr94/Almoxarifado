# controllers/transferencia_controller.py
import flet as ft

def criar_controller(
    page: ft.Page,
    tabela: ft.DataTable,
    tf_de_local: ft.TextField,
    tf_de_lugar: ft.TextField,
    tf_de_lote: ft.TextField,
    tf_para_local: ft.TextField,
    tf_para_lugar: ft.TextField,
    tf_para_lote: ft.TextField,
):
    async def carregar(e=None):
        texto = (await page.clipboard.get() or "").upper()

        if not texto.strip():
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Área de transferência vazia!"),
                bgcolor="red",
            )
            page.snack_bar.open = True
            page.update()
            return

        linhas = [ln for ln in texto.strip().splitlines() if ln.strip()]
        tabela.rows.clear()

        for ln in linhas:
            # aceita TAB; se quiser, trate ';' e ',' também
            cols = ln.split("\t")
            while len(cols) < 2:
                cols.append("")
            kardex = (cols[0] or "").strip()
            qtde   = (cols[1] or "").strip()

            # (opcional) normalizar qtde p/ apenas dígitos:
            # qtde = "".join(ch for ch in qtde if ch.isdigit())

            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(kardex)),
                    ft.DataCell(ft.Text(qtde)),
                ]
            )
            # se quiser usar depois: row.data = {"kardex": kardex, "qtde": qtde}
            tabela.rows.append(row)

        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"{len(linhas)} linha(s) colada(s) com sucesso!"),
            bgcolor="green",
        )
        page.snack_bar.open = True
        page.update()

    def limpar(e=None):
        tabela.rows.clear()
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Tabela limpa!"),
            bgcolor="blue",
        )
        page.snack_bar.open = True
        page.update()

    return carregar, limpar