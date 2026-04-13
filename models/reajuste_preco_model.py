import os
import json
from datetime import datetime
from models.config_model import obter_pasta_itens

def obter_pasta_reajuste():
    """
    Cria a pasta 'reajustePreco' dentro da pasta configurada no sistema.
    """
    base = obter_pasta_itens()
    if not base:
        raise RuntimeError("Pasta de itens não configurada no sistema.")
    
    pasta = os.path.join(base, "reajustePreco")
    os.makedirs(pasta, exist_ok=True)
    return pasta

def caminho_json():
    """Retorna o caminho completo do arquivo reajustePreco.json"""
    return os.path.join(obter_pasta_reajuste(), "reajustePreco.json")

def ler_reajustes():
    """Carrega os reajustes do arquivo JSON"""
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

def salvar_reajustes(dados):
    """Salva os reajustes no arquivo JSON"""
    caminho = caminho_json()
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

def adicionar_reajuste(fornecedor, kardex, item, descricao, preco_antigo):
    """Adiciona um novo reajuste com a data atual"""
    dados = ler_reajustes()
    
    novo_reajuste = {
        "Fornecedor": fornecedor,
        "Kardex": kardex,
        "Item": item,
        "Descrição": descricao,
        "Preço antigo": preco_antigo,
        "Data pedido reajuste": datetime.now().strftime("%d/%m/%Y"),
        "Status": "Pendente",
        "Observação": ""
    }
    
    dados.append(novo_reajuste)
    salvar_reajustes(dados)
    return novo_reajuste

def excluir_reajuste(indice):
    """Exclui um reajuste pelo índice"""
    dados = ler_reajustes()
    if 0 <= indice < len(dados):
        removido = dados.pop(indice)
        salvar_reajustes(dados)
        return True, removido
    return False, None

def atualizar_campo(indice, campo, valor):
    """Atualiza um campo específico (Status ou Observação) de um reajuste"""
    dados = ler_reajustes()
    if 0 <= indice < len(dados):
        dados[indice][campo] = valor
        salvar_reajustes(dados)
        return True
    return False