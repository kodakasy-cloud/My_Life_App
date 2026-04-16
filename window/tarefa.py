import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser
from datetime import datetime
import json
import os
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

# ==================== MODELOS ====================

class Prioridade(Enum):
    BAIXA = ("🟢 Baixa", "#4CAF50")
    MEDIA = ("🟡 Média", "#FFC107")
    ALTA = ("🔴 Alta", "#F44336")
    URGENTE = ("⚡ Urgente", "#9C27B0")
    
    def __init__(self, display: str, cor: str):
        self.display = display
        self.cor = cor

class Categoria(Enum):
    PESSOAL = ("👤 Pessoal", "#2196F3")
    TRABALHO = ("💼 Trabalho", "#FF9800")
    ESTUDOS = ("📚 Estudos", "#9C27B0")
    SAUDE = ("🏃 Saúde", "#4CAF50")
    FINANCAS = ("💰 Finanças", "#F44336")
    OUTROS = ("📦 Outros", "#757575")
    
    def __init__(self, display: str, cor: str):
        self.display = display
        self.cor = cor

@dataclass
class Tarefa:
    id: int
    texto: str
    concluida: bool
    data_criacao: str
    data_vencimento: Optional[str]
    prioridade: str
    categoria: str
    descricao: str
    subtarefas: List[Dict]
    anexos: List[str]
    tags: List[str]
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "texto": self.texto,
            "concluida": self.concluida,
            "data_criacao": self.data_criacao,
            "data_vencimento": self.data_vencimento,
            "prioridade": self.prioridade,
            "categoria": self.categoria,
            "descricao": self.descricao,
            "subtarefas": self.subtarefas,
            "anexos": self.anexos,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id", 0),
            texto=data.get("texto", ""),
            concluida=data.get("concluida", False),
            data_criacao=data.get("data_criacao", ""),
            data_vencimento=data.get("data_vencimento"),
            prioridade=data.get("prioridade", Prioridade.MEDIA.name),
            categoria=data.get("categoria", Categoria.OUTROS.name),
            descricao=data.get("descricao", ""),
            subtarefas=data.get("subtarefas", []),
            anexos=data.get("anexos", []),
            tags=data.get("tags", [])
        )

# ==================== COMPONENTES PERSONALIZADOS ====================

