import pyautogui
import time
from datetime import datetime
from models.digitar_ae_model import digitar_texto, enter, capslock_ativo  # Reaproveitando funções existentes

def get_mes_atual():
    """Retorna o mês atual por extenso"""
    meses = {
        1: "Janeiro",
        2: "Fevereiro",
        3: "Março",
        4: "Abril",
        5: "Maio",
        6: "Junho",
        7: "Julho",
        8: "Agosto",
        9: "Setembro",
        10: "Outubro",
        11: "Novembro",
        12: "Dezembro"
    }
    mes_num = datetime.now().month
    return meses[mes_num]

def executar_sequencia_qad(kardex, qtde):
    """
    Executa a sequência completa de transferência no QAD
    Reutiliza as funções do digitar_ae_model.py
    """

    
    try:
        # Salvar estado original do Caps Lock
        estado_caps_original = capslock_ativo()
        
        if estado_caps_original:
            pyautogui.press("capslock")
            time.sleep(0.1)
        
        # Pequena pausa inicial para o usuário posicionar o cursor
        time.sleep(2)
        
        # === SEQUÊNCIA QAD ===
        digitar_texto(kardex)  # resgata o valor do kardex do pedidos.json
        enter()

        digitar_texto(qtde)  # resgata o valor da qtde do pedidos.json
        enter()

        # 4 enters consecutivos
        enter(4)

        digitar_texto("transfi")
        enter(2)  # 2 enters

        digitar_texto("10912")
        enter()

        digitar_texto("ZCENTRAL")
        enter()

        # F2 + 4 enters
        pyautogui.press("f2")
        time.sleep(0.1)
        enter(4)

        digitar_texto("10912")
        enter()

        digitar_texto("ZMANUTE")
        enter()

        digitar_texto(f"ALEXANDRE-{get_mes_atual()}")
        enter(3)  # 3 enters
        
        # Restaurar estado original do Caps Lock se necessário
        if not estado_caps_original:
            pyautogui.press("capslock")
        
        return True, "Sequência executada com sucesso!"
        
    except Exception as e:
        return False, f"Erro ao executar sequência: {str(e)}"