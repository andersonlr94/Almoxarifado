import os
import json
from datetime import datetime
from models.config_model import obter_pasta_itens

def filtrar_dados(dados, filtro_status):
    lista = []

    for item in dados:
        status_item = str(item.get("status", ""))

        mostrar = False

        if filtro_status == "Entregue":
            mostrar = status_item.startswith("Entregue")
        elif filtro_status == "Programado":
            mostrar = status_item.startswith("Programado")
        elif status_item == filtro_status:
            mostrar = True

        if mostrar:
            lista.append(item)

    return lista

def buscar_dados_estoque_por_kardex(kardex):
    """
    Busca Loc Novo, Loc Retorno e Consumo Médio
    no arquivo itensAlmoxarifado.json
    """
    pasta = obter_pasta_itens()
    if not pasta:
        return None

    caminho = os.path.join(pasta, "itensAlmoxarifado.json")
    if not os.path.exists(caminho):
        return None

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except Exception:
        return None

    for item in dados:
        if str(item.get("Kardex", "")).strip().upper() == str(kardex).strip().upper():
            return {
                "loc_novo": item.get("Loc novo", "-"),
                "loc_retorno": item.get("Loc retorno", "-"),
                "consumo_medio": item.get("Cons Medio", "-"),
            }

    return None

def atualizar_status_model(dados, pedidos_selecionados, novo_status):
    alterou = False
    data_completa = datetime.now().strftime("%d/%m/%Y")

    for item in dados:
        pedido_item = str(item.get("pedido", "")).strip()
        codigo_item = str(item.get("codigo", "")).strip().upper()

        for pedido, codigo in pedidos_selecionados:
            pedido_sel = str(pedido).strip()
            codigo_sel = str(codigo).strip().upper()

            if pedido_item == pedido_sel and codigo_item == codigo_sel:
                # Atualizar o status SEM a data
                if novo_status == "Entregue":
                    item["status"] = "Entregue"  # Apenas o texto, sem data
                    item["data_entregue"] = data_completa
                elif novo_status == "Programado":
                    item["status"] = "Programado"  # Apenas o texto, sem data
                    item["data_programado"] = data_completa
                elif novo_status == "Separando":
                    item["status"] = "Separando"  # Apenas o texto, sem data
                    item["data_separando"] = data_completa

                alterou = True

    return dados, alterou

def buscar_fornecedor_por_codigo(codigo):
    """
    Busca o fornecedor de um item no arquivo itensAlmoxarifado.json
    usando o código fornecido.
    """
    pasta_itens = obter_pasta_itens()
    
    if not pasta_itens:
        return None
    
    arquivo_itens = os.path.join(pasta_itens, "itensAlmoxarifado.json")
    
    if not os.path.exists(arquivo_itens):
        return None
    
    codigo_norm = codigo.strip().upper()
    
    try:
        with open(arquivo_itens, "r", encoding="utf-8") as f:
            itens = json.load(f)
        
        # Procura o item pelo código
        for item in itens:
            if str(item.get("Código", "")) == str(codigo):
                return item.get("Fornecedor", "")
        
        return None
    except Exception as e:
        print(f"Erro ao ler itensAlmoxarifado.json: {e}")
        return None
  

def buscar_kardex_por_codigo(codigo):
    """
    Busca o kardex de um item no arquivo itensAlmoxarifado.json
    usando o código fornecido.
    """
    pasta_itens = obter_pasta_itens()
    
    if not pasta_itens:
        return None
    
    arquivo_itens = os.path.join(pasta_itens, "itensAlmoxarifado.json")
    
    if not os.path.exists(arquivo_itens):
        return None
    
    codigo_norm = codigo.strip().upper()

    try:
        with open(arquivo_itens, "r", encoding="utf-8") as f:
            itens = json.load(f)
        
        # Procura o item pelo código
        for item in itens:
            if str(item.get("Código", "")) == str(codigo):
                return item.get("Kardex", "")
        
        return None
    except Exception as e:
        print(f"Erro ao ler itensAlmoxarifado.json: {e}")
        return None

def buscar_qtdes_estoque_por_kardex(kardex):
    """
    Busca Quantidades no itensAlmoxarifado.json para uso em tela
    (Loc Novo, Loc Retorno e Consumo Médio)

    NÃO interfere na função usada para etiquetas.
    """
    pasta = obter_pasta_itens()
    if not pasta:
        return None

    caminho = os.path.join(pasta, "itensAlmoxarifado.json")
    if not os.path.exists(caminho):
        return None

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except Exception:
        return None

    kardex_proc = str(kardex).strip().upper()

    for item in dados:
        kardex_json = str(item.get("Kardex", "")).strip().upper()
        if kardex_json == kardex_proc:
            # Formatar consumo médio com 2 casas decimais
            consumo = item.get("Consumo médio", "-")

            if consumo not in ("-", None, ""):
                try:
                    # normaliza formato brasileiro → internacional
                    consumo_str = str(consumo).replace(",", ".")
                    consumo_float = float(consumo_str)
                    consumo_formatado = f"{consumo_float:.2f}".replace(".", ",")
                except (ValueError, TypeError):
                    consumo_formatado = "-"
            else:
                consumo_formatado = "-"
            
            return {
                "qtde_novo": item.get("Qtde novo", "-"),
                "qtde_retorno": item.get("Qtde retorno", "-"),
                "consumo_medio": consumo_formatado,
            }

    return None

def inserir_novo_pedido(dados, pedido_base, kardex, codigo, qtde, requisitante, fornecedor):
    """
    Insere novo pedido gerando sufixo automático -01, -02...
    """
    # Filtrar pedidos com mesma base
    pedidos_mesma_base = [
        item for item in dados
        if str(item.get("pedido", "")).startswith(pedido_base + "-")
    ]

    numeros = []

    for item in pedidos_mesma_base:
        try:
            sufixo = item["pedido"].split("-")[-1]
            numeros.append(int(sufixo))
        except:
            pass

    if numeros:
        proximo = max(numeros) + 1
    else:
        proximo = 1

    novo_pedido = f"{pedido_base}-{str(proximo).zfill(2)}"
    data_atual = datetime.now().strftime("%d/%m/%Y")
    data_simples = datetime.now().strftime("%d/%m/%Y")

    novo_item = {
        "pedido": novo_pedido,
        "codigo": codigo,          
        "kardex": kardex,         
        "qtde": qtde,
        "fornecedor": fornecedor,
        "requisitante": requisitante,
        "status": "Pendente",
        "data_inserido": data_atual,
        "data_programado": "",
        "data_separando": "",
        "data_entregue": ""
    }

    dados.append(novo_item)

    return dados