"""Pacote main: evitar imports pesados no __init__ para prevenir ciclos de import.

Importe submódulos explicitamente quando necessário, por exemplo:
```
from main.main_loading import start_app
from main.main_window import PersonalApp
```
```
"""

__all__ = []