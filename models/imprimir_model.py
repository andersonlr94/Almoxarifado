import os
import json  # IMPORTANTE: Adicionar esta importação
import subprocess
import platform
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from datetime import datetime
from models.config_model import obter_pasta_itens  # IMPORTANTE: Importar a função

# === ZPL helpers ===
def mm_to_dots(mm: float) -> int:
    # ZD220 203 dpi ≈ 8 dots/mm
    return int(round(mm * 8))

def gerar_zpl_etiqueta(pedido, kardex, codigo, quantidade, requisitante, fornecedor, localizacao):
    width = mm_to_dots(100)   # 100 mm = 800 dots
    height = mm_to_dots(40)   # 40 mm  = 320 dots

    loc_display = (localizacao or "N/I").strip()[:12]

    zpl = [
        "^XA",
        # Se precisar virar 180°, troque ^PON por ^POI:
        "^PON",                      # orientação normal (use ^POI se sair invertido)
        f"^PW{width}",
        f"^LL{height}",
        "^LH0,0",

        # Moldura
        f"^FO{mm_to_dots(2)},{mm_to_dots(2)}^GB{width - mm_to_dots(4)},{height - mm_to_dots(4)},2^FS",

        # CÓDIGO (Grande)
        f"^FO{mm_to_dots(5)},{mm_to_dots(5)}^A0N,40,40^FD{codigo}^FS",

        # KARDEX
        f"^FO{mm_to_dots(5)},{mm_to_dots(12)}^A0N,30,30^FD{kardex}^FS",

        # Pedido e Requisitante (lado a lado)
        f"^FO{mm_to_dots(5)},{mm_to_dots(20)}^A0N,25,25^FDPed: {pedido}^FS",
        f"^FO{mm_to_dots(50)},{mm_to_dots(20)}^A0N,25,25^FDReq: {requisitante}^FS",

        # Quantidade e Localização (lado a lado)
        f"^FO{mm_to_dots(5)},{mm_to_dots(30)}^A0N,30,30^FDQtde: {quantidade}^FS",
        f"^FO{mm_to_dots(50)},{mm_to_dots(30)}^A0N,30,30^FDLOC: {loc_display}^FS",

        "^PQ1",
        "^XZ"
    ]
    # CRLF no final garante término do job
    return "\n".join(zpl) + "\r\n"

def imprimir_zpl_via_spooler(nome_impressora: str, zpl: str):
    """
    Envia ZPL como RAW para a impressora no Windows (win32print).
    """
    try:
        import win32print
        hPrinter = win32print.OpenPrinter(nome_impressora)
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Etiqueta ZPL", None, "RAW"))
            try:
                win32print.StartPagePrinter(hPrinter)

                # 👇 Ajuste CRÍTICO: ASCII + CRLF
                payload = (zpl if zpl.endswith("\r\n") else zpl + "\r\n").encode("ascii", errors="ignore")
                win32print.WritePrinter(hPrinter, payload)

                win32print.EndPagePrinter(hPrinter)
            finally:
                win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)
    except Exception as e:
        raise RuntimeError(f"Falha no spooler Windows: {e}")

