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

def ler_itens_zero():
    caminho = caminho_json()
    if not os.path.exists(caminho):
        return []

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
            if isinstance(dados, list):
                return dados
            return []
    except Exception:
        return []


def salvar_itens_zero(dados):
    caminho = caminho_json()
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def sync_itens(dados_existentes, novos_itens):
    """
    Sincroniza itens vindos da JTable:
    - Mantém apenas itens presentes na nova cópia
    - Insere novos itens
    - Remove itens que não vieram na nova cópia
    - PRESERVA os campos locais: DPP e Observação
    """

    # Index dos itens existentes por chave
    index_existentes = {
        (item["Kardex"], item["Código"]): item
        for item in dados_existentes
    }

    dados_sincronizados = []

    for novo in novos_itens:
        chave = (novo["Kardex"], novo["Código"])

        if chave in index_existentes:
            # Item já existia → preservar campos locais
            antigo = index_existentes[chave]

            novo_item = {
                **novo,
                "DPP": antigo.get("DPP", ""),
                "Observação": antigo.get("Observação", ""),
            }
        else:
            # Item novo
            novo_item = {
                **novo,
                "DPP": "",
                "Observação": "",
            }

        dados_sincronizados.append(novo_item)

    return dados_sincronizados

def atualizar_dpp(kardex, codigo, dpp):
    dados = ler_itens_zero()
    alterou = False

    for item in dados:
        if (
            item.get("Kardex") == kardex
            and item.get("Código") == codigo
        ):
            item["DPP"] = dpp
            alterou = True
            break

    if alterou:
        salvar_itens_zero(dados)

    return alterou


    return dados_existentes