# models/transferencia_model.py
import os
import json
from typing import List, Dict
from models.config_model import obter_pasta_dados

_ARQUIVO = "transferencias.json"

def _caminho_arquivo() -> str:
    pasta = obter_pasta_dados() or os.path.join(os.path.expanduser("~"), "Documents", "Almoxarifado")
    os.makedirs(pasta, exist_ok=True)
    return os.path.join(pasta, _ARQUIVO)

def carregar_transferencias() -> List[Dict]:
    arq = _caminho_arquivo()
    if not os.path.exists(arq):
        return []
    try:
        with open(arq, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def salvar_transferencias(registros: List[Dict]) -> None:
    arq = _caminho_arquivo()
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)

def filtrar_transferencias(registros: List[Dict], doc: str = "", kardex: str = "", de: str = "", para: str = "") -> List[Dict]:
    doc = (doc or "").strip().lower()
    kardex = (kardex or "").strip().lower()
    de = (de or "").strip().lower()
    para = (para or "").strip().lower()

    def _ok(v: str, f: str) -> bool:
        return (not f) or (f in str(v or "").lower())

    out = []
    for r in registros:
        if _ok(r.get("documento"), doc) and _ok(r.get("kardex"), kardex) and _ok(r.get("de_deposito"), de) and _ok(r.get("para_deposito"), para):
            out.append(r)
    return out