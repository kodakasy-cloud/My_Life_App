import logging
import tempfile
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import tkinter.font as tkfont
from typing import Any

from window.diario import DiarioManager
from window.tarefa import TarefasManager
from window.financas import FinancasManager
from window.calendario import CalendarioManager
from window.anotacoes import AnotacoesManager


# Utilitários compartilhados
def adjust_color_hex(color: str, factor: float) -> str:
    """Ajusta o brilho de uma cor hex (#rrggbb) e retorna o novo hex."""
    try:
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, min(255, int(r * factor)))
        g = max(0, min(255, int(g * factor)))
        b = max(0, min(255, int(b * factor)))
        return f'#{r:02x}{g:02x}{b:02x}'
    except Exception:
        return color


def safe_float(value) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


MINIFY_JSON = True


class ModernButton(tk.Button):
    """Botão moderno com efeitos visuais estáveis"""
    def __init__(self, parent, text, command, color="#3498DB", icon="", **kwargs):
        super().__init__(parent, text=f"{icon} {text}" if icon else text,
                        command=command, bg=color, fg='white',
                        font=("Segoe UI", 10, "bold"), relief=tk.FLAT,
                        cursor='hand2', padx=15, pady=8, **kwargs)
        self.color = color
        self.default_bg = color
        self.hover_bg = self.adjust_color(color, 0.8)
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def adjust_color(self, color, factor):
        return adjust_color_hex(color, factor)
    
    def on_enter(self, event):
        self.configure(bg=self.hover_bg)
    
    def on_leave(self, event):
        self.configure(bg=self.default_bg)