class TarefaWidget(tk.Frame):
    """Widget visual para exibir uma tarefa com design moderno"""
    
    def __init__(self, parent, tarefa: Tarefa, on_toggle, on_delete, on_edit, master=None):
        super().__init__(parent, bg='white', bd=1, relief=tk.RAISED)
        self.tarefa = tarefa
        self.on_toggle = on_toggle
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.master = master
        
        self.configure_style()
        self.create_widgets()
        self.bind_events()
    
    def configure_style(self):
        self.configure(highlightthickness=1, highlightbackground='#E0E0E0')
        
    def create_widgets(self):
        # Frame principal horizontal
        main_frame = tk.Frame(self, bg='white')
        main_frame.pack(fill=tk.X, padx=10, pady=8)
        
        # Checkbox
        self.var = tk.BooleanVar(value=self.tarefa.concluida)
        cb = tk.Checkbutton(main_frame, variable=self.var, bg='white',
                           command=self.toggle_task, cursor="hand2")
        cb.pack(side=tk.LEFT, padx=(0, 10))
        
        # Frame do conteúdo
        content_frame = tk.Frame(main_frame, bg='white')
        content_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Título da tarefa
        task_text = self.tarefa.texto
        if self.tarefa.concluida:
            task_text = f"✓ {task_text}"
            
        self.title_label = tk.Label(content_frame, text=task_text, 
                                    font=("Segoe UI", 11, "bold" if not self.tarefa.concluida else "normal"),
                                    bg='white', fg='#666' if self.tarefa.concluida else '#333',
                                    anchor='w', cursor="hand2")
        self.title_label.pack(anchor='w')
        self.title_label.bind('<Button-1>', lambda e: self.edit_task())
        
        # Frame de metadados
        meta_frame = tk.Frame(content_frame, bg='white')
        meta_frame.pack(anchor='w', pady=(5, 0))
        
        # Prioridade badge
        prioridade = Prioridade[self.tarefa.prioridade] if self.tarefa.prioridade in Prioridade.__members__ else Prioridade.MEDIA
        priority_badge = tk.Label(meta_frame, text=prioridade.display, 
                                  bg=prioridade.cor, fg='white',
                                  font=("Segoe UI", 8, "bold"),
                                  padx=6, pady=2)
        priority_badge.pack(side=tk.LEFT, padx=(0, 8))
        
        # Categoria badge
        categoria = Categoria[self.tarefa.categoria] if self.tarefa.categoria in Categoria.__members__ else Categoria.OUTROS
        cat_badge = tk.Label(meta_frame, text=categoria.display,
                            bg=categoria.cor, fg='white',
                            font=("Segoe UI", 8, "bold"),
                            padx=6, pady=2)
        cat_badge.pack(side=tk.LEFT, padx=(0, 8))
        
        # Data de criação
        tk.Label(meta_frame, text=f"📅 {self.tarefa.data_criacao}",
                font=("Segoe UI", 8), bg='white', fg='#999').pack(side=tk.LEFT, padx=(0, 8))
        
        # Data de vencimento
        if self.tarefa.data_vencimento:
            vencimento_label = tk.Label(meta_frame, text=f"⏰ {self.tarefa.data_vencimento}",
                                       font=("Segoe UI", 8), bg='white', fg='#FF6B6B')
            vencimento_label.pack(side=tk.LEFT, padx=(0, 8))
        
        # Tags
        for tag in self.tarefa.tags[:2]:  # Mostra até 2 tags
            tag_label = tk.Label(meta_frame, text=f"#{tag}",
                                font=("Segoe UI", 8), bg='#F0F0F0', fg='#666',
                                padx=4, pady=2)
            tag_label.pack(side=tk.LEFT, padx=(0, 4))
        
        # Botões de ação
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        edit_btn = tk.Button(btn_frame, text="✏️", command=self.edit_task,
                            bg='white', fg='#2196F3', font=("Segoe UI", 9),
                            cursor="hand2", bd=0)
        edit_btn.pack(side=tk.LEFT, padx=4)
        
        delete_btn = tk.Button(btn_frame, text="🗑️", command=self.delete_task,
                              bg='white', fg='#F44336', font=("Segoe UI", 9),
                              cursor="hand2", bd=0)
        delete_btn.pack(side=tk.LEFT, padx=4)
        
        # Descrição (se existir)
        if self.tarefa.descricao:
            desc_frame = tk.Frame(self, bg='#F9F9F9')
            desc_frame.pack(fill=tk.X, padx=10, pady=(0, 8))
            
            tk.Label(desc_frame, text="📝 " + self.tarefa.descricao[:100],
                    font=("Segoe UI", 9), bg='#F9F9F9', fg='#666',
                    wraplength=500, justify=tk.LEFT).pack(anchor='w', padx=15)
        
        # Subtarefas
        if self.tarefa.subtarefas:
            sub_frame = tk.Frame(self, bg='#F5F5F5')
            sub_frame.pack(fill=tk.X, padx=10, pady=(0, 8))
            
            for sub in self.tarefa.subtarefas[:2]:
                status = "✓" if sub.get("concluida", False) else "○"
                tk.Label(sub_frame, text=f"  {status} {sub.get('texto', '')[:50]}",
                        font=("Segoe UI", 8), bg='#F5F5F5', fg='#888').pack(anchor='w', padx=15)
    
    def toggle_task(self):
        self.on_toggle(self.tarefa.id)
    
    def delete_task(self):
        self.on_delete(self.tarefa.id)
    
    def edit_task(self):
        self.on_edit(self.tarefa)
    
    def bind_events(self):
        self.title_label.bind('<Enter>', lambda e: self.title_label.configure(fg='#2196F3'))
        self.title_label.bind('<Leave>', lambda e: self.title_label.configure(fg='#666' if self.tarefa.concluida else '#333'))

# ==================== DIALOGOS MODERNOS ====================

