import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from PIL import Image, ImageTk
import tkinter.font as tkfont

from window.perfil import PerfilManager
from window.diario import DiarioManager
from window.tarefa import TarefasManager
from window.financas import FinancasManager
from window.calendario import CalendarioManager
from window.anotacoes import AnotacoesManager


class PersonalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meu Painel Pessoal - Organizador Inteligente")
        self.root.geometry("1300x750")
        self.root.configure(bg='#F8F9FA')
        
        # Centralizar a janela
        self.center_window()
        
        # Dados do usuário
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
        self.perfil_manager = PerfilManager(self)
        self.diario_manager = DiarioManager(self)
        self.tarefas_manager = TarefasManager(self)
        self.financas_manager = FinancasManager(self)
        self.calendario_manager = CalendarioManager(self)
        self.anotacoes_manager = AnotacoesManager(self)
        
        # Atualizar última sessão
        self.user_data["ultimo_acesso"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.save_data()
        
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = 1300
        height = 750
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        # Container principal com padding
        main_container = tk.Frame(self.root, bg='#F8F9FA')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Barra superior
        self.create_top_bar(main_container)
        
        # Frame principal (conteúdo)
        content_wrapper = tk.Frame(main_container, bg='#F8F9FA')
        content_wrapper.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Sidebar (menu lateral)
        self.create_sidebar(content_wrapper)
        
        # Frame de conteúdo principal
        self.content_frame = tk.Frame(content_wrapper, bg='white', relief=tk.RAISED, bd=0)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        self.content_frame.configure(highlightbackground='#E0E0E0', highlightthickness=1)
        
        # Mostrar dashboard inicial
        self.show_dashboard()
    
    def create_top_bar(self, parent):
        """Cria a barra superior com saudação e data"""
        top_bar = tk.Frame(parent, bg='white', height=60)
        top_bar.pack(fill=tk.X, pady=(0, 10))
        top_bar.pack_propagate(False)
        top_bar.configure(highlightbackground='#E0E0E0', highlightthickness=1)
        
        # Ícone do app
        icon_label = tk.Label(top_bar, text="✨", font=("Segoe UI", 24), bg='white')
        icon_label.pack(side=tk.LEFT, padx=(20, 10), pady=10)
        
        # Saudação personalizada
        hora = datetime.now().hour
        if hora < 12:
            saudacao = "Bom dia"
        elif hora < 18:
            saudacao = "Boa tarde"
        else:
            saudacao = "Boa noite"
        
        welcome_text = f"{saudacao}, {self.user_data['nome']}! 👋"
        self.welcome_label = tk.Label(top_bar, text=welcome_text, 
                                      font=("Segoe UI", 14, "bold"),
                                      bg='white', fg='#2C3E50')
        self.welcome_label.pack(side=tk.LEFT, padx=10)
        
        # Data e hora atual
        self.datetime_label = tk.Label(top_bar, text="", font=("Segoe UI", 11),
                                       bg='white', fg='#7F8C8D')
        self.datetime_label.pack(side=tk.RIGHT, padx=20)
        self.update_datetime()
        
        # Botão de configurações
        settings_btn = tk.Label(top_bar, text="⚙️", font=("Segoe UI", 18),
                                bg='white', fg='#7F8C8D', cursor='hand2')
        settings_btn.pack(side=tk.RIGHT, padx=10)
        settings_btn.bind('<Button-1>', lambda e: self.show_settings())
        
        # Separador
        tk.Frame(top_bar, width=1, bg='#E0E0E0').pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        # Botão de perfil
        profile_btn = tk.Label(top_bar, text="👤", font=("Segoe UI", 18),
                               bg='white', fg='#7F8C8D', cursor='hand2')
        profile_btn.pack(side=tk.RIGHT, padx=10)
        profile_btn.bind('<Button-1>', lambda e: self.edit_profile())
    
    def update_datetime(self):
        """Atualiza o relógio na barra superior"""
        now = datetime.now()
        self.datetime_label.config(text=now.strftime("%A, %d de %B de %Y - %H:%M"))
        self.root.after(1000, self.update_datetime)
    
    def create_sidebar(self, parent):
        """Cria a sidebar com navegação"""
        sidebar = tk.Frame(parent, bg='white', width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        sidebar.configure(highlightbackground='#E0E0E0', highlightthickness=1)
        
        # Avatar e informações do usuário
        avatar_frame = tk.Frame(sidebar, bg='#F8F9FA')
        avatar_frame.pack(fill=tk.X, pady=20)
        
        # Avatar
        avatar_label = tk.Label(avatar_frame, text="👤", font=("Segoe UI", 50),
                                bg='#F8F9FA', fg='#3498DB')
        avatar_label.pack(pady=(10, 5))
        
        # Nome do usuário
        tk.Label(avatar_frame, text=self.user_data["nome"], 
                font=("Segoe UI", 12, "bold"), bg='#F8F9FA', fg='#2C3E50').pack()
        
        # Cargo/status
        tk.Label(avatar_frame, text="Organizando sua vida ✨", 
                font=("Segoe UI", 9), bg='#F8F9FA', fg='#7F8C8D').pack(pady=(2, 10))
        
        # Separador
        tk.Frame(sidebar, height=2, bg='#E0E0E0').pack(fill=tk.X, padx=15, pady=10)
        
        # Menu de navegação
        menu_items = [
            ("📊 Dashboard", self.show_dashboard, "#3498DB"),
            ("📔 Diário Pessoal", self.open_diario, "#9B59B6"),
            ("✅ Lista de Tarefas", self.open_tarefas, "#E67E22"),
            ("💰 Controle Financeiro", self.open_financas, "#27AE60"),
            ("📅 Calendário", self.open_calendario, "#E74C3C"),
            ("📝 Anotações Rápidas", self.open_anotacoes, "#1ABC9C"),
        ]
        
        self.menu_buttons = {}
        for text, command, color in menu_items:
            btn_frame = tk.Frame(sidebar, bg='white')
            btn_frame.pack(fill=tk.X, padx=15, pady=3)
            
            btn = tk.Button(btn_frame, text=text, command=command,
                           font=("Segoe UI", 10, "bold"),
                           bg='white', fg='#2C3E50', 
                           relief=tk.FLAT, cursor='hand2',
                           anchor=tk.W, padx=15, pady=10)
            btn.pack(fill=tk.X)
            
            # Efeito hover
            def on_enter(e, b=btn, c=color):
                b.configure(bg=c, fg='white')
            def on_leave(e, b=btn):
                b.configure(bg='white', fg='#2C3E50')
            
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
            
            self.menu_buttons[text] = btn
        
        # Separador
        tk.Frame(sidebar, height=2, bg='#E0E0E0').pack(fill=tk.X, padx=15, pady=10)
        
        # Estatísticas rápidas
        stats_frame = tk.Frame(sidebar, bg='#F8F9FA')
        stats_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(stats_frame, text="📊 Estatísticas", font=("Segoe UI", 11, "bold"),
                bg='#F8F9FA', fg='#2C3E50').pack(anchor=tk.W, pady=(0, 10))
        
        # Contadores
        self.stats_labels = {}
        stats_items = [
            ("📝 Tarefas", len(self.tasks)),
            ("📔 Diário", len(self.diario_entries)),
            ("💰 Finanças", len(self.financas)),
        ]
        
        for text, count in stats_items:
            stat_frame = tk.Frame(stats_frame, bg='#F8F9FA')
            stat_frame.pack(fill=tk.X, pady=3)
            
            tk.Label(stat_frame, text=text, font=("Segoe UI", 9),
                    bg='#F8F9FA', fg='#7F8C8D').pack(side=tk.LEFT)
            tk.Label(stat_frame, text=str(count), font=("Segoe UI", 10, "bold"),
                    bg='#F8F9FA', fg='#3498DB').pack(side=tk.RIGHT)
            
            self.stats_labels[text] = stat_frame
        
        # Botão sair
        tk.Frame(sidebar, height=2, bg='#E0E0E0').pack(fill=tk.X, padx=15, pady=10)
        
        logout_btn = tk.Button(sidebar, text="🚪 Sair", command=self.confirm_exit,
                              font=("Segoe UI", 10, "bold"),
                              bg='#E74C3C', fg='white', 
                              relief=tk.FLAT, cursor='hand2',
                              padx=15, pady=8)
        logout_btn.pack(fill=tk.X, padx=15, pady=10)
    
    def show_dashboard(self):
        """Mostra o dashboard principal"""
        self.clear_content()
        
        # Título do dashboard
        title_frame = tk.Frame(self.content_frame, bg='white')
        title_frame.pack(fill=tk.X, padx=30, pady=30)
        
        tk.Label(title_frame, text="📊 Dashboard", font=("Segoe UI", 20, "bold"),
                bg='white', fg='#2C3E50').pack(anchor=tk.W)
        tk.Label(title_frame, text="Visão geral da sua vida organizada",
                font=("Segoe UI", 11), bg='white', fg='#7F8C8D').pack(anchor=tk.W, pady=(5, 0))
        
        # Cards de resumo
        cards_frame = tk.Frame(self.content_frame, bg='white')
        cards_frame.pack(fill=tk.X, padx=30, pady=10)
        
        # Configurar grid para cards
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)
        
        # Card de tarefas
        self.create_dashboard_card(cards_frame, 0, "✅ Tarefas", 
                                   f"{len(self.tasks)} pendentes",
                                   "Clique para ver", "#E67E22", self.open_tarefas)
        
        # Card do diário
        self.create_dashboard_card(cards_frame, 1, "📔 Diário", 
                                   f"{len(self.diario_entries)} entradas",
                                   "Escrever novo", "#9B59B6", self.open_diario)
        
        # Card financeiro
        total_receitas = sum(item["valor"] for item in self.financas if item["tipo"] == "receita")
        total_despesas = sum(item["valor"] for item in self.financas if item["tipo"] == "despesa")
        saldo = total_receitas - total_despesas
        
        self.create_dashboard_card(cards_frame, 2, "💰 Finanças", 
                                   f"R$ {saldo:,.2f}",
                                   "Ver detalhes", "#27AE60", self.open_financas)
        
        # Card de anotações
        self.create_dashboard_card(cards_frame, 3, "📝 Anotações", 
                                   f"{len(self.notas)} notas",
                                   "Criar nota", "#1ABC9C", self.open_anotacoes)
        
        # Atividades recentes
        recent_frame = tk.Frame(self.content_frame, bg='white')
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        tk.Label(recent_frame, text="📋 Atividades Recentes", font=("Segoe UI", 14, "bold"),
                bg='white', fg='#2C3E50').pack(anchor=tk.W, pady=(0, 15))
        
        # Lista de atividades recentes
        activities = self.get_recent_activities()
        
        if activities:
            for activity in activities[:5]:
                activity_frame = tk.Frame(recent_frame, bg='#F8F9FA', relief=tk.FLAT)
                activity_frame.pack(fill=tk.X, pady=3)
                activity_frame.configure(highlightbackground='#E0E0E0', highlightthickness=1)
                
                inner = tk.Frame(activity_frame, bg='#F8F9FA')
                inner.pack(fill=tk.X, padx=15, pady=10)
                
                tk.Label(inner, text=activity["icon"], font=("Segoe UI", 14),
                        bg='#F8F9FA').pack(side=tk.LEFT, padx=(0, 10))
                tk.Label(inner, text=activity["text"], font=("Segoe UI", 10),
                        bg='#F8F9FA', fg='#2C3E50').pack(side=tk.LEFT)
                tk.Label(inner, text=activity["date"], font=("Segoe UI", 9),
                        bg='#F8F9FA', fg='#7F8C8D').pack(side=tk.RIGHT)
        else:
            tk.Label(recent_frame, text="Nenhuma atividade recente", 
                    font=("Segoe UI", 11), bg='white', fg='#95A5A6').pack(pady=30)
    
    def create_dashboard_card(self, parent, col, title, value, action_text, color, command):
        """Cria um card no dashboard"""
        card = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        card.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")
        card.configure(highlightbackground='#E0E0E0', highlightthickness=1)
        
        inner = tk.Frame(card, bg='white')
        inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Ícone
        tk.Label(inner, text=title[0], font=("Segoe UI", 32), bg='white', fg=color).pack()
        
        # Título
        tk.Label(inner, text=title[2:], font=("Segoe UI", 11, "bold"),
                bg='white', fg='#2C3E50').pack(pady=(5, 0))
        
        # Valor
        tk.Label(inner, text=value, font=("Segoe UI", 16, "bold"),
                bg='white', fg=color).pack(pady=5)
        
        # Botão de ação
        action_btn = tk.Button(inner, text=action_text, command=command,
                               bg=color, fg='white', font=("Segoe UI", 9),
                               relief=tk.FLAT, cursor='hand2', padx=15, pady=5)
        action_btn.pack(pady=(10, 0))
        
        # Efeito hover
        def on_enter(e, btn=action_btn, c=color):
            btn.configure(bg=self.darken_color(c))
        def on_leave(e, btn=action_btn, c=color):
            btn.configure(bg=c)
        
        action_btn.bind('<Enter>', on_enter)
        action_btn.bind('<Leave>', on_leave)
    
    def darken_color(self, color):
        """Escurece uma cor hex"""
        # Simplificado para efeito hover
        colors = {
            "#E67E22": "#D35400",
            "#9B59B6": "#8E44AD",
            "#27AE60": "#229954",
            "#1ABC9C": "#17A589",
            "#3498DB": "#2980B9"
        }
        return colors.get(color, color)
    
    def get_recent_activities(self):
        """Retorna atividades recentes"""
        activities = []
        
        # Adicionar últimas tarefas
        for task in self.tasks[-3:]:
            activities.append({
                "icon": "✅",
                "text": f"Tarefa: {task.get('titulo', 'Sem título')}",
                "date": task.get('data_criacao', 'Data não informada')
            })
        
        # Adicionar últimas entradas do diário
        for entry in self.diario_entries[-3:]:
            activities.append({
                "icon": "📔",
                "text": f"Diário: {entry.get('titulo', 'Nova entrada')[:30]}",
                "date": entry.get('data_formatada', 'Data não informada')
            })
        
        # Adicionar últimas transações
        for trans in self.financas[-3:]:
            icon = "💰" if trans.get('tipo') == 'receita' else "💸"
            activities.append({
                "icon": icon,
                "text": f"{trans.get('descricao', 'Transação')} - R$ {trans.get('valor', 0):,.2f}",
                "date": trans.get('data', 'Data não informada')
            })
        
        # Ordenar por data (simplificado)
        return sorted(activities, key=lambda x: x['date'], reverse=True)
    
    def edit_profile(self, event=None):
        self.perfil_manager.edit_profile()
        # Atualizar nome na sidebar
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children():
                pass  # Recarregar dashboard se necessário
    
    def update_profile_display(self):
        """Atualiza as informações do perfil na interface"""
        # Atualizar saudação
        hora = datetime.now().hour
        if hora < 12:
            saudacao = "Bom dia"
        elif hora < 18:
            saudacao = "Boa tarde"
        else:
            saudacao = "Boa noite"
        
        self.welcome_label.config(text=f"{saudacao}, {self.user_data['nome']}! 👋")
        
        # Recarregar dashboard se estiver visível
        if hasattr(self, 'content_frame'):
            # Verificar se está no dashboard
            pass
    
    def open_diario(self):
        self.diario_manager.open_diario()
        self.update_stats()
    
    def open_tarefas(self):
        self.tarefas_manager.open_tarefas()
        self.update_stats()
    
    def open_financas(self):
        self.financas_manager.open_financas()
        self.update_stats()
    
    def open_calendario(self):
        self.calendario_manager.open_calendario()
    
    def open_anotacoes(self):
        self.anotacoes_manager.open_anotacoes()
        self.update_stats()
    
    def update_stats(self):
        """Atualiza as estatísticas na sidebar"""
        if hasattr(self, 'stats_labels'):
            # Recriar stats
            for widget in self.content_frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    pass  # Refresh stats
    
    def show_settings(self):
        """Mostra janela de configurações"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Configurações")
        settings_window.geometry("400x300")
        settings_window.configure(bg='white')
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Centralizar
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (settings_window.winfo_screenheight() // 2) - (300 // 2)
        settings_window.geometry(f"400x300+{x}+{y}")
        
        main_frame = tk.Frame(settings_window, bg='white', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="⚙️ Configurações", font=("Segoe UI", 16, "bold"),
                bg='white', fg='#2C3E50').pack(pady=(0, 20))
        
        # Tema (placeholder)
        tk.Label(main_frame, text="Tema:", bg='white', font=("Segoe UI", 10)).pack(anchor=tk.W)
        theme_var = tk.StringVar(value="Claro")
        theme_combo = ttk.Combobox(main_frame, textvariable=theme_var, 
                                   values=["Claro", "Escuro"], state="readonly")
        theme_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Backup
        backup_btn = tk.Button(main_frame, text="💾 Fazer Backup dos Dados",
                               command=self.backup_data,
                               bg='#3498DB', fg='white', font=("Segoe UI", 10),
                               relief=tk.FLAT, cursor='hand2', pady=8)
        backup_btn.pack(fill=tk.X, pady=5)
        
        # Fechar
        close_btn = tk.Button(main_frame, text="Fechar", command=settings_window.destroy,
                              bg='#95A5A6', fg='white', font=("Segoe UI", 10),
                              relief=tk.FLAT, cursor='hand2', pady=8)
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
                "notas": self.notas
            }
            with open(backup_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Backup", f"Backup criado com sucesso!\nArquivo: {backup_file}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar backup: {str(e)}")
    
    def confirm_exit(self):
        """Confirma saída do aplicativo"""
        if messagebox.askyesno("Sair", "Tem certeza que deseja sair?"):
            self.save_data()
            self.root.quit()
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
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
            with open("personal_app_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
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
                print(f"Erro ao carregar dados: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalApp(root)
    root.mainloop()