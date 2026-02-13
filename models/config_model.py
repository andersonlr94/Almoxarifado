import os
import json

PASTA_CONFIG = os.path.join(
    os.path.expanduser("~"),
    "Documents",
    "Almoxarifado"
)

CONFIG_FILE = os.path.join(PASTA_CONFIG, "config_geral.json")


def obter_pasta_dados():
    if not os.path.exists(CONFIG_FILE):
        return ""
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("pasta_dados", "")
    except:
        return ""


def salvar_config(dados):
    if not os.path.exists(PASTA_CONFIG):
        os.makedirs(PASTA_CONFIG)

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
