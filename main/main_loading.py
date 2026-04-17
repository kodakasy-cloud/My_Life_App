import logging
from logging.handlers import RotatingFileHandler
import tkinter as tk

# Configurar logging rotativo para diagnóstico
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
log_handler = RotatingFileHandler(
    'app.log', maxBytes=1024 * 1024, backupCount=5, encoding='utf-8'
)
log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s'))
logger.addHandler(log_handler)

try:
    from loading.loading_start import LoadingScreen
except Exception as exc:
    raise ImportError('Could not import LoadingScreen from loading.loading_start') from exc


def start_app():
    """
    Inicia o loading na thread principal do Tkinter.
    Ao terminar, destrói a janela de loading e abre a janela principal
    — tudo na mesma thread, que é o único modo seguro com Tkinter.
    """
    root = tk.Tk()
    loading = LoadingScreen(root)

    def launch_main():
        """
        Chamado após root.destroy() dentro de _finish().
        Cria um novo Tk() — seguro porque estamos na thread principal
        e o loop anterior já foi encerrado.
        """
        try:
            from main.main_window import PersonalApp
            main_root = tk.Tk()
            PersonalApp(main_root)
            main_root.mainloop()
        except Exception:
            logging.getLogger(__name__).exception("Erro ao iniciar a aplicação principal")

    loading.set_on_complete(launch_main)
    root.mainloop()          # Bloqueia aqui até o loading terminar
    # Depois do mainloop encerrar, launch_main já terá sido chamado
    # e o segundo mainloop() estará rodando.


if __name__ == '__main__':
    start_app()