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
