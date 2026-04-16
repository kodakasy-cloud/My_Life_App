import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkinter import font as tkfont

class AnotacoesManager:
    def __init__(self, app):
        self.app = app
        self.note_entry = None
        self.title_entry = None
        self.notes_frame = None
        self.current_colors = ['#FFE5B4', '#FFD1DC', '#C9E4DE', '#D4E6F1', '#E8DAEF', '#F9E79F']
        self.filter_favorites_only = False
        self.search_term = ""
        self.sort_by = "date"  # date, title, favorite
        
    def open_anotacoes(self):
        self.app.clear_content()
        
        # Container principal com padding
        main_container = tk.Frame(self.app.content_frame, bg='white')
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Título com ícone
        title_frame = tk.Frame(main_container, bg='white')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(title_frame, text="📝", font=("Segoe UI", 32), 
                bg='white').pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(title_frame, text="Minhas Anotações", font=("Segoe UI", 24, "bold"), 
                bg='white', fg='#2C3E50').pack(side=tk.LEFT)
        
        # Barra de ferramentas (filtros e busca)
        toolbar = tk.Frame(main_container, bg='white')
        toolbar.pack(fill=tk.X, pady=(0, 15))
        
        # Botão de favoritos
        self.fav_filter_btn = tk.Button(toolbar, text="⭐ Todas", command=self.toggle_favorite_filter,
                                        bg='#ECF0F1', fg='#2C3E50', font=("Segoe UI", 9, "bold"),
                                        relief=tk.FLAT, padx=15, pady=5, cursor='hand2')
        self.fav_filter_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botões de ordenação
        tk.Label(toolbar, text="Ordenar:", bg='white', font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 5))
        
        sort_date_btn = tk.Button(toolbar, text="📅 Data", command=lambda: self.set_sort('date'),
                                  bg='white', fg='#7F8C8D', font=("Segoe UI", 9),
                                  relief=tk.FLAT, cursor='hand2')
        sort_date_btn.pack(side=tk.LEFT, padx=2)
        
        sort_title_btn = tk.Button(toolbar, text="🔤 Título", command=lambda: self.set_sort('title'),
                                   bg='white', fg='#7F8C8D', font=("Segoe UI", 9),
                                   relief=tk.FLAT, cursor='hand2')
        sort_title_btn.pack(side=tk.LEFT, padx=2)
        
        sort_fav_btn = tk.Button(toolbar, text="⭐ Favoritos", command=lambda: self.set_sort('favorite'),
                                 bg='white', fg='#7F8C8D', font=("Segoe UI", 9),
                                 relief=tk.FLAT, cursor='hand2')
        sort_fav_btn.pack(side=tk.LEFT, padx=2)
        
        # Campo de busca
        search_frame = tk.Frame(toolbar, bg='white')
        search_frame.pack(side=tk.RIGHT)
        
        tk.Label(search_frame, text="🔍", bg='white', font=("Segoe UI", 11)).pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, font=("Segoe UI", 10), width=20,
                                     bg='#F8F9FA', relief=tk.FLAT, highlightthickness=1,
                                     highlightcolor='#3498DB', highlightbackground='#D0D0D0')
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        clear_search_btn = tk.Button(search_frame, text="✖", command=self.clear_search,
                                     bg='white', fg='#95A5A6', font=("Segoe UI", 9),
                                     relief=tk.FLAT, cursor='hand2')
        clear_search_btn.pack(side=tk.LEFT)
        
        # Frame de adicionar anotação (estilizado)
        add_card = tk.Frame(main_container, bg='white', relief=tk.RAISED, bd=1)
        add_card.pack(fill=tk.X, pady=(0, 20))
        add_card.configure(highlightbackground='#E0E0E0', highlightthickness=1)
        
        # Padding interno do card
        add_inner = tk.Frame(add_card, bg='white')
        add_inner.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(add_inner, text="✏️ Nova Anotação", font=("Segoe UI", 12, "bold"), 
                bg='white', fg='#34495E').pack(anchor=tk.W, pady=(0, 10))
        
        # Campo de título
        title_frame_add = tk.Frame(add_inner, bg='white')
        title_frame_add.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(title_frame_add, text="Título:", bg='white', font=("Segoe UI", 10), 
                fg='#7F8C8D').pack(anchor=tk.W)
        
        self.title_entry = tk.Entry(title_frame_add, font=("Segoe UI", 11, "bold"),
                                    bg='#F8F9FA', fg='#2C3E50',
                                    relief=tk.FLAT, highlightthickness=1,
                                    highlightcolor='#3498DB', highlightbackground='#D0D0D0')
        self.title_entry.pack(fill=tk.X, ipady=5)
        
        # Campo de conteúdo
        tk.Label(add_inner, text="Conteúdo:", bg='white', font=("Segoe UI", 10), 
                fg='#7F8C8D').pack(anchor=tk.W)
        
        self.note_entry = tk.Entry(add_inner, font=("Segoe UI", 11), 
                                  bg='#F8F9FA', fg='#2C3E50',
                                  relief=tk.FLAT, highlightthickness=1,
                                  highlightcolor='#3498DB', highlightbackground='#D0D0D0')
        self.note_entry.pack(fill=tk.X, pady=(0, 10), ipady=8)
        
        # Bind Enter para adicionar anotação
        self.note_entry.bind('<Return>', lambda e: self.add_note())
        self.title_entry.bind('<Return>', lambda e: self.add_note())
        
        # Botão de adicionar com hover effect
        btn_frame = tk.Frame(add_inner, bg='white')
        btn_frame.pack(fill=tk.X)
        
        add_btn = tk.Button(btn_frame, text="➕ Adicionar Anotação", 
                           command=self.add_note,
                           bg='#3498DB', fg='white', 
                           font=("Segoe UI", 10, "bold"),
                           relief=tk.FLAT, cursor='hand2',
                           padx=20, pady=8)
        add_btn.pack()
        
        # Efeito hover no botão
        def on_enter(e):
            add_btn['background'] = '#2980B9'
        def on_leave(e):
            add_btn['background'] = '#3498DB'
        
        add_btn.bind('<Enter>', on_enter)
        add_btn.bind('<Leave>', on_leave)
        
        # Frame para lista de anotações com scroll
        notes_container = tk.Frame(main_container, bg='white')
        notes_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas e Scrollbar para scroll suave
        canvas = tk.Canvas(notes_container, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(notes_container, orient="vertical", command=canvas.yview)
        self.notes_frame = tk.Frame(canvas, bg='white')
        
        self.notes_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=self.notes_frame, anchor="nw", width=canvas.winfo_reqwidth())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Scroll com mouse wheel
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all('<MouseWheel>', on_mousewheel)
        
        # Atualizar exibição
        self.update_notes_display()
        
        # Atualizar largura do canvas quando redimensionar
        def configure_canvas(event):
            canvas.itemconfig(1, width=event.width)
        
        canvas.bind('<Configure>', configure_canvas)
    
    def toggle_favorite_filter(self):
        self.filter_favorites_only = not self.filter_favorites_only
        if self.filter_favorites_only:
            self.fav_filter_btn.configure(text="⭐ Favoritos", bg='#F9E79F', fg='#F39C12')
        else:
            self.fav_filter_btn.configure(text="⭐ Todas", bg='#ECF0F1', fg='#2C3E50')
        self.update_notes_display()
    
    def set_sort(self, sort_type):
        self.sort_by = sort_type
        self.update_notes_display()
    
    def on_search(self, event=None):
        self.search_term = self.search_entry.get().strip().lower()
        self.update_notes_display()
    
    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.search_term = ""
        self.update_notes_display()
    
    def add_note(self):
        title_text = self.title_entry.get().strip()
        note_text = self.note_entry.get().strip()
        
        if not note_text:
            messagebox.showwarning("Aviso", "Digite o conteúdo da anotação!")
            return
        
        if not title_text:
            title_text = "Sem título"
        
        # Verificar se é a primeira anotação do dia
        today = datetime.now().strftime("%d/%m/%Y")
        is_first_today = not any(n['data'].startswith(today) for n in self.app.notas)
        
        note = {
            "titulo": title_text,
            "texto": note_text,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "favorito": False,
            "destaque": is_first_today
        }
        self.app.notas.append(note)
        self.app.save_data()
        self.title_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)
        self.update_notes_display()
        
        # Animação de fade (efeito visual)
        self.animate_new_note()
    
    def get_filtered_and_sorted_notes(self):
        # Filtrar notas
        notes = self.app.notas.copy()
        
        # Filtro de favoritos
        if self.filter_favorites_only:
            notes = [n for n in notes if n.get('favorito', False)]
        
        # Filtro de busca
        if self.search_term:
            notes = [n for n in notes if self.search_term in n['titulo'].lower() or 
                    self.search_term in n['texto'].lower()]
        
        # Ordenação
        if self.sort_by == 'date':
            notes = sorted(notes, key=lambda x: x['data'], reverse=True)
        elif self.sort_by == 'title':
            notes = sorted(notes, key=lambda x: x['titulo'].lower())
        elif self.sort_by == 'favorite':
            notes = sorted(notes, key=lambda x: (not x.get('favorito', False), x['data']), reverse=True)
        
        return notes
    
    def animate_new_note(self):
        # Simples efeito de flash na última anotação
        if self.notes_frame.winfo_children():
            last_note = self.notes_frame.winfo_children()[-1]
            original_bg = last_note.cget('bg')
            last_note.configure(bg='#90EE90')
            self.app.content_frame.after(500, lambda: last_note.configure(bg=original_bg))
    
    def update_notes_display(self):
        # Limpar frame atual
        for widget in self.notes_frame.winfo_children():
            widget.destroy()
        
        filtered_notes = self.get_filtered_and_sorted_notes()
        
        if not filtered_notes:
            # Mensagem quando não há anotações
            empty_frame = tk.Frame(self.notes_frame, bg='white')
            empty_frame.pack(expand=True, fill=tk.BOTH, pady=50)
            
            if self.filter_favorites_only or self.search_term:
                tk.Label(empty_frame, text="🔍", font=("Segoe UI", 48), 
                        bg='white', fg='#BDC3C7').pack()
                tk.Label(empty_frame, text="Nenhuma anotação encontrada", 
                        font=("Segoe UI", 14), bg='white', fg='#7F8C8D').pack(pady=10)
                tk.Label(empty_frame, text="Tente outros filtros ou palavras-chave", 
                        font=("Segoe UI", 10), bg='white', fg='#95A5A6').pack()
            else:
                tk.Label(empty_frame, text="📭", font=("Segoe UI", 48), 
                        bg='white', fg='#BDC3C7').pack()
                tk.Label(empty_frame, text="Nenhuma anotação ainda", 
                        font=("Segoe UI", 14), bg='white', fg='#7F8C8D').pack(pady=10)
                tk.Label(empty_frame, text="Comece a escrever suas ideias acima ✨", 
                        font=("Segoe UI", 10), bg='white', fg='#95A5A6').pack()
            return
        
        # Agrupar anotações por data
        notes_by_date = {}
        for note in filtered_notes:
            date = note['data'].split()[0]
            if date not in notes_by_date:
                notes_by_date[date] = []
            notes_by_date[date].append(note)
        
        # Exibir anotações agrupadas
        for idx, (date, notes) in enumerate(notes_by_date.items()):
            # Separador de data
            date_frame = tk.Frame(self.notes_frame, bg='white')
            date_frame.pack(fill=tk.X, pady=(15 if idx > 0 else 0, 5))
            
            # Contador de anotações do dia
            tk.Label(date_frame, text=f"📅 {date} ({len(notes)} anotação{'' if len(notes) == 1 else 'ões'})", 
                    font=("Segoe UI", 10, "bold"), bg='white', fg='#7F8C8D').pack(anchor=tk.W)
            
            tk.Frame(date_frame, height=2, bg='#ECF0F1').pack(fill=tk.X, pady=5)
            
            # Anotações desta data
            for i, note in enumerate(notes):
                # Cor baseada no índice ou destaque/favorito
                if note.get('favorito', False):
                    bg_color = '#FFF4E6'
                    border_color = '#F39C12'
                    star_icon = "⭐ "
                elif note.get('destaque', False):
                    bg_color = '#FFF9C4'
                    border_color = '#F9E79F'
                    star_icon = "✨ "
                else:
                    bg_color = self.current_colors[i % len(self.current_colors)]
                    border_color = '#E0E0E0'
                    star_icon = ""
                
                # Card da anotação
                note_card = tk.Frame(self.notes_frame, bg=bg_color, relief=tk.RAISED, bd=0)
                note_card.pack(fill=tk.X, pady=8)
                note_card.configure(highlightbackground=border_color, highlightthickness=1)
                
                # Frame interno para padding
                inner_card = tk.Frame(note_card, bg=bg_color)
                inner_card.pack(fill=tk.X, padx=15, pady=12)
                
                # Título da anotação
                title_text = f"{star_icon}{note['titulo']}"
                title_label = tk.Label(inner_card, text=title_text, 
                                      font=("Segoe UI", 12, "bold"), 
                                      bg=bg_color, fg='#2C3E50', 
                                      wraplength=600, justify=tk.LEFT)
                title_label.pack(anchor=tk.W, pady=(0, 5))
                
                # Texto da anotação
                text_label = tk.Label(inner_card, text=f"💭 {note['texto']}", 
                                     font=("Segoe UI", 10), 
                                     bg=bg_color, fg='#34495E', 
                                     wraplength=600, justify=tk.LEFT)
                text_label.pack(anchor=tk.W, pady=(0, 8))
                
                # Frame inferior com data e botões
                bottom_frame = tk.Frame(inner_card, bg=bg_color)
                bottom_frame.pack(fill=tk.X)
                
                # Data
                tk.Label(bottom_frame, text=f"🕐 {note['data'].split()[1]}", 
                        font=("Segoe UI", 8), bg=bg_color, fg='#7F8C8D').pack(side=tk.LEFT)
                
                # Botões de ação
                btn_frame = tk.Frame(bottom_frame, bg=bg_color)
                btn_frame.pack(side=tk.RIGHT)
                
                # Botão favorito
                fav_icon = "⭐" if note.get('favorito', False) else "☆"
                fav_btn = tk.Label(btn_frame, text=fav_icon, font=("Segoe UI", 12), 
                                  bg=bg_color, fg='#F39C12', cursor='hand2')
                fav_btn.pack(side=tk.LEFT, padx=5)
                
                # Botão editar
                edit_btn = tk.Label(btn_frame, text="✏️", font=("Segoe UI", 10), 
                                   bg=bg_color, fg='#3498DB', cursor='hand2')
                edit_btn.pack(side=tk.LEFT, padx=5)
                
                # Botão excluir
                delete_btn = tk.Label(btn_frame, text="🗑️", font=("Segoe UI", 10), 
                                     bg=bg_color, fg='#E74C3C', cursor='hand2')
                delete_btn.pack(side=tk.LEFT, padx=5)
                
                # Encontrar índice original
                original_index = self.app.notas.index(note)
                
                # Bind eventos
                fav_btn.bind('<Button-1>', lambda e, idx=original_index: self.toggle_favorite(idx))
                edit_btn.bind('<Button-1>', lambda e, idx=original_index, card=note_card: self.edit_note(idx, card))
                delete_btn.bind('<Button-1>', lambda e, idx=original_index: self.delete_note(idx))
                
                # Hover effects nos botões
                for btn in [fav_btn, edit_btn, delete_btn]:
                    def on_hover(e, b=btn, color='#E0E0E0'):
                        b.configure(bg=color)
                    def on_leave(e, b=btn, bgc=bg_color):
                        b.configure(bg=bgc)
                    btn.bind('<Enter>', on_hover)
                    btn.bind('<Leave>', on_leave)
    
    def toggle_favorite(self, index):
        self.app.notas[index]['favorito'] = not self.app.notas[index].get('favorito', False)
        self.app.save_data()
        self.update_notes_display()
        
        # Animação
        if self.app.notas[index]['favorito']:
            messagebox.showinfo("Favorito", "Anotação adicionada aos favoritos! ⭐")
    
    def edit_note(self, index, note_card):
        # Criar janela de edição
        edit_window = tk.Toplevel(self.app.content_frame)
        edit_window.title("Editar Anotação")
        edit_window.geometry("550x400")
        edit_window.configure(bg='white')
        
        # Centralizar
        edit_window.transient(self.app.content_frame)
        edit_window.grab_set()
        
        # Frame principal
        main_frame = tk.Frame(edit_window, bg='white', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="✏️ Editar Anotação", font=("Segoe UI", 14, "bold"), 
                bg='white', fg='#2C3E50').pack(pady=(0, 15))
        
        # Campo de título
        tk.Label(main_frame, text="Título:", bg='white', font=("Segoe UI", 10), 
                fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        
        title_entry = tk.Entry(main_frame, font=("Segoe UI", 11, "bold"),
                               bg='#F8F9FA', fg='#2C3E50',
                               relief=tk.FLAT, highlightthickness=1,
                               highlightcolor='#3498DB', highlightbackground='#D0D0D0')
        title_entry.pack(fill=tk.X, pady=(0, 10), ipady=5)
        title_entry.insert(0, self.app.notas[index]['titulo'])
        
        # Campo de conteúdo
        tk.Label(main_frame, text="Conteúdo:", bg='white', font=("Segoe UI", 10), 
                fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        
        # Text widget para edição
        text_widget = tk.Text(main_frame, font=("Segoe UI", 11), 
                             wrap=tk.WORD, height=8,
                             relief=tk.FLAT, highlightthickness=1,
                             highlightcolor='#3498DB', highlightbackground='#D0D0D0')
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        text_widget.insert('1.0', self.app.notas[index]['texto'])
        
        # Frame de botões
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(fill=tk.X)
        
        def save_edit():
            new_title = title_entry.get().strip()
            new_text = text_widget.get('1.0', tk.END).strip()
            
            if not new_text:
                messagebox.showwarning("Aviso", "O conteúdo não pode estar vazio!")
                return
            
            if not new_title:
                new_title = "Sem título"
            
            self.app.notas[index]['titulo'] = new_title
            self.app.notas[index]['texto'] = new_text
            self.app.save_data()
            self.update_notes_display()
            edit_window.destroy()
        
        def cancel_edit():
            edit_window.destroy()
        
        save_btn = tk.Button(btn_frame, text="💾 Salvar", command=save_edit,
                            bg='#27AE60', fg='white', font=("Segoe UI", 10, "bold"),
                            relief=tk.FLAT, padx=20, pady=8)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="❌ Cancelar", command=cancel_edit,
                              bg='#95A5A6', fg='white', font=("Segoe UI", 10, "bold"),
                              relief=tk.FLAT, padx=20, pady=8)
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Efeitos hover
        for btn, color in [(save_btn, '#219A52'), (cancel_btn, '#7F8C8D')]:
            def on_enter(e, b=btn, c=color):
                b['background'] = c
            def on_leave(e, b=btn):
                b['background'] = btn.cget('bg')
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)
    
    def delete_note(self, index):
        result = messagebox.askyesno("Confirmar Exclusão", 
                                     "Tem certeza que deseja excluir esta anotação?\n\nEsta ação não pode ser desfeita.",
                                     icon='warning')
        if result:
            del self.app.notas[index]
            self.app.save_data()
            self.update_notes_display()