class PersonalApp:
    def __init__(self, root):
        self.root = root
        logging.getLogger(__name__).info("Inicializando PersonalApp")
        self.root.title("Meu Painel Pessoal - Organizador Inteligente")
        
        # Configurar tamanho da janela
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Tamanho proporcional à tela (80% da tela)
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        window_width = max(1024, min(window_width, 1600))
        window_height = max(700, min(window_height, 900))
        
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.minsize(1024, 700)
        self.root.configure(bg='#F8F9FA')
        
        # Centralizar a janela
        self.center_window()
        
        # Configurar grid responsivo
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Cores do tema
        self.colors = {
            "primary": "#3498DB",
            "primary_hover": "#2980B9",
            "success": "#27AE60",
            "success_hover": "#229954",
            "danger": "#E74C3C",
            "danger_hover": "#C0392B",
            "warning": "#F39C12",
            "purple": "#9B59B6",
            "orange": "#E67E22",
            "teal": "#1ABC9C",
            "gray": "#7F8C8D",
            "gray_light": "#BDC3C7",
            "dark": "#2C3E50",
            "light": "#ECF0F1",
            "white": "#FFFFFF",
            "background": "#F8F9FA"
        }
        
        # Fontes responsivas
        self.setup_fonts(window_width)
        
        # Dados do usuário (valores padrão)
        self.user_data = {
            "nome": "Usuário",
            "idade": "",
            "email": "",
            "cidade": "",
            "foto_path": None,
            "ultimo_acesso": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        # Dados do diário
        self.diario_entries = []
        
        # Dados das tarefas
        self.tasks = []
        
        # Dados financeiros
        self.financas = []
        
        # Anotações
        self.notas = []
        
        # Eventos do calendário
        self.eventos = {}
        
        self.load_data()
        self.create_widgets()
        
        # Inicializar managers
        self.diario_manager = DiarioManager(self)
        self.tarefas_manager = TarefasManager(self)
        self.financas_manager = FinancasManager(self)
        self.calendario_manager = CalendarioManager(self)
        self.anotacoes_manager = AnotacoesManager(self)
        
        # Atualizar última sessão
        self.user_data["ultimo_acesso"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.save_data()
        logging.getLogger(__name__).info("Aplicação principal inicializada e dados salvos")
        
        # Iniciar atualização do relógio (único after seguro)
        self.update_datetime()
    
    def setup_fonts(self, screen_width):
        """Configura fontes baseadas no tamanho da tela"""
        if screen_width < 1280:
            self.fonts = {
                "title": ("Segoe UI", 16, "bold"),
                "subtitle": ("Segoe UI", 12, "bold"),
                "body": ("Segoe UI", 9),
                "small": ("Segoe UI", 8)
            }
        elif screen_width < 1600:
            self.fonts = {
                "title": ("Segoe UI", 18, "bold"),
                "subtitle": ("Segoe UI", 13, "bold"),
                "body": ("Segoe UI", 10),
                "small": ("Segoe UI", 9)
            }
        else:
            self.fonts = {
                "title": ("Segoe UI", 20, "bold"),
                "subtitle": ("Segoe UI", 14, "bold"),
                "body": ("Segoe UI", 11),
                "small": ("Segoe UI", 10)
            }
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def create_widgets(self):
        # Container principal
        main_container = tk.Frame(self.root, bg=self.colors["background"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Barra superior
        self.create_top_bar(main_container)
        
        # Frame principal
        content_wrapper = tk.Frame(main_container, bg=self.colors["background"])
        content_wrapper.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Sidebar (20% da largura)
        sidebar_width = int(self.root.winfo_width() * 0.2)
        sidebar_width = max(220, min(280, sidebar_width))
        
        self.sidebar = tk.Frame(content_wrapper, bg=self.colors["white"], width=sidebar_width)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Frame de conteúdo (80% da largura)
        self.content_frame = tk.Frame(content_wrapper, bg=self.colors["white"])
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Criar conteúdo da sidebar
        self.create_sidebar_content()
        
        # Mostrar dashboard inicial
        self.show_dashboard()
    
    def create_top_bar(self, parent):
        """Cria a barra superior"""
        top_bar = tk.Frame(parent, bg=self.colors["white"], height=65)
        top_bar.pack(fill=tk.X, pady=(0, 10))
        top_bar.pack_propagate(False)
        
        # Borda inferior
        border = tk.Frame(top_bar, bg=self.colors["primary"], height=3)
        border.place(x=0, y=62, relwidth=1)
        
        # Container esquerdo
        left_frame = tk.Frame(top_bar, bg=self.colors["white"])
        left_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Ícone
        tk.Label(left_frame, text="✨", font=("Segoe UI", 24), 
                bg=self.colors["white"]).pack(side=tk.LEFT, padx=(0, 10))
        
        # Saudação (sem perfil, texto fixo)
        self.welcome_label = tk.Label(left_frame, text="Meu Painel Pessoal", 
                                      font=self.fonts["subtitle"],
                                      bg=self.colors["white"], fg=self.colors["dark"])
        self.welcome_label.pack(side=tk.LEFT)
        
        # Container direito
        right_frame = tk.Frame(top_bar, bg=self.colors["white"])
        right_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Relógio
        self.datetime_label = tk.Label(right_frame, text="", 
                                       font=self.fonts["body"],
                                       bg=self.colors["white"], fg=self.colors["gray"])
        self.datetime_label.pack(side=tk.RIGHT, padx=(0, 15))
        
        # Botões
        buttons_frame = tk.Frame(right_frame, bg=self.colors["white"])
        buttons_frame.pack(side=tk.RIGHT)
        
        self.create_top_button(buttons_frame, "🔔", self.show_notifications)
        self.create_top_button(buttons_frame, "⚙️", self.show_settings)
        
        tk.Frame(buttons_frame, width=1, bg=self.colors["light"]).pack(side=tk.LEFT, padx=10, fill=tk.Y, pady=5)
        self.create_top_button(buttons_frame, "👤", self.edit_profile)
    
    def create_top_button(self, parent, icon, command):
        """Cria botão na barra superior"""
        btn = tk.Label(parent, text=icon, font=("Segoe UI", 16),
                       bg=self.colors["white"], fg=self.colors["gray"], cursor='hand2')
        btn.pack(side=tk.LEFT, padx=5)
        btn.bind('<Button-1>', lambda e: command())
        
        # Efeito hover simples
        def on_enter(e):
            btn.configure(fg=self.colors["primary"])
        def on_leave(e):
            btn.configure(fg=self.colors["gray"])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def update_datetime(self):
        """Atualiza o relógio - único after seguro"""
        try:
            now = datetime.now()
            self.datetime_label.config(text=now.strftime("%A, %d de %B de %Y • %H:%M"))
            self.root.after(1000, self.update_datetime)
        except Exception as e:
            print(f"Erro em update_datetime: {e}")
    
    def create_sidebar_content(self):
        """Cria o conteúdo da sidebar"""
        # Logo/Ícone no lugar do avatar
        logo_frame = tk.Frame(self.sidebar, bg=self.colors["white"])
        logo_frame.pack(fill=tk.X, pady=25)
        
        # Ícone do app
        logo_canvas = tk.Canvas(logo_frame, width=80, height=80,
                                bg=self.colors["white"], highlightthickness=0)
        logo_canvas.pack(pady=(10, 5))
        logo_canvas.create_oval(5, 5, 75, 75, fill=self.colors["primary"], 
                                outline=self.colors["primary"], width=3)
        logo_canvas.create_text(40, 40, text="✨", font=("Segoe UI", 40), 
                                fill="white")
        
        # Título do app
        tk.Label(logo_frame, text="Organizador", 
                font=self.fonts["subtitle"], bg=self.colors["white"], 
                fg=self.colors["dark"]).pack()
        
        tk.Label(logo_frame, text="✨ Sua vida organizada ✨", 
                font=self.fonts["small"], bg=self.colors["white"], 
                fg=self.colors["gray"]).pack(pady=(2, 10))
        
        # Separador
        self.create_separator(self.sidebar)
        
        # Menu
        menu_items = [
            ("📊 Dashboard", self.show_dashboard, self.colors["primary"]),
            ("📔 Diário", self.open_diario, self.colors["purple"]),
            ("✅ Tarefas", self.open_tarefas, self.colors["orange"]),
            ("💰 Finanças", self.open_financas, self.colors["success"]),
            ("📅 Calendário", self.open_calendario, self.colors["danger"]),
            ("📝 Anotações", self.open_anotacoes, self.colors["teal"]),
        ]
        
        for text, command, color in menu_items:
            btn = ModernButton(self.sidebar, text=text, command=command, 
                              color=color, icon=text[0])
            btn.pack(fill=tk.X, padx=15, pady=3)
        
        # Separador
        self.create_separator(self.sidebar)
        
        # Estatísticas
        self.create_stats_panel()
        
        # Botão sair
        tk.Frame(self.sidebar, height=20, bg=self.colors["white"]).pack()
        logout_btn = ModernButton(self.sidebar, text="Sair", command=self.confirm_exit,
                                  color=self.colors["danger"], icon="🚪")
        logout_btn.pack(fill=tk.X, padx=15, pady=10)
    
    def create_separator(self, parent):
        """Cria separador decorativo"""
        sep_frame = tk.Frame(parent, bg=self.colors["white"])
        sep_frame.pack(fill=tk.X, padx=15, pady=10)
        separator = tk.Frame(sep_frame, height=2, bg=self.colors["light"])
        separator.pack(fill=tk.X)
    
    def create_stats_panel(self):
        """Cria painel de estatísticas"""
        stats_frame = tk.Frame(self.sidebar, bg=self.colors["light"])
        stats_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(stats_frame, text="📊 Estatísticas", font=self.fonts["subtitle"],
                bg=self.colors["light"], fg=self.colors["dark"]).pack(anchor=tk.W, pady=(10, 10), padx=10)
        
        stats_items = [
            ("✅ Tarefas", len(self.tasks), self.colors["orange"]),
            ("📔 Diário", len(self.diario_entries), self.colors["purple"]),
            ("💰 Finanças", len(self.financas), self.colors["success"]),
            ("📝 Anotações", len(self.notas), self.colors["teal"]),
        ]
        
        for text, count, color in stats_items:
            stat_card = tk.Frame(stats_frame, bg=self.colors["white"], relief=tk.RAISED, bd=1)
            stat_card.pack(fill=tk.X, pady=3, padx=10)
            stat_card.configure(highlightbackground=self.colors["gray_light"], highlightthickness=1)
            
            inner = tk.Frame(stat_card, bg=self.colors["white"])
            inner.pack(fill=tk.X, padx=10, pady=8)
            
            tk.Label(inner, text=text, font=self.fonts["body"],
                    bg=self.colors["white"], fg=self.colors["gray"]).pack(side=tk.LEFT)
            
            tk.Label(inner, text=str(count), font=("Segoe UI", 12, "bold"),
                    bg=self.colors["white"], fg=color).pack(side=tk.RIGHT)
    
    def show_dashboard(self):
        """Mostra o dashboard principal"""
        self.clear_content()
        
        # Container com scroll
        canvas = tk.Canvas(self.content_frame, bg=self.colors["white"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["white"])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título
        title_frame = tk.Frame(scrollable_frame, bg=self.colors["white"])
        title_frame.pack(fill=tk.X, padx=30, pady=30)
        
        tk.Label(title_frame, text="📊 Dashboard", font=self.fonts["title"],
                bg=self.colors["white"], fg=self.colors["dark"]).pack(anchor=tk.W)
        tk.Label(title_frame, text="Visão geral da sua vida organizada",
                font=self.fonts["body"], bg=self.colors["white"], 
                fg=self.colors["gray"]).pack(anchor=tk.W, pady=(5, 0))
        
        # Cards
        cards_frame = tk.Frame(scrollable_frame, bg=self.colors["white"])
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        # Configurar grid responsivo
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)
        
        # Dados dos cards
        cards_data = [
            ("✅ Tarefas", f"{len(self.tasks)} pendentes", "Ver tarefas", 
             self.colors["orange"], self.open_tarefas),
            ("📔 Diário", f"{len(self.diario_entries)} entradas", "Escrever", 
             self.colors["purple"], self.open_diario),
            ("💰 Finanças", self.get_saldo_text(), "Ver detalhes", 
             self.colors["success"], self.open_financas),
            ("📝 Anotações", f"{len(self.notas)} notas", "Criar nota", 
             self.colors["teal"], self.open_anotacoes),
        ]
        
        for i, (title, value, action, color, command) in enumerate(cards_data):
            card = self.create_dashboard_card(cards_frame, title, value, action, color, command)
            card.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
        
        # Atividades recentes
        recent_frame = tk.Frame(scrollable_frame, bg=self.colors["white"])
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(recent_frame, text="📋 Atividades Recentes", font=self.fonts["subtitle"],
                bg=self.colors["white"], fg=self.colors["dark"]).pack(anchor=tk.W, pady=(0, 15))
        
        # Lista de atividades
        activities = self.get_recent_activities()
        
        if activities:
            for activity in activities[:5]:
                self.create_activity_item(recent_frame, activity)
        else:
            empty_label = tk.Label(recent_frame, text="Nenhuma atividade recente", 
                                   font=self.fonts["body"], bg=self.colors["white"], 
                                   fg=self.colors["gray"])
            empty_label.pack(pady=30)
    
    def create_dashboard_card(self, parent, title, value, action_text, color, command):
        """Cria um card do dashboard"""
        card = tk.Frame(parent, bg=self.colors["white"], relief=tk.RAISED, bd=1)
        card.configure(highlightbackground=self.colors["gray_light"], highlightthickness=1)
        
        inner = tk.Frame(card, bg=self.colors["white"])
        inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Ícone
        icon_label = tk.Label(inner, text=title[0], font=("Segoe UI", 34), 
                              bg=self.colors["white"], fg=color)
        icon_label.pack()
        
        # Título
        tk.Label(inner, text=title[2:], font=self.fonts["subtitle"],
                bg=self.colors["white"], fg=self.colors["dark"]).pack(pady=(5, 0))
        
        # Valor
        tk.Label(inner, text=value, font=("Segoe UI", 15, "bold"),
                bg=self.colors["white"], fg=color).pack(pady=5)
        
        # Botão
        btn = tk.Button(inner, text=action_text, command=command,
                        bg=color, fg='white', font=self.fonts["body"],
                        relief=tk.FLAT, cursor='hand2', padx=15, pady=5)
        btn.pack(pady=(10, 0))
        
        # Hover effect
        def on_enter(e):
            btn.configure(bg=self.adjust_color(color, 0.8))
        def on_leave(e):
            btn.configure(bg=color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return card
    
    def adjust_color(self, color, factor):
        """Ajusta o brilho da cor"""
        return adjust_color_hex(color, factor)
    
    def create_activity_item(self, parent, activity):
        """Cria um item de atividade"""
        item_frame = tk.Frame(parent, bg=self.colors["light"], relief=tk.FLAT)
        item_frame.pack(fill=tk.X, pady=3)
        item_frame.configure(highlightbackground=self.colors["gray_light"], highlightthickness=1)
        
        inner = tk.Frame(item_frame, bg=self.colors["light"])
        inner.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(inner, text=activity["icon"], font=("Segoe UI", 14),
                bg=self.colors["light"]).pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(inner, text=activity["text"], font=self.fonts["body"],
                bg=self.colors["light"], fg=self.colors["dark"]).pack(side=tk.LEFT)
        tk.Label(inner, text=activity["date"], font=self.fonts["small"],
                bg=self.colors["light"], fg=self.colors["gray"]).pack(side=tk.RIGHT)
    
    def get_saldo_text(self):
        """Retorna o texto do saldo formatado"""
        total_receitas = sum(safe_float(item.get("valor", 0)) for item in self.financas if item.get("tipo") == "receita")
        total_despesas = sum(safe_float(item.get("valor", 0)) for item in self.financas if item.get("tipo") == "despesa")
        saldo = total_receitas - total_despesas
        return f"R$ {saldo:,.2f}"
    
    def get_recent_activities(self):
        """Retorna atividades recentes"""
        activities = []
        
        # Tarefas recentes
        for task in self.tasks[-3:]:
            activities.append({
                "icon": "✅",
                "text": f"Tarefa: {task.get('titulo', 'Sem título')}",
                "date": task.get('data_criacao', 'Data não informada')
            })
        
        # Entradas do diário
        for entry in self.diario_entries[-3:]:
            activities.append({
                "icon": "📔",
                "text": f"Diário: {entry.get('titulo', 'Nova entrada')[:30]}",
                "date": entry.get('data_formatada', 'Data não informada')
            })
        
        # Transações
        for trans in self.financas[-3:]:
            icon = "💰" if trans.get('tipo') == 'receita' else "💸"
            activities.append({
                "icon": icon,
                "text": f"{trans.get('descricao', 'Transação')} - R$ {float(trans.get('valor', 0)):,.2f}",
                "date": trans.get('data', 'Data não informada')
            })
        
        # Anotações
        for nota in self.notas[-3:]:
            activities.append({
                "icon": "📝",
                "text": f"Anotação: {nota.get('texto', 'Sem texto')[:30]}",
                "date": nota.get('data', 'Data não informada')
            })
        
        return sorted(activities, key=lambda x: x['date'], reverse=True)
    
    def show_notifications(self):
        """Mostra notificações"""
        messagebox.showinfo("Notificações", "🔔 Você não tem notificações no momento.\n\n✨ Volte em breve!")
    
    def show_settings(self):
        """Mostra janela de configurações"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Configurações")
        settings_window.geometry("500x450")
        settings_window.configure(bg=self.colors["white"])
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Centralizar
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (settings_window.winfo_screenheight() // 2) - (450 // 2)
        settings_window.geometry(f"500x450+{x}+{y}")
        
        main_frame = tk.Frame(settings_window, bg=self.colors["white"], padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="⚙️ Configurações", font=self.fonts["title"],
                bg=self.colors["white"], fg=self.colors["dark"]).pack(pady=(0, 20))
        
        # Informações
        info_frame = tk.Frame(main_frame, bg=self.colors["light"], relief=tk.RAISED, bd=1)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        info_inner = tk.Frame(info_frame, bg=self.colors["light"])
        info_inner.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(info_inner, text="📊 Informações do Sistema", font=self.fonts["subtitle"],
                bg=self.colors["light"], fg=self.colors["dark"]).pack(anchor=tk.W, pady=(0, 10))
        
        info_items = [
            f"Versão: 2.0.0",
            f"Último acesso: {self.user_data['ultimo_acesso']}",
            f"Total de registros: {len(self.diario_entries) + len(self.tasks) + len(self.financas) + len(self.notas)}"
        ]
        
        for item in info_items:
            tk.Label(info_inner, text=item, font=self.fonts["body"],
                    bg=self.colors["light"], fg=self.colors["gray"]).pack(anchor=tk.W, pady=2)
        
        # Backup
        backup_btn = ModernButton(main_frame, text="💾 Fazer Backup", command=self.backup_data,
                                  color=self.colors["primary"])
        backup_btn.pack(fill=tk.X, pady=5)
        
        # Fechar
        close_btn = ModernButton(main_frame, text="Fechar", command=settings_window.destroy,
                                 color=self.colors["gray"])
        close_btn.pack(fill=tk.X, pady=5)
    
    def backup_data(self):
        """Faz backup dos dados"""
        try:
            backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            data = {
                "user_data": self.user_data,
                "diario_entries": self.diario_entries,
                "tasks": self.tasks,
                "financas": self.financas,
                "notas": self.notas,
                "eventos": self.eventos
            }
            # Escritura atômica para evitar arquivos corrompidos
            dirpath = os.path.dirname(os.path.abspath(backup_file)) or '.'
            with tempfile.NamedTemporaryFile('w', delete=False, dir=dirpath, encoding='utf-8') as tf:
                if MINIFY_JSON:
                    json.dump(data, tf, ensure_ascii=False, separators=(',', ':'))
                else:
                    json.dump(data, tf, ensure_ascii=False, indent=2)
                temp_name = tf.name
            os.replace(temp_name, backup_file)
            messagebox.showinfo("Backup", f"✅ Backup criado com sucesso!\n\n📁 Arquivo: {backup_file}")
        except Exception as e:
            logging.exception("Erro ao criar backup")
            messagebox.showerror("Erro", f"❌ Erro ao criar backup: {str(e)}")
    
    def edit_profile(self):
        """Abre edição de perfil (funcionalidade simplificada)"""
        messagebox.showinfo("Perfil", "👤 Funcionalidade de perfil em desenvolvimento.\n\nOs dados são salvos automaticamente.")
    
    def open_diario(self):
        self.diario_manager.open_diario()
    
    def open_tarefas(self):
        self.tarefas_manager.open_tarefas()
    
    def open_financas(self):
        self.financas_manager.open_financas()
    
    def open_calendario(self):
        self.calendario_manager.open_calendario()
    
    def open_anotacoes(self):
        self.anotacoes_manager.open_anotacoes()
    
    def confirm_exit(self):
        """Confirma saída do aplicativo"""
        if messagebox.askyesno("Sair", "✨ Tem certeza que deseja sair?\n\nSeus dados serão salvos automaticamente."):
            self.save_data()
            self.root.quit()
    
    def clear_content(self):
        for widget in list(self.content_frame.winfo_children()):
            try:
                widget.destroy()
            except Exception:
                # Ignorar problemas ao destruir widgets (p.ex. master já removido)
                logging.getLogger(__name__).exception("Erro ao destruir widget durante clear_content")
    
    def save_data(self):
        data = {
            "user_data": self.user_data,
            "diario_entries": self.diario_entries,
            "tasks": self.tasks,
            "financas": self.financas,
            "notas": self.notas,
            "eventos": getattr(self, 'eventos', {})
        }
        try:
            # Escritura atômica: gravar em arquivo temporário e renomear
            dirpath = os.path.dirname(os.path.abspath("personal_app_data.json")) or '.'
            with tempfile.NamedTemporaryFile('w', delete=False, dir=dirpath, encoding='utf-8') as tf:
                if MINIFY_JSON:
                    json.dump(data, tf, ensure_ascii=False, separators=(',', ':'))
                else:
                    json.dump(data, tf, ensure_ascii=False, indent=2)
                temp_name = tf.name
            os.replace(temp_name, "personal_app_data.json")
            logging.getLogger(__name__).info("Dados salvos em personal_app_data.json")
        except Exception as e:
            logging.exception("Erro ao salvar dados")
            print(f"Erro ao salvar dados: {e}")
    
    def load_data(self):
        if os.path.exists("personal_app_data.json"):
            try:
                with open("personal_app_data.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.user_data = data.get("user_data", self.user_data)
                    self.diario_entries = data.get("diario_entries", [])
                    self.tasks = data.get("tasks", [])
                    self.financas = data.get("financas", [])
                    self.notas = data.get("notas", [])
                    self.eventos = data.get("eventos", {})
            except Exception as e:
                logging.exception("Erro ao carregar personal_app_data.json")
                print(f"Erro ao carregar dados: {e}")
            else:
                logging.getLogger(__name__).info("Dados carregados de personal_app_data.json")


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = PersonalApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")