import flet as ft
import time
from models.digitar_qad_model import executar_sequencia_qad


def criar_controller(page, tabela, ler_dados):

    def transferir_qad(e):
        print("Botão Transferir QAD clicado")

        selecionados = []

        for row in tabela.rows:
            # 1) Checar checkbox (coluna 0) mesmo com GestureDetector
            if not _get_checkbox_value_from_cell(row.cells[0]):
                continue

            # 2) Preferível: ler de row.data (se você tiver colocado ao montar a linha)
            d = getattr(row, "data", None)
            if isinstance(d, dict) and d:
                kardex = str(d.get("kardex", ""))
                qtde   = str(d.get("qtde", ""))
            else:
                # Fallback: ler da UI, usando helper que desembrulha GestureDetector
                kardex = _get_text_value_from_cell(row.cells[2], "")
                qtde   = _get_text_value_from_cell(row.cells[4], "")

            if kardex:
                selecionados.append((kardex, qtde))
                print(f"Item selecionado: {kardex} - Qtde: {qtde}")

        if not selecionados:
            print("Nenhum item selecionado")
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Selecione pelo menos um pedido!"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        print(f"Iniciando transferência de {len(selecionados)} item(ns)")
        time.sleep(2)  # tempo pro usuário focar a tela do QAD

        sucesso_total = True

        for i, (kardex, qtde) in enumerate(selecionados, start=1):
            print(f"Processando item {i}: {kardex} - {qtde}")

            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Transferindo pedido {kardex}..."),
                bgcolor="blue"
            )
            page.snack_bar.open = True
            page.update()

            sucesso, mensagem = executar_sequencia_qad(kardex, qtde)
            print(f"Resultado: {sucesso} - {mensagem}")

            if not sucesso:
                sucesso_total = False
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Erro: {mensagem}"),
                    bgcolor="red"
                )
                page.snack_bar.open = True
                page.update()
                break
            else:
                time.sleep(1)  # pequena pausa entre itens

        if sucesso_total:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"{len(selecionados)} transferência(s) concluída(s)!"),
                bgcolor="green"
            )
            page.snack_bar.open = True
            page.update()

    return transferir_qad



def _get_checkbox_value_from_cell(cell) -> bool:
    """
    Retorna o valor booleano do checkbox na célula, mesmo que esteja embrulhado.
    Suporta:
      - DataCell(Checkbox(...))
      - DataCell(GestureDetector(content=Checkbox(...)))
      - Wrappers com .content encadeado
    """
    if cell is None:
        return False
    ctrl = cell.content

    # Caso direto: Checkbox
    if isinstance(ctrl, ft.Checkbox):
        return bool(ctrl.value)

    # GestureDetector contendo Checkbox
    if isinstance(ctrl, ft.GestureDetector):
        inner = ctrl.content
        if isinstance(inner, ft.Checkbox):
            return bool(inner.value)

    # Desembrulhar encadeado por .content
    try:
        while hasattr(ctrl, "content") and ctrl.content is not getattr(ctrl, "content", None):
            ctrl = ctrl.content
            if isinstance(ctrl, ft.Checkbox):
                return bool(ctrl.value)
    except Exception:
        pass

    return False


def _get_text_value_from_cell(cell, default: str = "") -> str:
    """
    Retorna o texto da célula, mesmo que esteja embrulhada em GestureDetector, Container, Row, etc.
    Suporta ft.Text, ft.TextField e tenta varrer children em Row/Column.
    """
    if cell is None:
        return default

    ctrl = cell.content
    visited = set()

    while True:
        if id(ctrl) in visited:
            break
        visited.add(id(ctrl))

        if isinstance(ctrl, ft.Text):
            return ctrl.value or default
        if isinstance(ctrl, ft.TextField):
            return ctrl.value or default

        if hasattr(ctrl, "value") and not isinstance(ctrl, ft.Checkbox):
            val = getattr(ctrl, "value", None)
            if val is not None:
                return str(val)

        if hasattr(ctrl, "content") and ctrl.content is not None:
            ctrl = ctrl.content
            continue

        if hasattr(ctrl, "controls") and isinstance(ctrl.controls, list):
            # tenta achar Text direto
            for ch in ctrl.controls:
                if isinstance(ch, ft.Text):
                    return ch.value or default