class TarefaDialog(tk.Toplevel):
    """Diálogo moderno para criar/editar tarefas"""
    
    def __init__(self, parent, titulo: str, tarefa: Optional[Tarefa] = None):
        super().__init__(parent)
        self.tarefa = tarefa
        self.resultado = None
        
        self.title(titulo)
        self.geometry("600x700")
        self.configure(bg='white')
        self.resizable(False, False)
        
        # Centralizar
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        # Canvas para scroll
        canvas = tk.Canvas(self, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título
        tk.Label(scrollable_frame, text="📝 Detalhes da Tarefa", 
                font=("Segoe UI", 16, "bold"), bg='white', fg='#333').pack(pady=20)
        
        # Frame do formulário
        form = tk.Frame(scrollable_frame, bg='white')
        form.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        # Título da tarefa
        tk.Label(form, text="Título da Tarefa *", font=("Segoe UI", 10, "bold"),
                bg='white', fg='#555').pack(anchor='w', pady=(10, 5))
        self.txt_titulo = tk.Text(form, height=2, font=("Segoe UI", 11), wrap=tk.WORD)
        self.txt_titulo.pack(fill=tk.X, pady=(0, 10))
        
        # Descrição
        tk.Label(form, text="Descrição", font=("Segoe UI", 10, "bold"),
                bg='white', fg='#555').pack(anchor='w', pady=(10, 5))
        self.txt_descricao = tk.Text(form, height=4, font=("Segoe UI", 10), wrap=tk.WORD)
        self.txt_descricao.pack(fill=tk.X, pady=(0, 10))
        
        # Frame de duas colunas
        cols_frame = tk.Frame(form, bg='white')
        cols_frame.pack(fill=tk.X, pady=10)
        
        # Coluna esquerda
        left_col = tk.Frame(cols_frame, bg='white')
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Prioridade
        tk.Label(left_col, text="Prioridade", font=("Segoe UI", 10, "bold"),
                bg='white', fg='#555').pack(anchor='w')
        self.prioridade_var = tk.StringVar(value=Prioridade.MEDIA.name)
        prioridades_frame = tk.Frame(left_col, bg='white')
        prioridades_frame.pack(fill=tk.X, pady=5)
        for p in Prioridade:
            rb = tk.Radiobutton(prioridades_frame, text=p.display, variable=self.prioridade_var,
                               value=p.name, bg='white', font=("Segoe UI", 9), cursor="hand2")
            rb.pack(side=tk.LEFT, padx=5)
        
        # Categoria
        tk.Label(left_col, text="Categoria", font=("Segoe UI", 10, "bold"),
                bg='white', fg='#555').pack(anchor='w', pady=(10, 5))
        self.categoria_var = tk.StringVar(value=Categoria.PESSOAL.name)
        categoria_combo = tk.OptionMenu(left_col, self.categoria_var, *[c.name for c in Categoria])
        categoria_combo.configure(bg='white', font=("Segoe UI", 9))
        categoria_combo.pack(fill=tk.X)
        
        # Coluna direita
        right_col = tk.Frame(cols_frame, bg='white')
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Data de vencimento
        tk.Label(right_col, text="Data de Vencimento", font=("Segoe UI", 10, "bold"),
                bg='white', fg='#555').pack(anchor='w')
        self.data_vencimento = tk.Entry(right_col, font=("Segoe UI", 10))
        self.data_vencimento.pack(fill=tk.X, pady=5)
        self.data_vencimento.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        # Tags
        tk.Label(right_col, text="Tags (separadas por vírgula)", font=("Segoe UI", 10, "bold"),
                bg='white', fg='#555').pack(anchor='w', pady=(10, 5))
        self.tags_entry = tk.Entry(right_col, font=("Segoe UI", 10))
        self.tags_entry.pack(fill=tk.X)
        
        # Subtarefas
        tk.Label(form, text="Subtarefas (uma por linha)", font=("Segoe UI", 10, "bold"),
                bg='white', fg='#555').pack(anchor='w', pady=(15, 5))
        self.subtarefas_text = tk.Text(form, height=4, font=("Segoe UI", 10))
        self.subtarefas_text.pack(fill=tk.X, pady=(0, 10))
        
        # Botões
        btn_frame = tk.Frame(form, bg='white')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="💾 Salvar", command=self.save,
                 bg='#4CAF50', fg='white', font=("Segoe UI", 11, "bold"),
                 padx=30, pady=8, cursor="hand2").pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="❌ Cancelar", command=self.destroy,
                 bg='#F44336', fg='white', font=("Segoe UI", 11, "bold"),
                 padx=30, pady=8, cursor="hand2").pack(side=tk.LEFT, padx=10)
    
    def load_data(self):
        if self.tarefa:
            self.txt_titulo.insert("1.0", self.tarefa.texto)
            self.txt_descricao.insert("1.0", self.tarefa.descricao)
            self.prioridade_var.set(self.tarefa.prioridade)
            self.categoria_var.set(self.tarefa.categoria)
            if self.tarefa.data_vencimento:
                self.data_vencimento.delete(0, tk.END)
                self.data_vencimento.insert(0, self.tarefa.data_vencimento)
            self.tags_entry.insert(0, ", ".join(self.tarefa.tags))
            subtarefas_text = "\n".join([f"{'✓ ' if sub.get('concluida') else '○ '}{sub.get('texto')}" 
                                        for sub in self.tarefa.subtarefas])
            self.subtarefas_text.insert("1.0", subtarefas_text)
    
    def save(self):
        titulo = self.txt_titulo.get("1.0", tk.END).strip()
        if not titulo:
            messagebox.showwarning("Aviso", "Por favor, insira um título para a tarefa!")
            return
        
        # Processar subtarefas
        subtarefas = []
        for linha in self.subtarefas_text.get("1.0", tk.END).strip().split('\n'):
            if linha.strip():
                concluida = linha.strip().startswith('✓')
                texto = linha.strip()[2:] if linha.strip()[0] in '✓○' else linha.strip()
                subtarefas.append({"texto": texto, "concluida": concluida})
        
        # Processar tags
        tags = [tag.strip() for tag in self.tags_entry.get().split(',') if tag.strip()]
        
        self.resultado = {
            "id": self.tarefa.id if self.tarefa else None,
            "texto": titulo,
            "descricao": self.txt_descricao.get("1.0", tk.END).strip(),
            "prioridade": self.prioridade_var.get(),
            "categoria": self.categoria_var.get(),
            "data_vencimento": self.data_vencimento.get().strip(),
            "tags": tags,
            "subtarefas": subtarefas
        }
        
        self.destroy()

