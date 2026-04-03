import os
import json
from models.config_model import obter_pasta_itens


def carregar_itens_almoxarifado():
    """
    Carrega os dados do arquivo itensAlmoxarifado.json
    """
    try:
        print("=== CARREGANDO ITENS ALMOXARIFADO ===")
        
        pasta_itens = obter_pasta_itens()
        print(f"Pasta de itens configurada: {pasta_itens}")
        
        if not pasta_itens:
            print("❌ Pasta de itens não configurada")
            return []
        
        arquivo = os.path.join(pasta_itens, "itensAlmoxarifado.json")
        print(f"Caminho completo do arquivo: {arquivo}")
        
        if not os.path.exists(arquivo):
            print(f"❌ Arquivo não encontrado: {arquivo}")
            return []
        
        tamanho = os.path.getsize(arquivo)
        print(f"✅ Arquivo encontrado! Tamanho: {tamanho} bytes")
        
        if tamanho == 0:
            print("⚠️ Arquivo vazio!")
            return []
        
        # Tentar ler com encoding utf-8-sig (remove BOM automaticamente)
        try:
            with open(arquivo, "r", encoding="utf-8-sig") as f:
                dados = json.load(f)
            print(f"✅ Carregados {len(dados)} itens do almoxarifado (utf-8-sig)")
            
            # Mostrar os primeiros itens para debug
            if dados:
                print("\nPrimeiro item (exemplo):")
                primeiro = dados[0]
                for chave in list(primeiro.keys())[:10]:
                    print(f"  {chave}: {primeiro.get(chave)}")
            
            return dados
            
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao decodificar JSON: {e}")
            
            # Tentar ler como texto puro para debug
            with open(arquivo, "r", encoding="utf-8-sig") as f:
                conteudo = f.read()
                print(f"Primeiros 200 caracteres do arquivo:\n{conteudo[:200]}")
            
            return []
        
    except Exception as e:
        print(f"❌ Erro ao carregar itens: {e}")
        import traceback
        traceback.print_exc()
        return []


def filtrar_itens(itens, termo_busca):
    """
    Filtra os itens por código, descrição ou kardex
    """
    if not termo_busca:
        return itens
    
    termo = termo_busca.lower().strip()
    resultado = []
    
    for item in itens:
        codigo = str(item.get("codigo", "")).lower()
        descricao = str(item.get("descricao", "")).lower()
        kardex = str(item.get("kardex", "")).lower()
        
        if termo in codigo or termo in descricao or termo in kardex:
            resultado.append(item)
    
    print(f"Filtro '{termo_busca}': {len(resultado)} itens encontrados de {len(itens)}")
    return resultado