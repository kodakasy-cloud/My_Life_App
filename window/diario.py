import logging
import tkinter as tk
from tkinter import messagebox, font as tkfont
from datetime import datetime
import json


class DiarioManager:
    def __init__(self, app):
        self.app = app
        self.current_entry = None
        self.search_term = ""
        self.filter_type = "all"  # all, recent, week, month
        self.selected_mood = None
        self.moods = {
            "😊": "Feliz",
            "😢": "Triste",
            "🤔": "Pensativo",
            "😌": "Calmo",
            "🤩": "Empolgado",
            "😤": "Estressado",
            "🥰": "Apaixonado",
            "😴": "Cansado"
        }
        
    def open_diario(self):
        self.app.clear_content()
        
        # Container principal
        main_container = tk.Frame(self.app.content_frame, bg='white')
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Título
        title_frame = tk.Frame(main_container, bg='white')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(title_frame, text="📔", font=("Segoe UI", 32), 
                bg='white').pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(title_frame, text="Meu Diário Pessoal", font=("Segoe UI", 24, "bold"), 
                bg='white', fg='#2C3E50').pack(side=tk.LEFT)
        
        # Barra de ferramentas
        toolbar = tk.Frame(main_container, bg='white')
        toolbar.pack(fill=tk.X, pady=(0, 15))
        
        # Filtros
        filter_frame = tk.Frame(toolbar, bg='white')
        filter_frame.pack(side=tk.LEFT)
        
        tk.Label(filter_frame, text="Filtrar:", bg='white', font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 5))
        
        filters = [
            ("Todas", "all"),
            ("Últimos 7 dias", "week"),
            ("Último mês", "month"),
            ("Recentes", "recent")
        ]
        
        for text, f_type in filters:
            btn = tk.Button(filter_frame, text=text, 
                          command=lambda t=f_type: self.set_filter(t),
                          bg='#ECF0F1' if self.filter_type == f_type else 'white',
                          fg='#2C3E50', font=("Segoe UI", 9),
                          relief=tk.FLAT, cursor='hand2', padx=10, pady=3)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Campo de busca
        search_frame = tk.Frame(toolbar, bg='white')
        search_frame.pack(side=tk.RIGHT)
        
        tk.Label(search_frame, text="🔍", bg='white', font=("Segoe UI", 11)).pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, font=("Segoe UI", 10), width=25,
                                     bg='#F8F9FA', relief=tk.FLAT, highlightthickness=1,
                                     highlightcolor='#3498DB', highlightbackground='#D0D0D0')
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        clear_btn = tk.Button(search_frame, text="✖", command=self.clear_search,
                             bg='white', fg='#95A5A6', font=("Segoe UI", 9),
                             relief=tk.FLAT, cursor='hand2')
        clear_btn.pack(side=tk.LEFT)
        
        # Estatísticas
        stats_frame = tk.Frame(main_container, bg='#F8F9FA', relief=tk.RAISED, bd=1)
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        stats_frame.configure(highlightbackground='#E0E0E0', highlightthickness=1)
        
        stats_inner = tk.Frame(stats_frame, bg='#F8F9FA')
        stats_inner.pack(fill=tk.X, padx=15, pady=10)
        
        self.stats_labels = {}
        stats_texts = [
            ("📝", "Total de entradas", "total_entries", "0"),
            ("📅", "Este mês", "month_entries", "0"),
            ("🔥", "Sequência atual", "streak", "0 dias"),
            ("🏆", "Melhor sequência", "best_streak", "0 dias")
        ]
        
        for i, (icon, text, key, default) in enumerate(stats_texts):
            stat_card = tk.Frame(stats_inner, bg='white', relief=tk.RAISED, bd=1)
            stat_card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
            stat_card.configure(highlightbackground='#E0E0E0', highlightthickness=1)
            
            card_inner = tk.Frame(stat_card, bg='white')
            card_inner.pack(fill=tk.BOTH, padx=10, pady=10)
            
            tk.Label(card_inner, text=icon, font=("Segoe UI", 20), bg='white').pack()
            tk.Label(card_inner, text=text, font=("Segoe UI", 9), bg='white', 
                    fg='#7F8C8D').pack()
            self.stats_labels[key] = tk.Label(card_inner, text=default, 
                                             font=("Segoe UI", 14, "bold"), 
                                             bg='white', fg='#2C3E50')
            self.stats_labels[key].pack()
        
        # Frame principal (entrada + lista)
        content_frame = tk.Frame(main_container, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Coluna esquerda - Nova entrada
        left_column = tk.Frame(content_frame, bg='white')
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # Card de nova entrada
        new_entry_card = tk.Frame(left_column, bg='white', relief=tk.RAISED, bd=1)
        new_entry_card.pack(fill=tk.BOTH, expand=True)
        new_entry_card.configure(highlightbackground='#E0E0E0', highlightthickness=1)
        
        card_inner = tk.Frame(new_entry_card, bg='white')
        card_inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(card_inner, text="✍️ Escrever no Diário", font=("Segoe UI", 14, "bold"), 
                bg='white', fg='#2C3E50').pack(anchor=tk.W, pady=(0, 15))
        
        # Seleção de humor
        mood_frame = tk.Frame(card_inner, bg='white')
        mood_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(mood_frame, text="Como você está se sentindo?", font=("Segoe UI", 10), 
                bg='white', fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        
        self.mood_buttons = {}
        mood_btn_frame = tk.Frame(mood_frame, bg='white')
        mood_btn_frame.pack()
        
        for mood_icon, mood_text in self.moods.items():
            btn = tk.Button(mood_btn_frame, text=mood_icon, command=lambda m=mood_icon: self.select_mood(m),
                           font=("Segoe UI", 16), bg='#F8F9FA', fg='#2C3E50',
                           relief=tk.FLAT, width=4, height=1, cursor='hand2')
            btn.pack(side=tk.LEFT, padx=3)
            self.mood_buttons[mood_icon] = btn
        
        # Título da entrada
        tk.Label(card_inner, text="Título (opcional):", font=("Segoe UI", 10), 
                bg='white', fg='#7F8C8D').pack(anchor=tk.W, pady=(10, 5))
        
        self.title_entry = tk.Entry(card_inner, font=("Segoe UI", 11, "bold"),
                                    bg='#F8F9FA', relief=tk.FLAT, highlightthickness=1,
                                    highlightcolor='#3498DB', highlightbackground='#D0D0D0')
        self.title_entry.pack(fill=tk.X, pady=(0, 10), ipady=5)
        
        # Conteúdo
        tk.Label(card_inner, text="Conteúdo:", font=("Segoe UI", 10), 
                bg='white', fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        
        self.text_entry = tk.Text(card_inner, height=12, font=("Segoe UI", 11),
                                  bg='#F8F9FA', relief=tk.FLAT, highlightthickness=1,
                                  highlightcolor='#3498DB', highlightbackground='#D0D0D0',
                                  wrap=tk.WORD)
        self.text_entry.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Botões de ação
        btn_frame = tk.Frame(card_inner, bg='white')
        btn_frame.pack(fill=tk.X)
        
        save_btn = tk.Button(btn_frame, text="💾 Salvar no Diário", command=self.save_entry,
                            bg='#27AE60', fg='white', font=("Segoe UI", 10, "bold"),
                            relief=tk.FLAT, cursor='hand2', padx=20, pady=10)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(btn_frame, text="🗑️ Limpar", command=self.clear_form,
                             bg='#95A5A6', fg='white', font=("Segoe UI", 10, "bold"),
                             relief=tk.FLAT, cursor='hand2', padx=20, pady=10)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Efeitos hover
        for btn, color in [(save_btn, '#219A52'), (clear_btn, '#7F8C8D')]:
            def on_enter(e, b=btn, c=color):
                b['background'] = c
            def on_leave(e, b=btn):
                b['background'] = btn.cget('bg')
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
        
        # Coluna direita - Lista de entradas
        right_column = tk.Frame(content_frame, bg='white', width=450)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_column.pack_propagate(False)
        
        tk.Label(right_column, text="📖 Entradas Recentes", font=("Segoe UI", 14, "bold"), 
                bg='white', fg='#2C3E50').pack(anchor=tk.W, pady=(0, 10))
        
        # Frame com scroll para entradas
        entries_container = tk.Frame(right_column, bg='white')
        entries_container.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(entries_container, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(entries_container, orient="vertical", command=canvas.yview)
        self.entries_frame = tk.Frame(canvas, bg='white')
        
        self.entries_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.canvas_window = canvas.create_window((0, 0), window=self.entries_frame, anchor="nw", width=canvas.winfo_reqwidth())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Scroll com mouse wheel
        def on_mousewheel(event):
            try:
                if not canvas.winfo_exists():
                    return
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except Exception:
                logging.getLogger(__name__).exception("Erro no on_mousewheel do diário")

        canvas.bind_all('<MouseWheel>', on_mousewheel)
        
        def configure_canvas(event):
            try:
                canvas.itemconfig(self.canvas_window, width=event.width)
            except Exception:
                pass
        
        canvas.bind('<Configure>', configure_canvas)
        
        # Atualizar exibição
        self.update_entries_display()
        self.update_statistics()
    
    def select_mood(self, mood):
        self.selected_mood = mood
        # Resetar todos os botões
        for btn in self.mood_buttons.values():
            btn.configure(bg='#F8F9FA', relief=tk.FLAT)
        # Destacar botão selecionado
        self.mood_buttons[mood].configure(bg='#FFE5B4', relief=tk.SUNKEN)
    
    def set_filter(self, filter_type):
        self.filter_type = filter_type
        self.update_entries_display()
        self.update_statistics()
    
    def on_search(self, event=None):
        self.search_term = self.search_entry.get().strip().lower()
        self.update_entries_display()
    
    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.search_term = ""
        self.update_entries_display()
    
    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.text_entry.delete('1.0', tk.END)
        self.selected_mood = None
        for btn in self.mood_buttons.values():
            btn.configure(bg='#F8F9FA', relief=tk.FLAT)
    
    def save_entry(self):
        content = self.text_entry.get('1.0', tk.END).strip()
        if not content:
            messagebox.showwarning("Aviso", "Digite algo no diário!")
            return
        
        title = self.title_entry.get().strip()
        if not title:
            title = f"Entrada de {datetime.now().strftime('%d/%m/%Y')}"
        
        entry = {
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "data_formatada": datetime.now().strftime("%d/%m/%Y às %H:%M"),
            "titulo": title,
            "texto": content,
            "humor": self.selected_mood,
            "data_obj": datetime.now().timestamp()
        }
        
        self.app.diario_entries.insert(0, entry)
        self.app.save_data()
        self.clear_form()
        self.update_entries_display()
        self.update_statistics()
        
        messagebox.showinfo("Sucesso", "✨ Entrada salva no diário!")
    
    def get_filtered_entries(self):
        entries = self.app.diario_entries.copy()
        
        # Filtro por busca
        if self.search_term:
            entries = [e for e in entries if 
                      self.search_term in e['titulo'].lower() or 
                      self.search_term in e['texto'].lower()]
        
        # Filtro por período
        if self.filter_type == "week":
            from datetime import timedelta
            week_ago = datetime.now() - timedelta(days=7)
            entries = [e for e in entries if datetime.fromtimestamp(e['data_obj']) >= week_ago]
        elif self.filter_type == "month":
            from datetime import timedelta
            month_ago = datetime.now() - timedelta(days=30)
            entries = [e for e in entries if datetime.fromtimestamp(e['data_obj']) >= month_ago]
        elif self.filter_type == "recent":
            entries = entries[:10]
        
        return entries
    
    def update_statistics(self):
        total = len(self.app.diario_entries)
        
        # Entradas deste mês
        current_month = datetime.now().month
        current_year = datetime.now().year
        month_entries = sum(1 for e in self.app.diario_entries 
                           if datetime.fromtimestamp(e['data_obj']).month == current_month and
                           datetime.fromtimestamp(e['data_obj']).year == current_year)
        
        # Calcular sequência (streak)
        dates = sorted([datetime.fromtimestamp(e['data_obj']).date() 
                       for e in self.app.diario_entries], reverse=True)
        
        streak = 0
        best_streak = 0
        current_streak = 0
        last_date = None
        
        for date in dates:
            if last_date is None:
                current_streak = 1
            elif (last_date - date).days == 1:
                current_streak += 1
            elif (last_date - date).days > 1:
                current_streak = 1
            else:
                continue
            
            best_streak = max(best_streak, current_streak)
            last_date = date
        
        # Sequência atual (dias consecutivos até hoje)
        today = datetime.now().date()
        streak = 0
        for date in dates:
            if (today - date).days == streak:
                streak += 1
            else:
                break
        
        self.stats_labels['total_entries'].config(text=str(total))
        self.stats_labels['month_entries'].config(text=str(month_entries))
        self.stats_labels['streak'].config(text=f"{streak} dias")
        self.stats_labels['best_streak'].config(text=f"{best_streak} dias")
    
    def update_entries_display(self):
        # Limpar frame
        for widget in self.entries_frame.winfo_children():
            widget.destroy()
        
        filtered_entries = self.get_filtered_entries()
        
        if not filtered_entries:
            empty_frame = tk.Frame(self.entries_frame, bg='white')
            empty_frame.pack(expand=True, fill=tk.BOTH, pady=50)
            
            if self.search_term or self.filter_type != "all":
                tk.Label(empty_frame, text="🔍", font=("Segoe UI", 48), 
                        bg='white', fg='#BDC3C7').pack()
                tk.Label(empty_frame, text="Nenhuma entrada encontrada", 
                        font=("Segoe UI", 14), bg='white', fg='#7F8C8D').pack(pady=10)
            else:
                tk.Label(empty_frame, text="📔", font=("Segoe UI", 48), 
                        bg='white', fg='#BDC3C7').pack()
                tk.Label(empty_frame, text="Comece a escrever seu diário", 
                        font=("Segoe UI", 14), bg='white', fg='#7F8C8D').pack(pady=10)
                tk.Label(empty_frame, text="Suas memórias e sentimentos te esperam ✨", 
                        font=("Segoe UI", 10), bg='white', fg='#95A5A6').pack()
            return
        
        for entry in filtered_entries:
            # Card da entrada
            entry_card = tk.Frame(self.entries_frame, bg='white', relief=tk.RAISED, bd=1)
            entry_card.pack(fill=tk.X, pady=8)
            entry_card.configure(highlightbackground='#E0E0E0', highlightthickness=1)
            
            inner_card = tk.Frame(entry_card, bg='white')
            inner_card.pack(fill=tk.X, padx=15, pady=12)
            
            # Cabeçalho
            header_frame = tk.Frame(inner_card, bg='white')
            header_frame.pack(fill=tk.X, pady=(0, 8))
            
            # Humor
            if entry.get('humor'):
                tk.Label(header_frame, text=entry['humor'], font=("Segoe UI", 16), 
                        bg='white').pack(side=tk.LEFT, padx=(0, 10))
            
            # Título
            tk.Label(header_frame, text=entry['titulo'], font=("Segoe UI", 12, "bold"), 
                    bg='white', fg='#2C3E50', wraplength=350, justify=tk.LEFT).pack(side=tk.LEFT, expand=True, anchor=tk.W)
            
            # Data
            tk.Label(inner_card, text=f"📅 {entry['data_formatada']}", font=("Segoe UI", 9), 
                    bg='white', fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 8))
            
            # Conteúdo (prévia)
            preview = entry['texto'][:150] + ("..." if len(entry['texto']) > 150 else "")
            tk.Label(inner_card, text=preview, font=("Segoe UI", 10), 
                    bg='white', fg='#34495E', wraplength=400, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 8))
            
            # Botões de ação
            btn_frame = tk.Frame(inner_card, bg='white')
            btn_frame.pack(fill=tk.X)
            
            view_btn = tk.Button(btn_frame, text="👁️ Ver completa", 
                                command=lambda e=entry: self.view_full_entry(e),
                                bg='#3498DB', fg='white', font=("Segoe UI", 9),
                                relief=tk.FLAT, cursor='hand2', padx=10, pady=5)
            view_btn.pack(side=tk.LEFT, padx=2)
            
            edit_btn = tk.Button(btn_frame, text="✏️ Editar", 
                                command=lambda e=entry: self.edit_entry(e),
                                bg='#F39C12', fg='white', font=("Segoe UI", 9),
                                relief=tk.FLAT, cursor='hand2', padx=10, pady=5)
            edit_btn.pack(side=tk.LEFT, padx=2)
            
            delete_btn = tk.Button(btn_frame, text="🗑️ Excluir", 
                                  command=lambda e=entry: self.delete_entry(e),
                                  bg='#E74C3C', fg='white', font=("Segoe UI", 9),
                                  relief=tk.FLAT, cursor='hand2', padx=10, pady=5)
            delete_btn.pack(side=tk.LEFT, padx=2)
            
            # Efeitos hover
            for btn, color in [(view_btn, '#2980B9'), (edit_btn, '#E67E22'), (delete_btn, '#C0392B')]:
                def on_enter(e, b=btn, c=color):
                    b['background'] = c
                def on_leave(e, b=btn):
                    b['background'] = btn.cget('bg')
                btn.bind('<Enter>', on_enter)
                btn.bind('<Leave>', on_leave)
    
    def view_full_entry(self, entry):
        # Janela de visualização completa
        view_window = tk.Toplevel(self.app.content_frame)
        view_window.title("Entrada do Diário")
        view_window.geometry("600x500")
        view_window.configure(bg='white')
        
        view_window.transient(self.app.content_frame)
        view_window.grab_set()
        
        # Centralizar
        view_window.update_idletasks()
        x = (view_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (view_window.winfo_screenheight() // 2) - (500 // 2)
        view_window.geometry(f"600x500+{x}+{y}")
        
        main_frame = tk.Frame(view_window, bg='white', padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        if entry.get('humor'):
            tk.Label(header_frame, text=entry['humor'], font=("Segoe UI", 24), 
                    bg='white').pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(header_frame, text=entry['titulo'], font=("Segoe UI", 18, "bold"), 
                bg='white', fg='#2C3E50', wraplength=450).pack(anchor=tk.W)
        
        tk.Label(main_frame, text=f"📅 {entry['data_formatada']}", font=("Segoe UI", 11), 
                bg='white', fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 20))
        
        # Linha separadora
        tk.Frame(main_frame, height=2, bg='#ECF0F1').pack(fill=tk.X, pady=(0, 15))
        
        # Conteúdo
        text_widget = tk.Text(main_frame, font=("Segoe UI", 11), wrap=tk.WORD,
                             bg='#F8F9FA', relief=tk.FLAT, padx=15, pady=15)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert('1.0', entry['texto'])
        text_widget.configure(state='disabled')
        
        # Botão fechar
        close_btn = tk.Button(main_frame, text="Fechar", command=view_window.destroy,
                             bg='#3498DB', fg='white', font=("Segoe UI", 10, "bold"),
                             relief=tk.FLAT, padx=20, pady=8)
        close_btn.pack(pady=(15, 0))
    
    def edit_entry(self, entry):
        # Encontrar índice da entrada
        index = self.app.diario_entries.index(entry)
        
        # Preencher formulário
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, entry['titulo'])
        
        self.text_entry.delete('1.0', tk.END)
        self.text_entry.insert('1.0', entry['texto'])
        
        if entry.get('humor'):
            self.select_mood(entry['humor'])
        
        # Remover entrada antiga
        del self.app.diario_entries[index]
        
        # Rolar para o topo do formulário
        self.text_entry.focus()
        
        messagebox.showinfo("Editar", "Faça as alterações e clique em 'Salvar'")
    
    def delete_entry(self, entry):
        if messagebox.askyesno("Confirmar Exclusão", 
                               "Tem certeza que deseja excluir esta entrada?\n\nEsta ação não pode ser desfeita.",
                               icon='warning'):
            self.app.diario_entries.remove(entry)
            self.app.save_data()
            self.update_entries_display()
            self.update_statistics()
            messagebox.showinfo("Sucesso", "Entrada excluída!")