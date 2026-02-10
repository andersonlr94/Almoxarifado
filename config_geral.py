import flet as ft
import json
import os

# ================== CAMINHO PADRÃO ==================
PASTA_CONFIG = os.path.join(
    os.path.expanduser("~"),
    "Documents",
    "Almoxarifado"
)

CONFIG_FILE = os.path.join(PASTA_CONFIG, "config_geral.json")


# ================== FUNÇÕES ==================
def garantir_pasta():
    if not os.path.exists(PASTA_CONFIG):
        os.makedirs(PASTA_CONFIG)


def carregar_config():
    garantir_pasta()

    if not os.path.exists(CONFIG_FILE):
        return {"pasta_dados": ""}

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"pasta_dados": ""}


def salvar_config(dados):
    garantir_pasta()

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


# ================== TELA ==================
def tela_config_geral(page: ft.Page):
    config = carregar_config()

    txt_pasta = ft.TextField(
        label="Caminho da pasta de Programação de Agulhas",
        hint_text=r"Ex: C:\Almoxarifado\Dados",
        value=config.get("pasta_dados", ""),
        expand=True
    )

    lbl_status = ft.Text("")

    def salvar(e):
        caminho = txt_pasta.value.strip()

        if not caminho:
            lbl_status.value = "Informe o caminho da pasta."
            lbl_status.color = "red"
            page.update()
            return

        if not os.path.isdir(caminho):
            lbl_status.value = "O caminho informado não existe."
            lbl_status.color = "red"
            page.update()
            return

        salvar_config({"pasta_dados": caminho})

        lbl_status.value = "Configuração salva com sucesso!"
        lbl_status.color = "green"
        page.update()

    return ft.Column(
        [
            ft.Text("Configuração Geral", size=26, weight="bold"),
            ft.Text(
                "Os arquivos pedidos.json e kardex_locação.json serão buscados nesta pasta:"
            ),
            txt_pasta,
            lbl_status,
            ft.ElevatedButton(
                "Salvar",
                icon=ft.Icons.SAVE,
                bgcolor="green",
                color="white",
                on_click=salvar
            )
        ],
        expand=True,
        spacing=15
    )
