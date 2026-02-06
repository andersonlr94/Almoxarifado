import flet as ft
import pyautogui
import time
import ctypes

pyautogui.FAILSAFE = True


def tela_digitar_ae(page: ft.Page):
    page.title = "Digitar AE"
    page.window_always_on_top = False
    page.window_resizable = True

    # ---------------- TABELA ----------------
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Gerar")),
            ft.DataColumn(ft.Text("Item")),
            ft.DataColumn(ft.Text("Descrição")),
            ft.DataColumn(ft.Text("Qtde")),
            ft.DataColumn(ft.Text("UM")),
            ft.DataColumn(ft.Text("Custo")),
            ft.DataColumn(ft.Text("Classificação fiscal")),
            ft.DataColumn(ft.Text("Classe de imposto")),
            ft.DataColumn(ft.Text("C-M")),
        ],
        rows=[],
        data_row_min_height=32,
        data_row_max_height=32,
        heading_row_height=36,
    )

    # ---------------- CLIPBOARD ----------------
    async def colar_do_clipboard(e):
        texto = (await page.clipboard.get() or "").upper()

        if not texto:
            page.snack_bar = ft.SnackBar(ft.Text("Área de transferência vazia"))
            page.snack_bar.open = True
            page.update()
            return

        linhas = texto.strip().splitlines()

        for linha in linhas:
            colunas = linha.split("\t")
            while len(colunas) < 9:
                colunas.append("")

            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(colunas[0], size=12)),
                        ft.DataCell(ft.Text(colunas[1], size=12)),
                        ft.DataCell(ft.Text(colunas[2], size=12)),
                        ft.DataCell(ft.Text(colunas[3], size=12)),
                        ft.DataCell(ft.Text(colunas[4], size=12)),
                        ft.DataCell(ft.Text(colunas[5], size=12)),
                        ft.DataCell(ft.Text(colunas[6], size=12)),
                        ft.DataCell(ft.Text(colunas[7], size=12)),
                        ft.DataCell(ft.Text(colunas[8], size=12)),
                    ]
                )
            )

        page.update()

    # ---------------- CAMPOS ----------------
    txt_conta = ft.TextField(label="Conta", width=200)
    txt_subconta = ft.TextField(label="SubConta", width=200)
    txt_cc = ft.TextField(label="CC", width=200)

     # ---------------- PYAUTOGUI ----------------
    def digitar_texto(texto):
        pyautogui.write(str(texto), interval=0.02)

    def enter(vezes=1):
        for _ in range(vezes):
            pyautogui.press("enter")
            time.sleep(0.05)

    def digitar_coluna(row, col):
        valor = tabela.rows[row].cells[col].content.value
        digitar_texto(valor)

    def capslock_ativo():
        state = (ctypes.c_ubyte * 256)()
        ctypes.windll.user32.GetKeyboardState(state)
        return state[0x14] & 1


    # ---------------- EXECUTAR ----------------
    def executar(e):
        conta = txt_conta.value or ""
        subConta = txt_subconta.value or ""
        cc = txt_cc.value or ""

        if not tabela.rows:
            page.snack_bar = ft.SnackBar(ft.Text("Tabela vazia"))
            page.snack_bar.open = True
            page.update()
            return
        
        # ---------- CAPS LOCK ----------
        estado_caps_original = capslock_ativo()

        if estado_caps_original:
            pyautogui.press("capslock")
            time.sleep(0.1)

        page.snack_bar = ft.SnackBar(
            ft.Text("Você tem 5 segundos para focar o sistema destino")
        )
        page.snack_bar.open = True
        page.update()

        time.sleep(5)

        for row in range(len(tabela.rows)):

            digitar_coluna(row, 1)
            enter(3)

            digitar_coluna(row, 7)
            enter(3)

            digitar_coluna(row, 2)
            enter(2)

            digitar_coluna(row, 3)
            enter()

            digitar_texto("PC")
            enter()

            digitar_coluna(row, 5)
            enter(3)

            digitar_coluna(row, 6)
            enter()

            digitar_texto("0")
            enter()

            digitar_coluna(row, 8)
            enter(3)

            digitar_texto(conta)
            enter()

            digitar_texto(subConta)
            enter()

            digitar_texto(cc)
            enter(9)

            digitar_texto("01.999.00")
            enter(3)

        # ---------- RESTAURA CAPS ----------
        if not estado_caps_original:
            pyautogui.press("capslock")


     # ---------------- LIMPAR ----------------
    def limpar_tabela(e):
        tabela.rows.clear()
        page.update()

    # ---------------- BOTÕES ----------------
    btn_colar = ft.ElevatedButton(
        "Colar da JTable", bgcolor="blue", color="white", on_click=colar_do_clipboard
    )

    btn_executar = ft.ElevatedButton(
        "Executar", bgcolor="green", color="white", on_click=executar
    )

    btn_limpar = ft.ElevatedButton(
        "Limpar tabela", bgcolor="red", color="white", on_click=limpar_tabela
    )

    # ---------------- Layout ----------------
    return ft.Column(
        [
            ft.Row([txt_conta, txt_subconta, txt_cc]),
            ft.Divider(),
            ft.Row([btn_colar, btn_executar, btn_limpar]),
            ft.Divider(),
            ft.ListView([tabela], expand=True),
        ],
        expand=True,
    )
