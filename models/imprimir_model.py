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
    """
    Gera ZPL para etiqueta 100x40 mm (ZD220 - 203 dpi)
    """
    width = mm_to_dots(100)
    height = mm_to_dots(40)

    loc_display = (localizacao or "N/I").strip()
    if len(loc_display) > 12:
        loc_display = loc_display[:12]

    # Ajuste de tamanhos: A0N,h,w (altura/largura em dots das fontes proportionais da Zebra)
    # Pode ajustar se quiser mais “grosso/fino”
    zpl = [
        "^XA",
        f"^PW{width}",
        f"^LL{height}",
        "^LH0,0",

        # moldura
        f"^FO{mm_to_dots(2)},{mm_to_dots(2)}^GB{width - mm_to_dots(4)},{height - mm_to_dots(4)},2^FS",

        # CÓDIGO (grande)
        f"^FO{mm_to_dots(5)},{mm_to_dots(3)}^A0N,40,40^FD{codigo}^FS",

        # KARDEX (médio)
        f"^FO{mm_to_dots(5)},{mm_to_dots(12)}^A0N,28,28^FD{kardex}^FS",

        # Pedido (pequeno)
        f"^FO{mm_to_dots(5)},{mm_to_dots(20)}^A0N,20,20^FD{pedido}^FS",

        # Requisitante (pequeno)
        f"^FO{mm_to_dots(5)},{mm_to_dots(24)}^A0N,20,20^FD{requisitante}^FS",

        # Quantidade (médio)
        f"^FO{mm_to_dots(5)},{mm_to_dots(30)}^A0N,28,28^FDQtde: {quantidade}^FS",

        # Localização (médio, à direita)
        f"^FO{mm_to_dots(50)},{mm_to_dots(30)}^A0N,28,28^FDLOC: {loc_display}^FS",

        "^XZ",
    ]
    return "\n".join(zpl)

def imprimir_zpl_via_spooler(nome_impressora: str, zpl: str):
    """
    Envia ZPL como RAW para a impressora no Windows.
    Requer pywin32 instalado:  pip install pywin32
    """
    try:
        import win32print
        hPrinter = win32print.OpenPrinter(nome_impressora)
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Etiqueta ZPL", None, "RAW"))
            try:
                win32print.StartPagePrinter(hPrinter)
                # Zebra espera binário RAW
                win32print.WritePrinter(hPrinter, zpl.encode("utf-8"))
                win32print.EndPagePrinter(hPrinter)
            finally:
                win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)
    except Exception as e:
        raise RuntimeError(f"Falha no spooler Windows: {e}")

def imprimir_zpl_via_tcp(ip: str, zpl: str, port: int = 9100, timeout: float = 5.0):
    """
    Envia ZPL via socket (RAW 9100) para Zebra na rede.
    """
    try:
        import socket
        with socket.create_connection((ip, port), timeout=timeout) as s:
            s.sendall(zpl.encode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"Falha no envio TCP {ip}:{port} -> {e}")


def listar_impressoras():
    """
    Lista as impressoras disponíveis no sistema
    """
    try:
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
            
        elif sistema == "Linux":
            resultado = subprocess.run(
                ['lpstat', '-p'],
                capture_output=True,
                text=True,
                check=True
            )
            
            impressoras = []
            for linha in resultado.stdout.split('\n'):
                if linha.startswith('printer'):
                    nome = linha.split()[1]
                    impressoras.append(nome)
            
            return impressoras
            
        elif sistema == "Darwin":
            resultado = subprocess.run(
                ['lpstat', '-p'],
                capture_output=True,
                text=True,
                check=True
            )
            
            impressoras = []
            for linha in resultado.stdout.split('\n'):
                if 'idle' in linha or 'printing' in linha:
                    partes = linha.split()
                    if partes:
                        impressoras.append(partes[1])
            
            return impressoras
            
        else:
            return []
            
    except Exception as e:
        print(f"Erro ao listar impressoras: {e}")
        return []

