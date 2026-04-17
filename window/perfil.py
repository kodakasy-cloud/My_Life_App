import json
import os
from tkinter import messagebox

# Caminho para o arquivo de dados no diretório raiz do projeto
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_FILE = os.path.join(ROOT, 'personal_app_data.json')

def load_profile():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get('profile', {})
    except Exception:
        return {}
    return {}

def save_profile(profile_data: dict):
    try:
        data = {}
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        data['profile'] = profile_data
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

def open_profile(parent=None):
    """Abertura simplificada da tela de perfil.

    Mantém a interface leve para importação em ambientes sem GUI.
    """
    try:
        messagebox.showinfo('Perfil', '👤 Funcionalidade de perfil em desenvolvimento.')
    except Exception:
        # Em ambientes sem GUI simplesmente ignore
        return

__all__ = ['load_profile', 'save_profile', 'open_profile']
