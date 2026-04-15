import tkinter as tk
from loading.loading_start import LoadingScreen


def start_app():
    """Função que inicia a tela de loading e depois o app principal"""
    root = tk.Tk()
    loading = LoadingScreen(root)
    root.mainloop()