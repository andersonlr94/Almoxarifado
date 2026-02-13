import os
import json
from models.config_model import obter_pasta_dados


def caminho_arquivo(nome):
    pasta = obter_pasta_dados()
    if not pasta:
        return None
    return os.path.join(pasta, nome)


def ler_dados():
    caminho = caminho_arquivo("pedidos.json")
    if not caminho or not os.path.exists(caminho):
        return []
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def salvar_no_arquivo(dados):
    caminho = caminho_arquivo("pedidos.json")
    if not caminho:
        return
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
