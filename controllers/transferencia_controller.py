# controllers/transferencia_controller.py
import flet as ft
from models.transferencia_model import (
    carregar_transferencias,
    filtrar_transferencias,
)

def criar_controller(page: ft.Page, tabela: ft.DataTable,
                     tf_documento: ft.TextField, tf_kardex: ft.TextField,
                     tf_depo_de: ft.TextField, tf_depo_para: ft.TextField):

    def _popular_tabela(registros: list[dict]):
        tabela.rows.clear()
        for r in registros:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Checkbox(value=False)),
                    ft.DataCell(ft.Text(r.get("documento", ""))),
                    ft.DataCell(ft.Text(r.get("kardex", ""))),
                    ft.DataCell(ft.Text(str(r.get("qtde", "")))),
                    ft.DataCell(ft.Text(r.get("de_deposito", ""))),
                    ft.DataCell(ft.Text(r.get("para_deposito", ""))),
                    ft.DataCell(ft.Text(r.get("data", ""))),
                ]
            )
            # Guarda os dados originais da linha
            row.data = r
            tabela.rows.append(row)
        page.update()

    def carregar(e=None):
        regs = carregar_transferencias()
        filtrados = filtrar_transferencias(
            regs,
            doc=tf_documento.value,
            kardex=tf_kardex.value,
            de=tf_depo_de.value,
            para=tf_depo_para.value,
        )
        _popular_tabela(filtrados)

    def limpar(e=None):
        for tf in (tf_documento, tf_kardex, tf_depo_de, tf_depo_para):
            tf.value = ""
        tabela.rows.clear()
        page.update()

    return carregar, limpar