def imprimir_pdf(arquivo_pdf, nome_impressora=None):
    """
    Envia um PDF para a impressora especificada ou salva como PDF
    """
    try:
        sistema = platform.system()
        
        if not os.path.exists(arquivo_pdf):
            return False, f"Arquivo não encontrado: {arquivo_pdf}"
        
        # Se for para salvar como PDF, apenas retorna sucesso (já está salvo)
        if nome_impressora == "Salvar como PDF":
            return True, f"PDF salvo em: {arquivo_pdf}"
        
        if sistema == "Windows":
            if nome_impressora and nome_impressora != "Padrão do Sistema":
                # Usar PowerShell para imprimir em impressora específica
                comando = [
                    'powershell',
                    '-command',
                    f'Start-Process -FilePath "{arquivo_pdf}" -Verb Print -PassThru | ' +
                    f'foreach {{ $_.Printer = "{nome_impressora}"; $_ }}'
                ]
                subprocess.run(comando, check=True)
                return True, f"Arquivo enviado para impressora: {nome_impressora}"
            else:
                # Impressora padrão
                os.startfile(arquivo_pdf, "print")
                return True, "Arquivo enviado para impressora padrão"
        
        elif sistema == "Linux" or sistema == "Darwin":
            if nome_impressora and nome_impressora != "Padrão do Sistema":
                comando = ['lp', '-d', nome_impressora, arquivo_pdf]
            else:
                comando = ['lp', arquivo_pdf]
            
            subprocess.run(comando, check=True)
            return True, f"Arquivo enviado para impressora: {nome_impressora or 'padrão'}"
        
    except Exception as e:
        return False, f"Erro ao imprimir: {str(e)}"

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

def gerar_etiqueta_pdf(pedido, kardex, codigo, quantidade, requisitante, fornecedor, localizacao):
    """
    Gera uma etiqueta em PDF usando ReportLab com layout personalizado
    Tamanho: 100mm x 40mm
    """
    try:
        # Criar pasta de etiquetas se não existir
        pasta_etiquetas = "etiquetas"
        if not os.path.exists(pasta_etiquetas):
            os.makedirs(pasta_etiquetas)
        
        # Nome do arquivo com data/hora para evitar sobrescrita
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_base = pedido.replace('/', '_').replace('\\', '_')
        nome_arquivo = f"{pasta_etiquetas}/etiqueta_{nome_base}_{timestamp}.pdf"
        
        # Definir tamanho da etiqueta (100mm x 40mm)
        largura = 100 * mm
        altura = 40 * mm
        
        # Criar PDF com tamanho personalizado
        c = canvas.Canvas(nome_arquivo, pagesize=(largura, altura))
        
        # Desenhar borda
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(0.5)
        c.rect(2*mm, 2*mm, largura - 4*mm, altura - 4*mm)
        
        # Margens em mm
        margem_esquerda = 5 * mm
        margem_superior = altura - 8 * mm
        
        # CÓDIGO - tamanho grande
        # c.setFont("Helvetica-Bold", 32)
        # c.drawString(margem_esquerda, margem_superior - 4*mm, f"{codigo}")
        
        # KARDEX - tamanho médio
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margem_esquerda, margem_superior - 8*mm, f"{kardex}")
        
        # Pedido - pequeno
        c.setFont("Helvetica", 8)
        c.drawString(margem_esquerda, margem_superior - 16*mm, f"{pedido}")
        
        # Requisitante - pequeno
        c.setFont("Helvetica", 8)
        c.drawString(margem_esquerda, margem_superior - 20*mm, f"{requisitante}")
        
        # QUANTIDADE - médio (esquerda)
        c.setFont("Helvetica", 14)
        c.drawString(margem_esquerda, margem_superior - 26*mm, f"Qtde: {quantidade}")
        
        # LOCALIZAÇÃO (locNovo) - médio (direita)
        c.setFont("Helvetica", 14)
        # Tratar localização para não ficar muito longa
        loc_display = localizacao if len(localizacao) < 15 else localizacao[:12] + "..."
        c.drawString(33*mm, margem_superior - 26*mm, f"LOC: {loc_display}")
        
        c.save()
        return True, nome_arquivo
        
    except Exception as e:
        return False, str(e)

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