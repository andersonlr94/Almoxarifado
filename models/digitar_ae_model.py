import pyautogui
import time
import ctypes

pyautogui.FAILSAFE = True


def digitar_texto(texto):
    pyautogui.write(str(texto), interval=0.02)


def enter(vezes=1):
    for _ in range(vezes):
        pyautogui.press("enter")
        time.sleep(0.05)


def capslock_ativo():
    state = (ctypes.c_ubyte * 256)()
    ctypes.windll.user32.GetKeyboardState(state)
    return state[0x14] & 1


def executar_automacao(linhas, conta, subconta, cc):

    if not linhas:
        return False, "Tabela vazia"

    estado_caps_original = capslock_ativo()

    if estado_caps_original:
        pyautogui.press("capslock")
        time.sleep(0.1)

    time.sleep(5)

    for row in linhas:

        digitar_texto(row[1])
        enter(3)

        digitar_texto(row[7])
        enter(3)

        digitar_texto(row[2])
        enter(2)

        digitar_texto(row[3])
        enter()

        digitar_texto("PC")
        enter()

        digitar_texto(row[5])
        enter(3)

        digitar_texto(row[6])
        enter()

        digitar_texto("0")
        enter()

        digitar_texto(row[8])
        enter(3)

        digitar_texto(conta)
        enter()

        digitar_texto(subconta)
        enter()

        digitar_texto(cc)
        enter(9)

        digitar_texto("01.999.00")
        enter(3)

    if not estado_caps_original:
        pyautogui.press("capslock")

    return True, "Execução concluída"
