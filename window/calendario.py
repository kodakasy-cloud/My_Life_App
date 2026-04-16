import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import calendar
from tkinter import font as tkfont


class CalendarioManager:
    def __init__(self, app):
        self.app = app
        self.current_year = None
        self.current_month = None
        self.selected_date = None
        self.events = {}  # Dicionário para armazenar eventos {data: [eventos]}
        self.reminders = {}  # Dicionário para lembretes
        self.event_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#F39C12']
        self.load_events()
        
    def load_events(self):
        # Carregar eventos salvos (se existirem)
        if hasattr(self.app, 'eventos') and self.app.eventos:
            self.events = self.app.eventos
        else:
            # Eventos de exemplo
            today = datetime.now()
            self.events = {
                f"{today.day}/{today.month}/{today.year}": [
                    {"titulo": "Reunião importante", "hora": "14:00", "descricao": "Reunião com a equipe", "cor": 0}
                ]
            }
    
    def save_events(self):
        if hasattr(self.app, 'eventos'):
            self.app.eventos = self.events
            self.app.save_data()
    
    def open_calendario(self):
        self.app.clear_content()
        
        # Container principal
        main_container = tk.Frame(self.app.content_frame, bg='white')
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Título
        title_frame = tk.Frame(main_container, bg='white')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(title_frame, text="📅", font=("Segoe UI", 32), 
                bg='white').pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(title_frame, text="Calendário Inteligente", font=("Segoe UI", 24, "bold"), 
                bg='white', fg='#2C3E50').pack(side=tk.LEFT)
        
        # Frame principal com duas colunas
        content_frame = tk.Frame(main_container, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Coluna esquerda - Calendário
        left_column = tk.Frame(content_frame, bg='white')
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # Coluna direita - Eventos do dia
        right_column = tk.Frame(content_frame, bg='#F8F9FA', width=350)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_column.pack_propagate(False)
        
        # Título da coluna direita
        tk.Label(right_column, text="📋 Eventos do Dia", font=("Segoe UI", 14, "bold"), 
                bg='#F8F9FA', fg='#2C3E50').pack(pady=(20, 10))
        
        # Frame para lista de eventos
        self.events_frame = tk.Frame(right_column, bg='#F8F9FA')
        self.events_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Canvas com scroll para eventos
        events_canvas = tk.Canvas(self.events_frame, bg='#F8F9FA', highlightthickness=0)
        events_scrollbar = tk.Scrollbar(self.events_frame, orient="vertical", command=events_canvas.yview)
        self.events_list_frame = tk.Frame(events_canvas, bg='#F8F9FA')
        
        self.events_list_frame.bind("<Configure>", lambda e: events_canvas.configure(scrollregion=events_canvas.bbox("all")))
        events_canvas.create_window((0, 0), window=self.events_list_frame, anchor="nw", width=320)
        events_canvas.configure(yscrollcommand=events_scrollbar.set)
        
        events_canvas.pack(side="left", fill="both", expand=True)
        events_scrollbar.pack(side="right", fill="y")
        
        # Botão adicionar evento
        add_event_btn = tk.Button(right_column, text="➕ Adicionar Evento", 
                                 command=self.open_add_event_dialog,
                                 bg='#3498DB', fg='white', 
                                 font=("Segoe UI", 10, "bold"),
                                 relief=tk.FLAT, cursor='hand2',
                                 padx=20, pady=10)
        add_event_btn.pack(pady=(10, 20), padx=15, fill=tk.X)
        
        # Efeito hover no botão
        def on_enter(e):
            add_event_btn['background'] = '#2980B9'
        def on_leave(e):
            add_event_btn['background'] = '#3498DB'
        add_event_btn.bind('<Enter>', on_enter)
        add_event_btn.bind('<Leave>', on_leave)
        
        # Frame do calendário
        cal_wrapper = tk.Frame(left_column, bg='white')
        cal_wrapper.pack(fill=tk.BOTH, expand=True)
        
        # Barra de navegação melhorada
        nav_frame = tk.Frame(cal_wrapper, bg='white')
        nav_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Botões de navegação
        btn_prev = tk.Button(nav_frame, text="◀◀", command=lambda: self.change_month(-12),
                            bg='#ECF0F1', fg='#2C3E50', font=("Segoe UI", 10),
                            relief=tk.FLAT, cursor='hand2')
        btn_prev.pack(side=tk.LEFT, padx=2)
        
        btn_prev_year = tk.Button(nav_frame, text="◀", command=lambda: self.change_month(-1),
                                 bg='#ECF0F1', fg='#2C3E50', font=("Segoe UI", 10),
                                 relief=tk.FLAT, cursor='hand2')
        btn_prev_year.pack(side=tk.LEFT, padx=2)
        
        # Display do mês/ano
        self.month_label = tk.Label(nav_frame, text="", font=("Segoe UI", 16, "bold"), 
                                   bg='white', fg='#2C3E50', width=20)
        self.month_label.pack(side=tk.LEFT, expand=True)
        
        btn_next_year = tk.Button(nav_frame, text="▶", command=lambda: self.change_month(1),
                                 bg='#ECF0F1', fg='#2C3E50', font=("Segoe UI", 10),
                                 relief=tk.FLAT, cursor='hand2')
        btn_next_year.pack(side=tk.RIGHT, padx=2)
        
        btn_next = tk.Button(nav_frame, text="▶▶", command=lambda: self.change_month(12),
                            bg='#ECF0F1', fg='#2C3E50', font=("Segoe UI", 10),
                            relief=tk.FLAT, cursor='hand2')
        btn_next.pack(side=tk.RIGHT, padx=2)
        
        # Botão hoje
        today_btn = tk.Button(nav_frame, text="📅 Hoje", command=self.go_to_today,
                             bg='#27AE60', fg='white', font=("Segoe UI", 9, "bold"),
                             relief=tk.FLAT, cursor='hand2', padx=15)
        today_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Frame do grid do calendário
        self.calendar_frame = tk.Frame(cal_wrapper, bg='white')
        self.calendar_frame.pack(fill=tk.BOTH, expand=True)
        
        # Inicializar com data atual
        now = datetime.now()
        self.current_year = now.year
        self.current_month = now.month
        self.selected_date = now.day
        
        self.show_calendar()
        
        # Atualizar eventos do dia atual
        self.update_events_display(now.day, now.month, now.year)
    
    def change_month(self, delta):
        self.current_month += delta
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        elif self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.show_calendar()
    
    def go_to_today(self):
        now = datetime.now()
        self.current_year = now.year
        self.current_month = now.month
        self.selected_date = now.day
        self.show_calendar()
        self.update_events_display(now.day, now.month, now.year)
    
    def show_calendar(self):
        # Limpar frame
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        # Atualizar label do mês
        self.month_label.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")
        
        # Configuração de estilo
        style = ttk.Style()
        style.configure("Calendar.TLabel", font=("Segoe UI", 11))
        
        # Frame para dias da semana
        weekdays_frame = tk.Frame(self.calendar_frame, bg='white')
        weekdays_frame.pack(pady=(0, 10))
        
        weekdays = ["SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM"]
        for i, day in enumerate(weekdays):
            # Cor diferente para fim de semana
            if i >= 5:  # Sábado e Domingo
                bg_color = '#FFE5E5'
                fg_color = '#E74C3C'
            else:
                bg_color = '#3498DB'
                fg_color = 'white'
            
            tk.Label(weekdays_frame, text=day, font=("Segoe UI", 11, "bold"), 
                    bg=bg_color, fg=fg_color, width=8, height=2, 
                    relief=tk.RAISED, borderwidth=1).grid(row=0, column=i, padx=2, pady=2)
        
        # Calendário
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        now = datetime.now()
        
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day != 0:
                    # Verificar se tem eventos neste dia
                    date_key = f"{day}/{self.current_month}/{self.current_year}"
                    has_events = date_key in self.events and len(self.events[date_key]) > 0
                    is_today = (day == now.day and self.current_month == now.month and 
                               self.current_year == now.year)
                    is_selected = (day == self.selected_date)
                    
                    # Definir cores
                    if is_today:
                        bg_color = '#FFF9C4'
                        border_color = '#F9E79F'
                    elif is_selected:
                        bg_color = '#3498DB'
                        fg_color = 'white'
                    elif has_events:
                        bg_color = '#D5F4E6'
                    else:
                        bg_color = 'white'
                        fg_color = '#2C3E50'
                    
                    # Frame do dia
                    day_frame = tk.Frame(weekdays_frame, bg=bg_color, relief=tk.RAISED, 
                                        borderwidth=1, highlightbackground=border_color if is_today else '#E0E0E0')
                    day_frame.grid(row=week_num + 1, column=day_num, padx=2, pady=2, sticky="nsew")
                    day_frame.configure(width=100, height=80)
                    day_frame.pack_propagate(False)
                    
                    # Número do dia
                    day_number = tk.Label(day_frame, text=str(day), font=("Segoe UI", 12, "bold"),
                                         bg=bg_color, fg=fg_color if is_selected else '#2C3E50')
                    day_number.pack(anchor=tk.NW, padx=5, pady=3)
                    
                    # Indicadores de eventos
                    if has_events:
                        events_count = len(self.events[date_key])
                        event_indicator = tk.Label(day_frame, text="●" * min(events_count, 3), 
                                                  font=("Segoe UI", 8), bg=bg_color, 
                                                  fg='#E74C3C' if events_count > 0 else 'white')
                        event_indicator.pack(anchor=tk.NW, padx=5)
                        
                        # Tooltip com eventos
                        self.create_tooltip(day_frame, self.get_events_preview(date_key))
                    
                    # Bind de clique
                    day_frame.bind('<Button-1>', lambda e, d=day: self.select_date(d))
                    day_frame.bind('<Double-Button-1>', lambda e, d=day: self.open_add_event_dialog(d))
                    
                    # Efeito hover
                    def on_enter(e, frame=day_frame, original_bg=bg_color):
                        frame.configure(bg='#E8F4FD')
                        for child in frame.winfo_children():
                            child.configure(bg='#E8F4FD')
                    
                    def on_leave(e, frame=day_frame, original_bg=bg_color):
                        frame.configure(bg=original_bg)
                        for child in frame.winfo_children():
                            child.configure(bg=original_bg)
                    
                    day_frame.bind('<Enter>', on_enter)
                    day_frame.bind('<Leave>', on_leave)
    
    def create_tooltip(self, widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, justify=tk.LEFT,
                           background="#FFFFE0", relief=tk.SOLID, borderwidth=1,
                           font=("Segoe UI", 9))
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
        
        widget.bind('<Enter>', show_tooltip)
    
    def get_events_preview(self, date_key):
        if date_key not in self.events:
            return "Sem eventos"
        
        preview = "Eventos:\n"
        for event in self.events[date_key]:
            preview += f"• {event['hora']} - {event['titulo']}\n"
        return preview
    
    def select_date(self, day):
        self.selected_date = day
        self.show_calendar()
        self.update_events_display(day, self.current_month, self.current_year)
    
    def update_events_display(self, day, month, year):
        # Limpar lista de eventos
        for widget in self.events_list_frame.winfo_children():
            widget.destroy()
        
        date_key = f"{day}/{month}/{year}"
        date_obj = datetime(year, month, day)
        
        # Cabeçalho da data
        tk.Label(self.events_list_frame, text=f"{date_obj.strftime('%A, %d de %B de %Y')}", 
                font=("Segoe UI", 12, "bold"), bg='#F8F9FA', fg='#2C3E50',
                wraplength=300).pack(pady=(0, 15))
        
        if date_key in self.events and self.events[date_key]:
            for i, event in enumerate(self.events[date_key]):
                # Card do evento
                event_card = tk.Frame(self.events_list_frame, bg='white', relief=tk.RAISED, bd=1)
                event_card.pack(fill=tk.X, pady=5, padx=5)
                event_card.configure(highlightbackground=self.event_colors[event.get('cor', 0)], 
                                    highlightthickness=2)
                
                inner_card = tk.Frame(event_card, bg='white')
                inner_card.pack(fill=tk.X, padx=10, pady=10)
                
                # Título e hora
                title_frame = tk.Frame(inner_card, bg='white')
                title_frame.pack(fill=tk.X, pady=(0, 5))
                
                tk.Label(title_frame, text=f"🕐 {event['hora']}", font=("Segoe UI", 9, "bold"),
                        bg='white', fg='#7F8C8D').pack(side=tk.LEFT)
                
                # Botões de ação
                btn_frame = tk.Frame(title_frame, bg='white')
                btn_frame.pack(side=tk.RIGHT)
                
                edit_btn = tk.Label(btn_frame, text="✏️", font=("Segoe UI", 9),
                                   bg='white', fg='#3498DB', cursor='hand2')
                edit_btn.pack(side=tk.LEFT, padx=3)
                
                delete_btn = tk.Label(btn_frame, text="🗑️", font=("Segoe UI", 9),
                                     bg='white', fg='#E74C3C', cursor='hand2')
                delete_btn.pack(side=tk.LEFT, padx=3)
                
                # Título do evento
                tk.Label(inner_card, text=event['titulo'], font=("Segoe UI", 11, "bold"),
                        bg='white', fg='#2C3E50', wraplength=250, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 5))
                
                # Descrição
                if event.get('descricao'):
                    tk.Label(inner_card, text=event['descricao'], font=("Segoe UI", 9),
                            bg='white', fg='#7F8C8D', wraplength=250, justify=tk.LEFT).pack(anchor=tk.W)
                
                # Bind eventos
                edit_btn.bind('<Button-1>', lambda e, idx=i, dk=date_key: self.edit_event(dk, idx))
                delete_btn.bind('<Button-1>', lambda e, idx=i, dk=date_key: self.delete_event(dk, idx))
        else:
            # Mensagem quando não há eventos
            tk.Label(self.events_list_frame, text="✨ Nenhum evento agendado\n\nClique em 'Adicionar Evento' para começar", 
                    font=("Segoe UI", 10), bg='#F8F9FA', fg='#95A5A6',
                    justify=tk.CENTER).pack(pady=30)
    
    def open_add_event_dialog(self, day=None):
        if day is None:
            day = self.selected_date
        
        # Janela de diálogo
        dialog = tk.Toplevel(self.app.content_frame)
        dialog.title("Adicionar Evento")
        dialog.geometry("600x900")
        dialog.configure(bg='white')
        dialog.transient(self.app.content_frame)
        dialog.grab_set()
        
        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (900 // 2)
        dialog.geometry(f"600x900+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(dialog, bg='white', padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="➕ Novo Evento", font=("Segoe UI", 16, "bold"), 
                bg='white', fg='#2C3E50').pack(pady=(0, 20))
        
        # Data
        tk.Label(main_frame, text="📅 Data:", bg='white', font=("Segoe UI", 10),
                fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        
        date_frame = tk.Frame(main_frame, bg='white')
        date_frame.pack(fill=tk.X, pady=(0, 15))
        
        day_var = tk.StringVar(value=str(day))
        month_var = tk.StringVar(value=str(self.current_month))
        year_var = tk.StringVar(value=str(self.current_year))
        
        tk.Spinbox(date_frame, from_=1, to=31, textvariable=day_var, width=5, font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=2)
        tk.Label(date_frame, text="/", bg='white').pack(side=tk.LEFT)
        tk.Spinbox(date_frame, from_=1, to=12, textvariable=month_var, width=5, font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=2)
        tk.Label(date_frame, text="/", bg='white').pack(side=tk.LEFT)
        tk.Spinbox(date_frame, from_=2020, to=2030, textvariable=year_var, width=7, font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=2)
        
        # Hora
        tk.Label(main_frame, text="⏰ Hora:", bg='white', font=("Segoe UI", 10),
                fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        
        hour_var = tk.StringVar(value="14")
        minute_var = tk.StringVar(value="00")
        
        time_frame = tk.Frame(main_frame, bg='white')
        time_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Spinbox(time_frame, from_=0, to=23, textvariable=hour_var, width=5, font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=2)
        tk.Label(time_frame, text=":", bg='white').pack(side=tk.LEFT)
        tk.Spinbox(time_frame, from_=0, to=59, textvariable=minute_var, width=5, font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=2)
        
        # Título
        tk.Label(main_frame, text="📝 Título:", bg='white', font=("Segoe UI", 10),
                fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        
        title_entry = tk.Entry(main_frame, font=("Segoe UI", 11),
                               bg='#F8F9FA', relief=tk.FLAT, highlightthickness=1,
                               highlightcolor='#3498DB', highlightbackground='#D0D0D0')
        title_entry.pack(fill=tk.X, pady=(0, 15), ipady=5)
        
        # Descrição
        tk.Label(main_frame, text="📄 Descrição (opcional):", bg='white', font=("Segoe UI", 10),
                fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        
        desc_text = tk.Text(main_frame, font=("Segoe UI", 10), height=4,
                           bg='#F8F9FA', relief=tk.FLAT, highlightthickness=1,
                           highlightcolor='#3498DB', highlightbackground='#D0D0D0')
        desc_text.pack(fill=tk.X, pady=(0, 15))
        
        # Cor do evento
        tk.Label(main_frame, text="🎨 Cor:", bg='white', font=("Segoe UI", 10),
                fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        
        color_frame = tk.Frame(main_frame, bg='white')
        color_frame.pack(fill=tk.X, pady=(0, 20))
        
        color_var = tk.IntVar(value=0)
        for i, color in enumerate(self.event_colors):
            rb = tk.Radiobutton(color_frame, bg='white', value=i, variable=color_var,
                               indicatoron=0, width=3, height=1)
            rb.configure(selectcolor=color, activebackground=color, bg=color)
            rb.pack(side=tk.LEFT, padx=2)
        
        # Botões
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(fill=tk.X)
        
        def save_event():
            try:
                event_date = f"{int(day_var.get())}/{int(month_var.get())}/{int(year_var.get())}"
                event_time = f"{int(hour_var.get()):02d}:{int(minute_var.get()):02d}"
                title = title_entry.get().strip()
                
                if not title:
                    messagebox.showwarning("Aviso", "Digite um título para o evento!")
                    return
                
                if event_date not in self.events:
                    self.events[event_date] = []
                
                self.events[event_date].append({
                    "titulo": title,
                    "hora": event_time,
                    "descricao": desc_text.get('1.0', tk.END).strip(),
                    "cor": color_var.get()
                })
                
                self.save_events()
                self.show_calendar()
                self.update_events_display(self.selected_date, self.current_month, self.current_year)
                dialog.destroy()
                
                messagebox.showinfo("Sucesso", "Evento adicionado com sucesso! 🎉")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar evento: {str(e)}")
        
        tk.Button(btn_frame, text="💾 Salvar Evento", command=save_event,
                 bg='#27AE60', fg='white', font=("Segoe UI", 10, "bold"),
                 relief=tk.FLAT, padx=20, pady=8).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="❌ Cancelar", command=dialog.destroy,
                 bg='#95A5A6', fg='white', font=("Segoe UI", 10, "bold"),
                 relief=tk.FLAT, padx=20, pady=8).pack(side=tk.LEFT, padx=5)
    
    def edit_event(self, date_key, event_index):
        event = self.events[date_key][event_index]
        
        # Diálogo de edição (similar ao de adicionar)
        dialog = tk.Toplevel(self.app.content_frame)
        dialog.title("Editar Evento")
        dialog.geometry("500x450")
        dialog.configure(bg='white')
        dialog.transient(self.app.content_frame)
        dialog.grab_set()
        
        main_frame = tk.Frame(dialog, bg='white', padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="✏️ Editar Evento", font=("Segoe UI", 16, "bold"), 
                bg='white', fg='#2C3E50').pack(pady=(0, 20))
        
        # Hora
        tk.Label(main_frame, text="⏰ Hora:", bg='white', font=("Segoe UI", 10),
                fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        
        time_parts = event['hora'].split(':')
        hour_var = tk.StringVar(value=time_parts[0])
        minute_var = tk.StringVar(value=time_parts[1])
        
        time_frame = tk.Frame(main_frame, bg='white')
        time_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Spinbox(time_frame, from_=0, to=23, textvariable=hour_var, width=5).pack(side=tk.LEFT, padx=2)
        tk.Label(time_frame, text=":", bg='white').pack(side=tk.LEFT)
        tk.Spinbox(time_frame, from_=0, to=59, textvariable=minute_var, width=5).pack(side=tk.LEFT, padx=2)
        
        # Título
        tk.Label(main_frame, text="📝 Título:", bg='white', font=("Segoe UI", 10),
                fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        
        title_entry = tk.Entry(main_frame, font=("Segoe UI", 11),
                               bg='#F8F9FA', relief=tk.FLAT)
        title_entry.pack(fill=tk.X, pady=(0, 15), ipady=5)
        title_entry.insert(0, event['titulo'])
        
        # Descrição
        tk.Label(main_frame, text="📄 Descrição:", bg='white', font=("Segoe UI", 10),
                fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        
        desc_text = tk.Text(main_frame, font=("Segoe UI", 10), height=4,
                           bg='#F8F9FA', relief=tk.FLAT)
        desc_text.pack(fill=tk.X, pady=(0, 15))
        desc_text.insert('1.0', event.get('descricao', ''))
        
        def save_edit():
            event['hora'] = f"{int(hour_var.get()):02d}:{int(minute_var.get()):02d}"
            event['titulo'] = title_entry.get().strip()
            event['descricao'] = desc_text.get('1.0', tk.END).strip()
            
            self.save_events()
            self.show_calendar()
            self.update_events_display(self.selected_date, self.current_month, self.current_year)
            dialog.destroy()
            messagebox.showinfo("Sucesso", "Evento atualizado!")
        
        tk.Button(main_frame, text="💾 Salvar Alterações", command=save_edit,
                 bg='#27AE60', fg='white', font=("Segoe UI", 10, "bold"),
                 relief=tk.FLAT, padx=20, pady=8).pack(pady=10)
    
    def delete_event(self, date_key, event_index):
        if messagebox.askyesno("Confirmar", "Deseja excluir este evento?"):
            del self.events[date_key][event_index]
            if not self.events[date_key]:
                del self.events[date_key]
            
            self.save_events()
            self.show_calendar()
            self.update_events_display(self.selected_date, self.current_month, self.current_year)
            messagebox.showinfo("Sucesso", "Evento excluído!")