# My Life Prime

**Descrição**: Aplicativo de produtividade pessoal com diário, tarefas, finanças, calendário, anotações e gerenciamento de perfil. Interface gráfica em Tkinter com tela de carregamento animada.

**Requisitos**:
- **Python**: 3.8 ou superior
- **Bibliotecas**: `tkinter` (parte da stdlib), `Pillow` (para manipular imagens)

Instale o Pillow se necessário:

```bash
pip install pillow
```

**Como executar**:
- Crie e ative um ambiente virtual (opcional):

```bash
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
.venv\\Scripts\\activate     # Windows PowerShell
```
- Execute o aplicativo:

```bash
python app.py
```

**Estrutura do projeto**
- **Entrada**: [app.py](app.py) — inicia a aplicação.
- **Carregamento**: [main/main_loading.py](main/main_loading.py) e [loading/loading_start.py](loading/loading_start.py) — tela de loading e sequência de inicialização.
- **Janela principal**: [main/main_window.py](main/main_window.py) — classe `PersonalApp` que inicializa os módulos.
- **Módulos de janela** (funcionalidades):
	- [window/perfil.py](window/perfil.py) — gerenciamento de perfil (usa Pillow para fotos).
	- [window/diario.py](window/diario.py) — diário pessoal.
	- [window/tarefa.py](window/tarefa.py) — lista de tarefas.
	- [window/financas.py](window/financas.py) — controle financeiro simples.
	- [window/calendario.py](window/calendario.py) — visualizador de calendário.
	- [window/anotacoes.py](window/anotacoes.py) — notas rápidas.
- **Dados**:
	- [personal_app_data.json](personal_app_data.json) — arquivo de dados do usuário (salva perfil, diário, tarefas, finanças e anotações).
	- [premium_profile_data.json](premium_profile_data.json) — (dados opcionais de perfil premium).
	- [profile_system_data.json](profile_system_data.json) — (dados do sistema de perfil).

**Comportamento importante**
- O aplicativo salva/recupera dados de `personal_app_data.json` no diretório atual.
- Se usar fotos de perfil, selecione imagens compatíveis (JPEG/PNG). O carregamento de imagens usa `Pillow`.

**Desenvolvimento e testes**
- Arquivo de teste disponível: [test.py](test.py) — use como ponto de partida para validar partes do projeto.
- Para desenvolver: abra o projeto no VS Code, execute `python app.py` e acompanhe logs na tela de carregamento.

**Contribuição**
- Sugestões e correções: abra uma issue ou envie um PR.
- Antes de enviar PRs, rode o app e verifique que as funcionalidades básicas (diário, tarefas, finanças, perfil) funcionam.

**Checklist para empacotamento**
- Adicionar `requirements.txt` com dependências (`Pillow`).
- Incluir instruções de build/empacotamento (PyInstaller/brief setup) se quiser distribuir executáveis.

**Licença**
- Escolha uma licença (por exemplo, MIT). Adicione `LICENSE` quando decidir.

**Contato**
- Autor / mantenedor: (adicione seu nome e contato aqui)

---

Se quiser, eu atualizo o `requirements.txt`, adiciono exemplos de uso mais detalhados ou reflito configurações específicas (ícones, recursos premium). Diga o que prefere.
