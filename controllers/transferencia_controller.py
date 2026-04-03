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
    rg_terceira_coluna,
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
                lote   = (cols[2] or "").strip() if len(cols) >= 3 else ""

                tabela.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(kardex)),
                            ft.DataCell(ft.Text(qtde)),
                            ft.DataCell(ft.Text(lote)),
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
        modo = rg_terceira_coluna.value

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

                # 1) Extrai valores da linha (ORDEM CORRETA)
                kardex = str(getattr(row.cells[0].content, "value", "") or "").strip()
                qtde = str(getattr(row.cells[1].content, "value", "") or "").strip()
                lote_coluna = str(getattr(row.cells[2].content, "value", "") or "").strip()

                # 2) Validação obrigatória quando a 3ª coluna é usada
                if modo in ("lote_inicial", "lote_destino") and not lote_coluna:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text(
                            f"Lote vazio na linha {idx}.\n"
                            "Quando usar este modo, a terceira coluna deve estar preenchida."
                        ),
                        bgcolor="red",
                    )
                    page.snack_bar.open = True
                    page.update()
                    return   # ⛔ interrompe corretamente

                # 3) Valores padrão (modo formulário)
                lote_inicial = tf_de_lote.value or ""
                lote_destino = tf_para_lote.value or ""

                # 4) Aplica regra do RadioButton
                if modo == "lote_inicial":
                    lote_inicial = lote_coluna
                elif modo == "lote_destino":
                    lote_destino = lote_coluna

                # 5) PyAutoGUI (executa AGORA sim)
                pyautogui.write(kardex)
                pyautogui.press("enter")

                pyautogui.write(qtde)
                pyautogui.press("enter", presses=5, interval=0.03)

                pyautogui.write("TransfI")
                pyautogui.press("enter", presses=2, interval=0.03)

                pyautogui.write(de_local)
                pyautogui.press("enter")

                pyautogui.write(de_lugar)
                pyautogui.press("enter")

                pyautogui.write(lote_inicial)
                pyautogui.press("enter")
                pyautogui.press("enter")

                pyautogui.write(para_local)
                pyautogui.press("enter")

                pyautogui.write(para_lugar)
                pyautogui.press("enter")

                pyautogui.write(lote_destino)
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