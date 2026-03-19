# controllers/transferencia_controller.py
import flet as ft
import time

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
    # ---------------------------
    # 1) CARREGAR do Clipboard (Kardex, Qtde)
    # ---------------------------
    async def carregar(e=None):
        try:
            texto = (await page.clipboard.get() or "").upper()
            if not texto.strip():
                page.snack_bar = ft.SnackBar(ft.Text("Área de transferência vazia!"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return

            linhas = [ln for ln in texto.strip().splitlines() if ln.strip()]
            if not linhas:
                page.snack_bar = ft.SnackBar(ft.Text("Nada para colar!"), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return

            tabela.rows.clear()

            for ln in linhas:
                # aceita TAB por padrão; se quiser ; ou , troque conforme necessidade
                if "\t" in ln:
                    cols = ln.split("\t")
                elif ";" in ln:
                    cols = ln.split(";")
                elif "," in ln:
                    cols = ln.split(",")
                else:
                    cols = [ln]

                while len(cols) < 2:
                    cols.append("")

                kardex = (cols[0] or "").strip()
                qtde   = (cols[1] or "").strip()

                tabela.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(kardex)),
                            ft.DataCell(ft.Text(qtde)),
                        ]
                    )
                )

            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"{len(linhas)} linha(s) colada(s) com sucesso!"),
                bgcolor="green",
            )
            page.snack_bar.open = True
            page.update()

        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao colar: {ex}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    # ---------------------------
    # 2) LIMPAR tabela
    # ---------------------------
    def limpar(e=None):
        tabela.rows.clear()
        page.snack_bar = ft.SnackBar(ft.Text("Tabela limpa!"), bgcolor="blue")
        page.snack_bar.open = True
        page.update()

    # ---------------------------
    # 3) TRANSFERIR (pyautogui)
    # ---------------------------
    def transferir(e=None):
        try:
            import pyautogui
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"pyautogui não encontrado: {ex}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        total = len(tabela.rows)
        if total == 0:
            page.snack_bar = ft.SnackBar(ft.Text("Não há linhas na tabela para transferir."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # Captura valores dos campos
        de_local   = (tf_de_local.value   or "").strip()
        de_lugar   = (tf_de_lugar.value   or "").strip()
        de_lote    = (tf_de_lote.value    or "").strip()
        para_local = (tf_para_local.value or "").strip()
        para_lugar = (tf_para_lugar.value or "").strip()
        para_lote  = (tf_para_lote.value  or "").strip()

        # Aviso e countdown para focar a janela alvo
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Atenção: foque a janela de destino. Começando em 3 segundos..."),
            bgcolor="orange",
        )
        page.snack_bar.open = True
        page.update()
        time.sleep(1)
        for c in [2, 1]:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Começando em {c}..."), bgcolor="orange")
            page.snack_bar.open = True
            page.update()
            time.sleep(1)

        # Configuração de segurança do pyautogui
        pyautogui.FAILSAFE = True   # mover mouse para canto sup-esq para abortar
        pyautogui.PAUSE = .5      # pequeno intervalo entre comandos

        try:
            for idx, row in enumerate(tabela.rows, start=1):
                # Extrai texto da célula (Text)
                kardex = str(getattr(row.cells[0].content, "value", "") or "").strip()
                qtde   = str(getattr(row.cells[1].content, "value", "") or "").strip()

                # --- Sequência solicitada por item ---
                # 1) Kardex (primeira coluna)
                pyautogui.write(kardex)
                pyautogui.press("enter")

                # 2) Qtde (segunda coluna)
                pyautogui.write(qtde)
                pyautogui.press("enter", presses=5, interval=0.03)

                # 3) "TransfI"
                pyautogui.write("TransfI")
                pyautogui.press("enter", presses=2, interval=0.03)

                # 4) De Local / De Lugar / De Lote / Enter
                pyautogui.write(de_local)
                pyautogui.press("enter")

                pyautogui.write(de_lugar)
                pyautogui.press("enter")

                pyautogui.write(de_lote)
                pyautogui.press("enter")

                pyautogui.press("enter")  # enter adicional

                # 5) Para Local / Para Lugar / Para Lote / 3x Enter
                pyautogui.write(para_local)
                pyautogui.press("enter")

                pyautogui.write(para_lugar)
                pyautogui.press("enter")

                pyautogui.write(para_lote)
                pyautogui.press("enter", presses=3, interval=0.03)

                pyautogui.press("f4")

                # Feedback a cada item (opcional)
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Transferido item {idx}/{total}: {kardex} ({qtde})"),
                    bgcolor="green",
                )
                page.snack_bar.open = True
                page.update()
                time.sleep(0.2)  # pequena folga entre itens

            # Final
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Transferência concluída para {total} linha(s)!"),
                bgcolor="green"
            )
            page.snack_bar.open = True
            page.update()

        except pyautogui.FailSafeException:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Automação abortada (PyAutoGUI FailSafe)."),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Erro durante automação: {ex}"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()

    return carregar, limpar, transferir