def listar_impressoras():
    """
    Lista as impressoras disponíveis no sistema usando win32print (mais confiável)
    """
    try:
        import win32print
        impressoras = []
        
        # Obtém todas as impressoras instaladas
        impressoras_raw = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
        
        for printer in impressoras_raw:
            # printer[2] contém o nome da impressora
            nome = printer[2]
            if nome and nome.strip():
                impressoras.append(nome.strip())
        
        print(f"Impressoras encontradas via win32print: {impressoras}")
        return impressoras
        
    except ImportError:
        print("win32print não instalado. Usando método alternativo...")
        # Fallback para o método antigo
        try:
            import subprocess
            import platform
            
            sistema = platform.system()
            
            if sistema == "Windows":
                resultado = subprocess.run(
                    ['wmic', 'printer', 'get', 'name'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                
                linhas = resultado.stdout.strip().split('\n')[1:]
                impressoras = []
                for linha in linhas:
                    nome = linha.strip()
                    if nome and not nome.startswith('Name'):
                        impressoras.append(nome)
                
                return impressoras
        except:
            pass
            
        return []
    except Exception as e:
        print(f"Erro ao listar impressoras: {e}")
        return []
    
def buscar_localizacao_por_codigo(codigo):
    """
    Busca a localização de um item no arquivo ItensAlmoxarifado.json
    usando o código fornecido.
    
    Args:
        codigo: Código do item a ser buscado
        
    Returns:
        str: Localização do item ou "N/I" se não encontrado
    """
    try:
        print(f"\n=== BUSCANDO LOCALIZAÇÃO PARA CÓDIGO: {codigo} ===")
        
        pasta_itens = obter_pasta_itens()
        print(f"Pasta de itens configurada: {pasta_itens}")
        
        if not pasta_itens:
            print("❌ Pasta de itens não configurada")
            return "N/I"
        
        arquivo_itens = os.path.join(pasta_itens, "itensAlmoxarifado.json")
        print(f"Caminho completo do arquivo: {arquivo_itens}")
        
        if not os.path.exists(arquivo_itens):
            print(f"❌ Arquivo não encontrado: {arquivo_itens}")
            return "N/I"
        
        print(f"✅ Arquivo encontrado! Tamanho: {os.path.getsize(arquivo_itens)} bytes")
        
        with open(arquivo_itens, "r", encoding="utf-8") as f:
            itens = json.load(f)
        
        print(f"✅ Arquivo JSON carregado! Total de itens: {len(itens)}")
        
        # Mostrar os primeiros itens para debug
        print("\nPrimeiros 3 itens do arquivo:")
        for i, item in enumerate(itens[:3]):
            print(f"  Item {i+1}: código='{item.get('codigo')}', locNovo='{item.get('locNovo')}'")
        
        # Procura o item pelo código
        codigo_str = str(codigo).strip()
        print(f"\nProcurando por código exato: '{codigo_str}'")
        
        for i, item in enumerate(itens):
            item_codigo = str(item.get("codigo", "")).strip()
            if item_codigo == codigo_str:
                print(f"✅ Código encontrado no índice {i}!")
                
                # AGORA USA locNovo EM VEZ DE localizacao
                localizacao = item.get("locNovo", "N/I")
                
                # Tratar valores especiais
                if localizacao in [None, "None", "nan", "NaN", ""]:
                    print("⚠️ Localização está vazia ou é inválida")
                    localizacao = "N/I"
                
                print(f"   Localização encontrada (locNovo): '{localizacao}'")
                return localizacao
        
        print(f"❌ Código '{codigo_str}' não encontrado no arquivo")
        return "N/I"
        
    except Exception as e:
        print(f"❌ Erro ao buscar localização: {e}")
        import traceback
        traceback.print_exc()
        return "N/I"

def imprimir_multiplas_etiquetas(itens_selecionados, destino=None):
    """
    Agora: se destino for uma Zebra (ex.: nome contém 'ZDesigner'),
    gerar ZPL e enviar via spooler Windows (ou TCP).
    """
    try:
        if not itens_selecionados:
            return False, "Nenhum item selecionado para impressão"
        
        arquivos_gerados = []
        itens_nao_encontrados = []
        mensagens = []
        sucesso_impressao = True

        # Heurística simples: nome Zebra contém "ZDesigner" / "Zebra"
        nome_destino = (destino or "").strip()
        is_zebra = any(s in nome_destino for s in ["ZDesigner", "Zebra"])

        # Se for salvar apenas, não imprimir
        somente_salvar_pdf = (destino == "Salvar como PDF")

        for i, item in enumerate(itens_selecionados, 1):
            # Desempacotar
            if len(item) == 6:
                pedido, kardex, codigo, quantidade, requisitante, fornecedor = item
            else:
                pedido, kardex, codigo, quantidade, requisitante = item
                fornecedor = "N/I"

            # Localização via JSON
            localizacao = buscar_localizacao_por_codigo(codigo)
            if localizacao == "N/I":
                itens_nao_encontrados.append(codigo)

            if is_zebra and not somente_salvar_pdf:
                # --- Impressão ZPL direta ---
                try:
                    zpl = gerar_zpl_etiqueta(pedido, kardex, codigo, quantidade, requisitante, fornecedor, localizacao)

                    # Escolha MECANISMO: 1) Spooler Windows
                    imprimir_zpl_via_spooler(nome_destino, zpl)

                    # OU 2) TCP/IP se a Zebra estiver na rede:
                    # imprimir_zpl_via_tcp("192.168.0.123", zpl)

                    mensagens.append(f"✅ {codigo}: impresso em {nome_destino} (ZPL)")
                except Exception as e:
                    sucesso_impressao = False
                    mensagens.append(f"❌ {codigo}: erro ao enviar ZPL -> {e}")

            else:
                # --- Fluxo PDF (salvar/ outras impressoras) ---
                ok, resultado = gerar_etiqueta_pdf(
                    pedido, kardex, codigo, quantidade, requisitante, fornecedor, localizacao
                )
                if ok:
                    arquivos_gerados.append(resultado)
                else:
                    return False, f"Erro ao gerar etiqueta {pedido}: {resultado}"

        # Aviso de itens sem localização
        if itens_nao_encontrados:
            msg_aviso = f"\n⚠️ Itens sem localização: {', '.join(itens_nao_encontrados[:5])}"
            if len(itens_nao_encontrados) > 5:
                msg_aviso += f" e mais {len(itens_nao_encontrados) - 5}"
        else:
            msg_aviso = ""

        # Se foi Zebra ZPL, já finalizamos
        if is_zebra and not somente_salvar_pdf:
            if sucesso_impressao:
                return True, ("Todas etiquetas ZPL enviadas com sucesso!" + msg_aviso + ("\n" + "\n".join(mensagens) if mensagens else ""))
            else:
                return False, ("Algumas etiquetas falharam no ZPL:" + msg_aviso + ("\n" + "\n".join(mensagens) if mensagens else ""))

        # Salvar apenas PDF
        if somente_salvar_pdf and arquivos_gerados:
            pasta = os.path.dirname(arquivos_gerados[0])
            return True, f"{len(arquivos_gerados)} etiqueta(s) salva(s) em PDF na pasta: {pasta}{msg_aviso}"

        # Se não Zebra, você poderia imprimir PDF aqui (Sumatra), caso deseje.
        # Como sua preferência é ZPL, deixei apenas salvar/imprimir Zebra.
        if arquivos_gerados:
            return True, f"{len(arquivos_gerados)} etiqueta(s) gerada(s) em PDF (sem envio).{msg_aviso}"

        # Caso não tenha nada
        return True, "Nada a imprimir."

    except Exception as e:
        return False, f"Erro ao processar etiquetas: {str(e)}"

def teste_zpl_win32(nome_impressora: str):
    import win32print
    zpl = "^XA^POI^PW800^LL320^LH0,0^FO40,40^A0N,60,60^FDTESTE ZPL^FS^XZ\r\n"
    payload = zpl.encode("ascii", errors="ignore")
    h = win32print.OpenPrinter(nome_impressora)
    try:
        win32print.StartDocPrinter(h, 1, ("TESTE_ZPL", None, "RAW"))
        win32print.StartPagePrinter(h)
        win32print.WritePrinter(h, payload)
        win32print.EndPagePrinter(h)
        win32print.EndDocPrinter(h)
    finally:
        win32print.ClosePrinter(h)