# ==================== GERENCIADOR PRINCIPAL ====================

class TarefasManager:
    def __init__(self, app):
        self.app = app
        self.current_filter = "TODAS"
        self.search_term = ""
        
    def open_tarefas(self):
        self.app.clear_content()
        
        # Cabeçalho
        header_frame = tk.Frame(self.app.content_frame, bg='white')
        header_frame.pack(fill=tk.X, pady=20, padx=30)
        
        tk.Label(header_frame, text="📋 Gerenciador de Tarefas", 
                font=("Segoe UI", 24, "bold"), bg='white', fg='#333').pack(anchor='w')
        
        tk.Label(header_frame, text="Organize suas tarefas de forma eficiente",
                font=("Segoe UI", 11), bg='white', fg='#777').pack(anchor='w', pady=(5, 0))
        
        # Barra de ferramentas
        toolbar = tk.Frame(self.app.content_frame, bg='white', bd=1, relief=tk.FLAT)
        toolbar.pack(fill=tk.X, pady=20, padx=30)
        
        # Botão adicionar
        add_btn = tk.Button(toolbar, text="➕ Nova Tarefa", command=self.add_task,
                           bg='#4CAF50', fg='white', font=("Segoe UI", 10, "bold"),
                           padx=15, pady=8, cursor="hand2")
        add_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Barra de pesquisa
        search_frame = tk.Frame(toolbar, bg='white', bd=1, relief=tk.SUNKEN)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 20))
        
        tk.Label(search_frame, text="🔍", bg='white', font=("Segoe UI", 12)).pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, font=("Segoe UI", 11), bg='white', bd=0)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        # Filtros
        filter_frame = tk.Frame(self.app.content_frame, bg='white')
        filter_frame.pack(fill=tk.X, pady=(0, 20), padx=30)
        
        filters = [
            ("📋 Todas", "TODAS"),
            ("✅ Pendentes", "PENDENTES"),
            ("✓ Concluídas", "CONCLUIDAS"),
            ("⭐ Prioritárias", "PRIORITARIAS"),
            ("📅 Vencendo", "VENCENDO")
        ]
        
        for text, filter_type in filters:
            btn = tk.Button(filter_frame, text=text, command=lambda f=filter_type: self.apply_filter(f),
                          bg='#F0F0F0', fg='#333', font=("Segoe UI", 9),
                          padx=12, pady=5, cursor="hand2")
            btn.pack(side=tk.LEFT, padx=5)
        
        # Estatísticas
        stats_frame = tk.Frame(self.app.content_frame, bg='#F9F9F9', bd=1, relief=tk.FLAT)
        stats_frame.pack(fill=tk.X, pady=(0, 20), padx=30)
        
        self.stats_labels = {}
        stats = ["total", "pendentes", "concluidas", "prioritarias"]
        for i, stat in enumerate(stats):
            frame = tk.Frame(stats_frame, bg='#F9F9F9')
            frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)
            
            tk.Label(frame, text="0", font=("Segoe UI", 20, "bold"),
                    bg='#F9F9F9', fg='#333').pack()
            tk.Label(frame, text=stat.upper(), font=("Segoe UI", 9),
                    bg='#F9F9F9', fg='#777').pack()
            self.stats_labels[stat] = frame.winfo_children()[0]
        
        # Lista de tarefas (scrollable)
        tasks_container = tk.Frame(self.app.content_frame, bg='white')
        tasks_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        self.tasks_canvas = tk.Canvas(tasks_container, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(tasks_container, orient="vertical", command=self.tasks_canvas.yview)
        self.tasks_frame = tk.Frame(self.tasks_canvas, bg='white')
        
        self.tasks_frame.bind(
            "<Configure>",
            lambda e: self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))
        )
        
        self.tasks_canvas.create_window((0, 0), window=self.tasks_frame, anchor="nw")
        self.tasks_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.tasks_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Atualizar exibição
        self.update_tasks_display()
    
    def on_search(self, event=None):
        self.search_term = self.search_entry.get().lower()
        self.update_tasks_display()
    
    def apply_filter(self, filter_type):
        self.current_filter = filter_type
        self.update_tasks_display()
    
    def get_filtered_tasks(self):
        tasks = self.app.tasks.copy()
        
        # Aplicar filtro de status
        if self.current_filter == "PENDENTES":
            tasks = [t for t in tasks if not t["concluida"]]
        elif self.current_filter == "CONCLUIDAS":
            tasks = [t for t in tasks if t["concluida"]]
        elif self.current_filter == "PRIORITARIAS":
            tasks = [t for t in tasks if t.get("prioridade", "MEDIA") in ["ALTA", "URGENTE"]]
        elif self.current_filter == "VENCENDO":
            hoje = datetime.now().strftime("%d/%m/%Y")
            tasks = [t for t in tasks if t.get("data_vencimento") and t.get("data_vencimento") >= hoje and not t["concluida"]]
        
        # Aplicar pesquisa
        if self.search_term:
            tasks = [t for t in tasks if 
                    self.search_term in t["texto"].lower() or
                    self.search_term in t.get("descricao", "").lower() or
                    any(self.search_term in tag.lower() for tag in t.get("tags", []))]
        
        # Ordenar: não concluídas primeiro, depois por prioridade
        prioridade_order = {"URGENTE": 0, "ALTA": 1, "MEDIA": 2, "BAIXA": 3}
        tasks.sort(key=lambda t: (t["concluida"], prioridade_order.get(t.get("prioridade", "MEDIA"), 2)))
        
        return tasks
    
    def update_tasks_display(self):
        # Limpar frame
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        
        # Obter tarefas filtradas
        filtered_tasks = self.get_filtered_tasks()
        
        # Atualizar estatísticas
        total = len(self.app.tasks)
        pendentes = len([t for t in self.app.tasks if not t["concluida"]])
        concluidas = len([t for t in self.app.tasks if t["concluida"]])
        prioritarias = len([t for t in self.app.tasks if t.get("prioridade", "MEDIA") in ["ALTA", "URGENTE"]])
        
        self.stats_labels["total"].configure(text=str(total))
        self.stats_labels["pendentes"].configure(text=str(pendentes))
        self.stats_labels["concluidas"].configure(text=str(concluidas))
        self.stats_labels["prioritarias"].configure(text=str(prioritarias))
        
        # Mensagem se não houver tarefas
        if not filtered_tasks:
            msg_frame = tk.Frame(self.tasks_frame, bg='white')
            msg_frame.pack(fill=tk.BOTH, expand=True, pady=50)
            
            tk.Label(msg_frame, text="🎉 Nenhuma tarefa encontrada!",
                    font=("Segoe UI", 16), bg='white', fg='#999').pack()
            tk.Label(msg_frame, text="Clique em 'Nova Tarefa' para começar",
                    font=("Segoe UI", 11), bg='white', fg='#BBB').pack(pady=10)
            return
        
        # Criar widgets para cada tarefa
        for tarefa_dict in filtered_tasks:
            tarefa = Tarefa.from_dict(tarefa_dict)
            widget = TarefaWidget(self.tasks_frame, tarefa,
                                 self.toggle_task, self.delete_task, self.edit_task)
            widget.pack(fill=tk.X, pady=5)
    
    def add_task(self):
        dialog = TarefaDialog(self.app.root, "➕ Nova Tarefa")
        self.app.root.wait_window(dialog)
        
        if dialog.resultado:
            nova_tarefa = Tarefa(
                id=self.get_next_id(),
                texto=dialog.resultado["texto"],
                concluida=False,
                data_criacao=datetime.now().strftime("%d/%m/%Y"),
                data_vencimento=dialog.resultado["data_vencimento"],
                prioridade=dialog.resultado["prioridade"],
                categoria=dialog.resultado["categoria"],
                descricao=dialog.resultado["descricao"],
                subtarefas=dialog.resultado["subtarefas"],
                anexos=[],
                tags=dialog.resultado["tags"]
            )
            self.app.tasks.append(nova_tarefa.to_dict())
            self.app.save_data()
            self.update_tasks_display()
    
    def edit_task(self, tarefa: Tarefa):
        dialog = TarefaDialog(self.app.root, "✏️ Editar Tarefa", tarefa)
        self.app.root.wait_window(dialog)
        
        if dialog.resultado:
            # Encontrar e atualizar a tarefa
            for i, t in enumerate(self.app.tasks):
                if t["id"] == tarefa.id:
                    self.app.tasks[i].update({
                        "texto": dialog.resultado["texto"],
                        "descricao": dialog.resultado["descricao"],
                        "prioridade": dialog.resultado["prioridade"],
                        "categoria": dialog.resultado["categoria"],
                        "data_vencimento": dialog.resultado["data_vencimento"],
                        "tags": dialog.resultado["tags"],
                        "subtarefas": dialog.resultado["subtarefas"]
                    })
                    break
            
            self.app.save_data()
            self.update_tasks_display()
    
    def toggle_task(self, task_id: int):
        for task in self.app.tasks:
            if task["id"] == task_id:
                task["concluida"] = not task["concluida"]
                break
        self.app.save_data()
        self.update_tasks_display()
    
    def delete_task(self, task_id: int):
        if messagebox.askyesno("Confirmar", "Deseja excluir esta tarefa?"):
            self.app.tasks = [t for t in self.app.tasks if t["id"] != task_id]
            self.app.save_data()
            self.update_tasks_display()
    
    def get_next_id(self) -> int:
        if not self.app.tasks:
            return 1
        return max(t["id"] for t in self.app.tasks) + 1