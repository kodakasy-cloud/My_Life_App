import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

from window.perfil import PerfilManager
from window.diario import DiarioManager
from window.tarefa import TarefasManager
from window.financas import FinancasManager
from window.calendario import CalendarioManager
from window.anotacoes import AnotacoesManager


class PersonalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meu Painel Pessoal")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        
        # Dados do usuário
        self.user_data = {
            "nome": "Usuário",
            "idade": "",
            "foto_path": None
        }
        
        # Dados do diário
        self.diario_entries = []
        
        # Dados das tarefas
        self.tasks = []
        
        # Dados financeiros
        self.financas = []
        
        # Anotações
        self.notas = []
        
        self.load_data()
        self.create_widgets()
        
        # Inicializar managers
        self.perfil_manager = PerfilManager(self)
        self.diario_manager = DiarioManager(self)
        self.tarefas_manager = TarefasManager(self)
        self.financas_manager = FinancasManager(self)
        self.calendario_manager = CalendarioManager(self)
        self.anotacoes_manager = AnotacoesManager(self)
        
    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Frame do perfil (lado esquerdo)
        profile_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        profile_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        
        # Ícone de perfil
        self.profile_icon = tk.Label(profile_frame, text="👤", font=("Arial", 80), bg='white')
        self.profile_icon.pack(pady=20)
        self.profile_icon.bind("<Button-1>", self.edit_profile)
        
        # Informações do perfil
        self.profile_name = tk.Label(profile_frame, text=self.user_data["nome"], font=("Arial", 14, "bold"), bg='white')
        self.profile_name.pack()
        
        self.profile_age = tk.Label(profile_frame, text=f"Idade: {self.user_data['idade'] if self.user_data['idade'] else 'Não informada'}", 
                                    font=("Arial", 10), bg='white')
        self.profile_age.pack()
        
        # Botão editar perfil
        edit_btn = tk.Button(profile_frame, text="Editar Perfil", command=self.edit_profile, 
                            bg='#4CAF50', fg='white', font=("Arial", 10))
        edit_btn.pack(pady=10)
        
        # Frame dos botões principais
        buttons_frame = tk.Frame(profile_frame, bg='white')
        buttons_frame.pack(pady=20)
        
        # Botões das funcionalidades
        buttons = [
            ("📔 Diário", self.open_diario),
            ("✅ Tarefas", self.open_tarefas),
            ("💰 Finanças", self.open_financas),
            ("📅 Calendário", self.open_calendario),
            ("📝 Anotações", self.open_anotacoes)
        ]
        
        for text, command in buttons:
            btn = tk.Button(buttons_frame, text=text, command=command, 
                          width=15, height=2, font=("Arial", 11),
                          bg='#2196F3', fg='white', relief=tk.RAISED)
            btn.pack(pady=5)
        
        # Frame de conteúdo (lado direito)
        self.content_frame = tk.Frame(main_frame, bg='white', relief=tk.SUNKEN, bd=2)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Label de boas-vindas
        welcome_label = tk.Label(self.content_frame, text=f"Bem-vindo(a), {self.user_data['nome']}!", 
                                font=("Arial", 18, "bold"), bg='white', fg='#333')
        welcome_label.pack(pady=50)
        
        info_label = tk.Label(self.content_frame, text="Selecione uma das opções ao lado para começar", 
                             font=("Arial", 12), bg='white', fg='#666')
        info_label.pack()
        
    def edit_profile(self, event=None):
        self.perfil_manager.edit_profile()
        
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
        
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def save_data(self):
        data = {
            "user_data": self.user_data,
            "diario_entries": self.diario_entries,
            "tasks": self.tasks,
            "financas": self.financas,
            "notas": self.notas
        }
        with open("personal_app_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
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
            except:
                pass