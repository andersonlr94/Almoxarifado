import os
import json
from models.config_model import obter_pasta_itens

def obter_pasta_itens_zero():
    """
    Cria a pasta 'itensZero' dentro da pasta configurada no sistema.
    Essa é a mesma base usada pelo itensAlmoxarifado.json
    """
    base = obter_pasta_itens()  # <- vindo do config_model
    if not base:
        raise RuntimeError("Pasta de itens não configurada no sistema.")

    pasta = os.path.join(base, "itensZero")
    os.makedirs(pasta, exist_ok=True)
    return pasta


def caminho_json():
    return os.path.join(obter_pasta_itens_zero(), "itensZero.json")



def caminho_json():
    return os.path.join(obter_pasta_itens_zero(), "itensZero.json")


def ler_itens_zero():
    caminho = caminho_json()
    if not os.path.exists(caminho):
        return []

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def salvar_itens_zero(dados):
    caminho = caminho_json()
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def merge_itens(dados_existentes, novos_itens):
    """
    Adiciona somente itens novos (Kardex + Código).
    """
    chaves = {(d["Kardex"], d["Código"]) for d in dados_existentes}

    for item in novos_itens:
        chave = (item["Kardex"], item["Código"])
        if chave not in chaves:
            chaves.add(chave)
            dados_existentes.append(item)

    return dados_existentes