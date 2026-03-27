import os
from datetime import datetime

def obter_pasta_anotacoes():
    """
    Obtém ou cria a pasta de anotações baseada na pasta de itens
    """
    from models.config_model import obter_pasta_itens
    
    pasta_itens = obter_pasta_itens()
    if not pasta_itens:
        return None
    
    pasta_anotacoes = os.path.join(pasta_itens, "AE_anotacoes")
    
    # Criar pasta se não existir
    if not os.path.exists(pasta_anotacoes):
        os.makedirs(pasta_anotacoes)
        print(f"Pasta de anotações criada: {pasta_anotacoes}")
    
    return pasta_anotacoes

def limpar_arquivos_antigos(pasta, limite=30):
    """
    Mantém apenas os 'limite' arquivos mais recentes, apaga os mais antigos
    
    Args:
        pasta: Caminho da pasta com os arquivos .txt
        limite: Número máximo de arquivos a manter (padrão: 30)
    
    Returns:
        int: Número de arquivos apagados
    """
    try:
        if not os.path.exists(pasta):
            return 0
        
        # Listar todos os arquivos .txt com data no nome (formato YYYY-MM-DD.txt)
        arquivos = []
        for arquivo in os.listdir(pasta):
            if arquivo.endswith('.txt') and len(arquivo) == 14:  # YYYY-MM-DD.txt = 14 caracteres
                caminho_completo = os.path.join(pasta, arquivo)
                arquivos.append((arquivo, os.path.getmtime(caminho_completo)))
        
        # Ordenar por data de modificação (mais recente primeiro)
        arquivos.sort(key=lambda x: x[1], reverse=True)
        
        # Verificar se ultrapassou o limite
        if len(arquivos) > limite:
            arquivos_para_apagar = arquivos[limite:]  # Pega os excedentes (mais antigos)
            
            for arquivo, _ in arquivos_para_apagar:
                caminho_arquivo = os.path.join(pasta, arquivo)
                os.remove(caminho_arquivo)
                print(f"🗑️ Arquivo antigo removido: {arquivo}")
            
            return len(arquivos_para_apagar)
        
        return 0
        
    except Exception as e:
        print(f"Erro ao limpar arquivos antigos: {e}")
        return 0

def salvar_anotacao(texto):
    """
    Salva o texto da anotação em um arquivo .txt com data atual
    
    Args:
        texto: String com o conteúdo da anotação
    
    Returns:
        tuple: (sucesso, mensagem, caminho_arquivo)
    """
    try:
        # Obter pasta de anotações
        pasta_anotacoes = obter_pasta_anotacoes()
        
        if not pasta_anotacoes:
            return False, "Pasta de itens não configurada", None
        
        # Nome do arquivo com data atual
        data_atual = datetime.now().strftime("%d-%m-%Y")
        nome_arquivo = f"{data_atual}.txt"
        caminho_completo = os.path.join(pasta_anotacoes, nome_arquivo)
        
        # Salvar o arquivo (sobrescreve se existir)
        with open(caminho_completo, "w", encoding="utf-8") as f:
            f.write(texto)
        
        print(f"✅ Anotação salva em: {caminho_completo}")
        
        # LIMPEZA AUTOMÁTICA: manter apenas 30 arquivos mais recentes
        apagados = limpar_arquivos_antigos(pasta_anotacoes, limite=30)
        
        if apagados > 0:
            print(f"🧹 {apagados} arquivo(s) antigo(s) removido(s) - limite de 30 arquivos")
        
        return True, f"Anotação salva em {nome_arquivo}", caminho_completo
        
    except Exception as e:
        print(f"❌ Erro ao salvar anotação: {e}")
        return False, f"Erro ao salvar: {str(e)}", None

def carregar_anotacao(data=None):
    """
    Carrega uma anotação de uma data específica
    
    Args:
        data: Data no formato YYYY-MM-DD (se None, usa data atual)
    
    Returns:
        str: Conteúdo da anotação ou string vazia se não existir
    """
    try:
        if data is None:
            data = datetime.now().strftime("%Y-%m-%d")
        
        pasta_anotacoes = obter_pasta_anotacoes()
        
        if not pasta_anotacoes:
            return ""
        
        caminho_arquivo = os.path.join(pasta_anotacoes, f"{data}.txt")
        
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                return f.read()
        
        return ""
        
    except Exception as e:
        print(f"Erro ao carregar anotação: {e}")
        return ""

def carregar_anotacao_mais_recente():
    """
    Carrega a anotação mais recente (última data)
    
    Returns:
        str: Conteúdo da anotação mais recente ou string vazia
    """
    try:
        pasta_anotacoes = obter_pasta_anotacoes()
        
        if not pasta_anotacoes or not os.path.exists(pasta_anotacoes):
            return ""
        
        # Listar todos os arquivos .txt
        arquivos = [f for f in os.listdir(pasta_anotacoes) if f.endswith('.txt')]
        
        if not arquivos:
            return ""
        
        # Ordenar por nome (que é a data) e pegar o último
        arquivos.sort(reverse=True)  # Do mais novo para o mais velho
        arquivo_mais_recente = arquivos[0]
        
        caminho_arquivo = os.path.join(pasta_anotacoes, arquivo_mais_recente)
        
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            return f.read()
        
    except Exception as e:
        print(f"Erro ao carregar anotação mais recente: {e}")
        return ""

def listar_anotacoes_disponiveis():
    """
    Lista todas as datas com anotações disponíveis
    
    Returns:
        list: Lista de strings com datas no formato YYYY-MM-DD
    """
    try:
        pasta_anotacoes = obter_pasta_anotacoes()
        
        if not pasta_anotacoes or not os.path.exists(pasta_anotacoes):
            return []
        
        arquivos = [f for f in os.listdir(pasta_anotacoes) if f.endswith('.txt')]
        datas = [f.replace('.txt', '') for f in arquivos]
        datas.sort(reverse=True)  # Mais recentes primeiro
        
        return datas
        
    except Exception as e:
        print(f"Erro ao listar anotações: {e}")
        return []