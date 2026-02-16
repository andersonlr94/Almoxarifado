from datetime import datetime


def filtrar_dados(dados, filtro_status):
    lista = []

    for item in dados:
        status_item = str(item.get("status", ""))

        mostrar = False

        if filtro_status == "Entregue":
            mostrar = status_item.startswith("Entregue")
        elif status_item == filtro_status:
            mostrar = True

        if mostrar:
            lista.append(item)

    return lista


def atualizar_status_model(dados, pedidos_selecionados, novo_status):
    alterou = False
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

    for item in dados:
        for pedido, codigo in pedidos_selecionados:
            if str(item.get("pedido")) == str(pedido) and str(item.get("codigo")) == str(codigo):

                if novo_status == "Entregue":
                    item["status"] = f"Entregue em {data_hora}"
                else:
                    item["status"] = novo_status

                alterou = True

    return dados, alterou

def inserir_novo_pedido(dados, pedido_base, codigo, qtde, requisitante):
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

    novo_item = {
        "pedido": novo_pedido,
        "codigo": codigo,
        "qtde": qtde,
        "requisitante": requisitante,
        "status": "Pendente"
    }

    dados.append(novo_item)

    return dados
