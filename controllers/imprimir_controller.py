import flet as ft
from models.imprimir_model import imprimir_multiplas_etiquetas


def criar_controller(page, tabela, cb_impressora):
    """
    Cria o controller para o botão de imprimir.
    """

    state = {"printing": False}  # debounce contra cliques múltiplos

    def imprimir(e):
        # Debounce: evita reentrância (ex.: clique duplo)
        if state["printing"]:
            return
        state["printing"] = True

        try:
            print("\n" + "="*50)
            print("=== BOTÃO IMPRIMIR CLICADO ===")
            print("="*50)

            # Obter o destino selecionado
            destino = cb_impressora.value
            print(f"Destino selecionado: {destino!r}")

            # Coletar itens selecionados (deduplicado)
            itens_selecionados = []
            vistos = set()

            print(f"\nTotal de linhas na tabela: {len(tabela.rows)}")

            for idx, row in enumerate(tabela.rows):
                if not _get_checkbox_value_from_cell(row.cells[0]):
                    continue  # só processa marcadas

                # ---- Preferível: usar row.data se você setou ao montar a linha ----
                d = getattr(row, "data", None)
                if isinstance(d, dict) and d:
                    pedido       = str(d.get("pedido", ""))
                    kardex       = str(d.get("kardex", ""))
                    codigo       = str(d.get("codigo", ""))
                    quantidade   = str(d.get("qtde", ""))
                    fornecedor   = str(d.get("fornecedor", ""))
                    requisitante = str(d.get("requisitante", ""))
                    status       = str(d.get("status", ""))
                else:
                    # ---- Fallback: ler dos controles (com GestureDetector) ----
                    pedido       = _get_text_value_from_cell(row.cells[1])
                    kardex       = _get_text_value_from_cell(row.cells[2])
                    codigo       = _get_text_value_from_cell(row.cells[3])
                    quantidade   = _get_text_value_from_cell(row.cells[4])
                    fornecedor   = _get_text_value_from_cell(row.cells[5])
                    requisitante = _get_text_value_from_cell(row.cells[6])
                    status       = _get_text_value_from_cell(row.cells[7])

                print(f"[{idx}] Pedido='{pedido}' Kardex='{kardex}' Código='{codigo}' "
                      f"Qtde='{quantidade}' Fornecedor='{fornecedor}' Requisitante='{requisitante}' Status='{status}'")

                chave = (pedido, kardex, codigo, quantidade, requisitante, fornecedor)
                if chave not in vistos:
                    vistos.add(chave)
                    itens_selecionados.append(chave)

            if not itens_selecionados:
                print("\n❌ Nenhum item selecionado")
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Selecione pelo menos um item!"),
                    bgcolor="red"
                )
                page.snack_bar.open = True
                page.update()
                return

            print("\n>>> Itens únicos a imprimir:")
            for it in itens_selecionados:
                print("   ", it)
            print(">>> Total único:", len(itens_selecionados))

            # Mostrar mensagem de processamento
            acao = "Salvando" if destino == "Salvar como PDF" else "Imprimindo"
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"{acao} {len(itens_selecionados)} etiqueta(s)...\nBuscando localizações..."),
                bgcolor="blue"
            )
            page.snack_bar.open = True
            page.update()

            # Chamar a função de impressão com o destino selecionado
            print("\n🔄 Chamando imprimir_multiplas_etiquetas...")
            sucesso, mensagem = imprimir_multiplas_etiquetas(itens_selecionados, destino)

            print("\n📋 Resultado final:")
            print(f"  Sucesso: {sucesso}")
            print(f"  Mensagem: {mensagem}")

            page.snack_bar = ft.SnackBar(
                content=ft.Text(mensagem),
                bgcolor=("green" if sucesso else "red")
            )
            page.snack_bar.open = True
            page.update()
            print("="*50 + "\n")

        finally:
            state["printing"] = False  # libera para próximos cliques

    return imprimir



# ---- Helpers robustos (mesmos que você já vinha usando) ----------------------
def _get_checkbox_value_from_cell(cell) -> bool:
    if cell is None:
        return False
    ctrl = cell.content
    if isinstance(ctrl, ft.Checkbox):
        return bool(ctrl.value)
    if isinstance(ctrl, ft.GestureDetector):
        inner = ctrl.content
        if isinstance(inner, ft.Checkbox):
            return bool(inner.value)
    try:
        while hasattr(ctrl, "content") and ctrl.content is not getattr(ctrl, "content", None):
            ctrl = ctrl.content
            if isinstance(ctrl, ft.Checkbox):
                return bool(ctrl.value)
    except Exception:
        pass
    return False



def _get_text_value_from_cell(cell, default: str = "") -> str:
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

        if hasattr(ctrl, "controls") and isinstance(ctrl.controls, list) and ctrl.controls:
            # tenta achar Text direto
            for ch in ctrl.controls:
                if isinstance(ch, ft.Text):
                    return ch.value or default
                if hasattr(ch, "content") and isinstance(ch.content, ft.Text):
                    return ch.content.value or default
            # fallback: aprofunda no primeiro filho
            ctrl = ctrl.controls[0]
            continue

        break
    return default
