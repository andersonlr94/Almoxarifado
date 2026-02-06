import flet as ft
from datetime import datetime
import json
import os
import subprocess
import sys
from digitar_ae import tela_digitar_ae



def main(page: ft.Page):
    page.title = "Controle de Almoxarifado"
    page.window_width = 1100
    page.window_height = 700
    
    DATA_FILE = "pedidos.json"


    def abrir_digitar_ae(e):
        return ft.Column(
        [
            ft.Text("Digitar AE", size=24, weight="bold"),
            # TODO: coloque aqui TODO o conteúdo da outra tela
        ],
        expand=True
    )


    # ---------- 1. VARIÁVEIS DE ESTADO (Devem vir primeiro) ----------
    conteudo = ft.Container(expand=True)

    # ---------- 2. FUNÇÕES DE DADOS ----------
    def ler_dados():
        if not os.path.exists(DATA_FILE):
            return []
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def salvar_no_arquivo(dados):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    # ---------- 3. COMPONENTES DA TABELA E BOTÕES DE AÇÃO ----------
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Sel")),
            ft.DataColumn(ft.Text("Pedido")),
            ft.DataColumn(ft.Text("Kardex")),
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Descrição")),
            ft.DataColumn(ft.Text("Qtde")),
            ft.DataColumn(ft.Text("Status")),
        ],
        rows=[]
    )

    # Botões inferiores (Iniciam invisíveis)
    btn_programar = ft.ElevatedButton(
        "Mudar p/ Programado", bgcolor="blue", color="white", visible=False,
        on_click=lambda _: atualizar_status("Programado")
    )
    btn_separar = ft.ElevatedButton(
        "Mudar p/ Separando", bgcolor="orange", color="white", visible=False,
        on_click=lambda _: atualizar_status("Separando")
    )
    btn_entregar = ft.ElevatedButton(
        "Mudar p/ Entregue", bgcolor="green", color="white", visible=False,
        on_click=lambda _: atualizar_status("Entregue")
    )

    # ---------- 4. LÓGICA DE CARREGAMENTO E FILTRO ----------
    def carregar_tabela(filtro_status="Pendente"):
        dados = ler_dados()
        tabela.rows.clear()
        
        # Controle de visibilidade dos botões conforme sua solicitação
        btn_programar.visible = (filtro_status == "Pendente")
        btn_separar.visible = (filtro_status == "Programado")
        btn_entregar.visible = (filtro_status == "Separando")
        
        for item in dados:
            status_item = str(item.get("status", ""))
            mostrar = False
            
            if filtro_status == "Entregue":
                if status_item.startswith("Entregue"): mostrar = True
            elif status_item == filtro_status:
                mostrar = True
            
            if mostrar:
                tabela.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Checkbox(value=False)),
                            ft.DataCell(ft.Text(item.get("pedido", ""))),
                            ft.DataCell(ft.Text(item.get("kardex", ""))),
                            ft.DataCell(ft.Text(item.get("codigo", ""))),
                            ft.DataCell(ft.Text(item.get("descricao", ""))),
                            ft.DataCell(ft.Text(item.get("qtde", ""))),
                            ft.DataCell(ft.Text(status_item)),
                        ]
                    )
                )
        page.update()

    def atualizar_status(novo_status):
        dados_completos = ler_dados()
        alterou = False
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
        origem = ""

        for row in tabela.rows:
            if row.cells[0].content.value == True:
                p_id = row.cells[1].content.value
                c_id = row.cells[3].content.value
                
                for item in dados_completos:
                    if str(item["pedido"]) == str(p_id) and str(item["codigo"]) == str(c_id):
                        if novo_status == "Entregue":
                            item["status"] = f"Entregue em {data_hora}"
                            origem = "Separando"
                        else:
                            item["status"] = novo_status
                            origem = "Pendente" if novo_status == "Programado" else "Programado"
                        alterou = True
        
        if alterou:
            salvar_no_arquivo(dados_completos)
            carregar_tabela(origem)
            page.snack_bar = ft.SnackBar(ft.Text(f"Item movido para {novo_status}"))
            page.snack_bar.open = True
            page.update()

    # ---------- 5. TELAS ----------
    def tela_manutencao():
        return ft.Column([
            ft.Row([
                ft.ElevatedButton("Pendentes", bgcolor="blue", color="white", on_click=lambda _: carregar_tabela("Pendente")),
                ft.ElevatedButton("Programados", bgcolor="yellow", color="white", on_click=lambda _: carregar_tabela("Programado")),
                ft.ElevatedButton("Separando", bgcolor="orange", color="white", on_click=lambda _: carregar_tabela("Separando")),
                ft.ElevatedButton("Entregues", bgcolor="green", color="white",on_click=lambda _: carregar_tabela("Entregue")),
            ], scroll=ft.ScrollMode.ADAPTIVE),
            ft.Divider(),
            ft.ListView([tabela], expand=True),
            ft.Divider(),
            ft.Row([btn_programar, btn_separar, btn_entregar], alignment="center")
        ], expand=True)

    def mudar_tela(destino):
        if destino == "home":
            conteudo.content = tela_home()
        elif destino == "manutencao":
            conteudo.content = tela_manutencao()
        elif destino == "digitar_ae":
            conteudo.content = tela_digitar_ae(page)


        page.update()

    # ---------- 6. ESTRUTURA PRINCIPAL ----------
    menu = ft.Row([
        # Usando strings para ícones para evitar AttributeError
        ft.TextButton("Início", icon="home", on_click=lambda _: mudar_tela("home")),
        ft.TextButton("Manutenção", icon="settings", on_click=lambda _: mudar_tela("manutencao")),
        ft.TextButton("Digitar AE", icon="edit", on_click=lambda _: mudar_tela("digitar_ae")
)
    ])

    # Conteúdo Inicial
    conteudo.content = ft.Column([
        ft.Text("Bem-vindo ao Almoxarifado", size=30, weight="bold")
    ], alignment="center", horizontal_alignment="center")

    page.add(
        ft.Column([
            menu,
            ft.Divider(),
            conteudo
        ], expand=True)
    )

ft.app(target=main)