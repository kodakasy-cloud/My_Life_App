import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re


class FinancasManager:
    def __init__(self, app):
        self.app = app
        self.current_filter = "all"
        self.search_term = ""
        self.categories = {
            "despesa": ["🍔 Alimentação", "🏠 Moradia", "🚗 Transporte", "💡 Contas", "🎮 Lazer", "🛍️ Compras", "🏥 Saúde", "📚 Educação", "🎁 Presentes", "📱 Tecnologia", "✈️ Viagem", "💼 Outros"],
            "receita": ["💰 Salário", "💼 Freelancer", "📈 Investimentos", "🎁 Presentes", "💸 Reembolsos", "🏆 Bônus", "💵 Outros"]
        }
        
    def open_financas(self):
        self.app.clear_content()
        
        # Container principal fixo
        main_container = tk.Frame(self.app.content_frame, bg='#F8F9FA')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Configurar grid para dividir a tela
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=2)  # Coluna esquerda (formulário)
        main_container.grid_columnconfigure(1, weight=3)  # Coluna direita (histórico)
        
        # ========== COLUNA ESQUERDA ==========
        left_column = tk.Frame(main_container, bg='#F8F9FA')
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Scroll para coluna esquerda
        left_canvas = tk.Canvas(left_column, bg='#F8F9FA', highlightthickness=0)
        left_scrollbar = tk.Scrollbar(left_column, orient="vertical", command=left_canvas.yview)
        left_scrollable = tk.Frame(left_canvas, bg='#F8F9FA')
        
        left_scrollable.bind("<Configure>", lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all")))
        left_canvas.create_window((0, 0), window=left_scrollable, anchor="nw")
        left_canvas.configure(yscrollcommand=left_scrollbar.set)
        
        left_canvas.pack(side="left", fill="both", expand=True)
        left_scrollbar.pack(side="right", fill="y")
        
        # ========== COLUNA DIREITA ==========
        right_column = tk.Frame(main_container, bg='#F8F9FA')
        right_column.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Conteúdo da coluna esquerda
        self.build_left_content(left_scrollable)
        
        # Conteúdo da coluna direita
        self.build_right_content(right_column)
    
    def build_left_content(self, parent):
        """Constrói o conteúdo da coluna esquerda (formulário e resumo)"""
        
        # Título
        title_frame = tk.Frame(parent, bg='#F8F9FA')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(title_frame, text="💰", font=("Segoe UI", 28), 
                bg='#F8F9FA').pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(title_frame, text="Controle Financeiro", font=("Segoe UI", 18, "bold"), 
                bg='#F8F9FA', fg='#2C3E50').pack(side=tk.LEFT)
        
        # Cards de resumo
        summary_frame = tk.Frame(parent, bg='#F8F9FA')
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        total_receitas = sum(float(item["valor"]) for item in self.app.financas if item["tipo"] == "receita")
        total_despesas = sum(float(item["valor"]) for item in self.app.financas if item["tipo"] == "despesa")
        saldo = total_receitas - total_despesas
        
        # Card Receitas
        receitas_card = self.create_summary_card(summary_frame, "💰 Receitas", 
                                                 f"R$ {total_receitas:,.2f}", "#27AE60")
        receitas_card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=3)
        
        # Card Despesas
        despesas_card = self.create_summary_card(summary_frame, "💸 Despesas", 
                                                 f"R$ {total_despesas:,.2f}", "#E74C3C")
        despesas_card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=3)
        
        # Card Saldo
        saldo_color = "#27AE60" if saldo >= 0 else "#E74C3C"
        saldo_card = self.create_summary_card(summary_frame, "💵 Saldo", 
                                              f"R$ {saldo:,.2f}", saldo_color)
        saldo_card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=3)
        
        # Frame para adicionar transações
        add_card = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        add_card.pack(fill=tk.X, pady=(0, 20))
        add_card.configure(highlightbackground='#E0E0E0', highlightthickness=1)
        
        add_inner = tk.Frame(add_card, bg='white')
        add_inner.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(add_inner, text="➕ Nova Transação", font=("Segoe UI", 13, "bold"), 
                bg='white', fg='#2C3E50').pack(anchor=tk.W, pady=(0, 15))
        
        # Formulário
        form_frame = tk.Frame(add_inner, bg='white')
        form_frame.pack(fill=tk.X)
        
        # Descrição
        tk.Label(form_frame, text="Descrição:", bg='white', font=("Segoe UI", 10), 
                fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        self.desc_entry = tk.Entry(form_frame, font=("Segoe UI", 11),
                                   bg='#F8F9FA', relief=tk.FLAT, highlightthickness=1,
                                   highlightcolor='#3498DB', highlightbackground='#D0D0D0')
        self.desc_entry.pack(fill=tk.X, pady=(0, 12), ipady=5)
        
        # Valor e Tipo em grid
        row_frame = tk.Frame(form_frame, bg='white')
        row_frame.pack(fill=tk.X, pady=(0, 12))
        
        # Valor
        valor_frame = tk.Frame(row_frame, bg='white')
        valor_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        tk.Label(valor_frame, text="Valor (R$):", bg='white', font=("Segoe UI", 10), 
                fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        
        valor_entry_frame = tk.Frame(valor_frame, bg='white')
        valor_entry_frame.pack(fill=tk.X)
        
        self.valor_entry = tk.Entry(valor_entry_frame, font=("Segoe UI", 11),
                                    bg='#F8F9FA', relief=tk.FLAT, highlightthickness=1,
                                    highlightcolor='#3498DB', highlightbackground='#D0D0D0')
        self.valor_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        tk.Label(valor_entry_frame, text=" (ex: 99.90)", font=("Segoe UI", 9), 
                bg='white', fg='#95A5A6').pack(side=tk.LEFT, padx=(5, 0))
        
        # Tipo
        tipo_frame = tk.Frame(row_frame, bg='white')
        tipo_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        tk.Label(tipo_frame, text="Tipo:", bg='white', font=("Segoe UI", 10), 
                fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        
        self.tipo_var = tk.StringVar(value="despesa")
        tipo_radio_frame = tk.Frame(tipo_frame, bg='white')
        tipo_radio_frame.pack(fill=tk.X)
        
        tk.Radiobutton(tipo_radio_frame, text="💸 Despesa", variable=self.tipo_var, value="despesa",
                      bg='white', font=("Segoe UI", 10), command=self.update_category_menu).pack(side=tk.LEFT, padx=(0, 10))
        tk.Radiobutton(tipo_radio_frame, text="💰 Receita", variable=self.tipo_var, value="receita",
                      bg='white', font=("Segoe UI", 10), command=self.update_category_menu).pack(side=tk.LEFT)
        
        # Categoria e Data em grid
        row_frame2 = tk.Frame(form_frame, bg='white')
        row_frame2.pack(fill=tk.X, pady=(0, 12))
        
        # Categoria
        cat_frame = tk.Frame(row_frame2, bg='white')
        cat_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        tk.Label(cat_frame, text="Categoria:", bg='white', font=("Segoe UI", 10), 
                fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        
        self.categoria_combo = ttk.Combobox(cat_frame, font=("Segoe UI", 10),
                                            values=self.categories["despesa"])
        self.categoria_combo.pack(fill=tk.X)
        self.categoria_combo.set("🍔 Alimentação")
        
        # Data
        data_frame = tk.Frame(row_frame2, bg='white')
        data_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        tk.Label(data_frame, text="Data:", bg='white', font=("Segoe UI", 10), 
                fg='#7F8C8D').pack(anchor=tk.W, pady=(0, 5))
        
        self.data_entry = tk.Entry(data_frame, font=("Segoe UI", 11),
                                   bg='#F8F9FA', relief=tk.FLAT, highlightthickness=1,
                                   highlightcolor='#3498DB', highlightbackground='#D0D0D0')
        self.data_entry.pack(fill=tk.X)
        self.data_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        # Botões
        btn_frame = tk.Frame(add_inner, bg='white')
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        add_btn = tk.Button(btn_frame, text="💾 Adicionar Transação", command=self.add_transaction,
                           bg='#27AE60', fg='white', font=("Segoe UI", 10, "bold"),
                           relief=tk.FLAT, cursor='hand2', padx=15, pady=8)
        add_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        clear_form_btn = tk.Button(btn_frame, text="🗑️ Limpar", command=self.clear_form,
                                   bg='#95A5A6', fg='white', font=("Segoe UI", 10, "bold"),
                                   relief=tk.FLAT, cursor='hand2', padx=15, pady=8)
        clear_form_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Gráfico de despesas
        self.create_expense_chart(parent)
    
    def build_right_content(self, parent):
        """Constrói o conteúdo da coluna direita (histórico)"""
        
        # Título do histórico
        title_frame = tk.Frame(parent, bg='#F8F9FA')
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(title_frame, text="📋 Histórico de Transações", font=("Segoe UI", 16, "bold"), 
                bg='#F8F9FA', fg='#2C3E50').pack(side=tk.LEFT)
        
        # Barra de ferramentas do histórico
        toolbar = tk.Frame(parent, bg='#F8F9FA')
        toolbar.pack(fill=tk.X, pady=(0, 15))
        
        # Filtros
        filter_frame = tk.Frame(toolbar, bg='#F8F9FA')
        filter_frame.pack(side=tk.LEFT)
        
        tk.Label(filter_frame, text="Filtrar:", bg='#F8F9FA', font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 8))
        
        self.filter_buttons = {}
        filters = [
            ("Todas", "all"),
            ("💰 Receitas", "receita"),
            ("💸 Despesas", "despesa")
        ]
        
        for text, f_type in filters:
            btn = tk.Button(filter_frame, text=text, 
                          command=lambda t=f_type: self.set_filter(t),
                          bg='#3498DB' if self.current_filter == f_type else '#ECF0F1',
                          fg='white' if self.current_filter == f_type else '#2C3E50',
                          font=("Segoe UI", 9), relief=tk.FLAT, cursor='hand2',
                          padx=12, pady=4)
            btn.pack(side=tk.LEFT, padx=3)
            self.filter_buttons[f_type] = btn
        
        # Busca
        search_frame = tk.Frame(toolbar, bg='#F8F9FA')
        search_frame.pack(side=tk.RIGHT)
        
        tk.Label(search_frame, text="🔍", bg='#F8F9FA', font=("Segoe UI", 11)).pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, font=("Segoe UI", 10), width=20,
                                     bg='white', relief=tk.FLAT, highlightthickness=1,
                                     highlightcolor='#3498DB', highlightbackground='#D0D0D0')
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.on_search())
        
        clear_btn = tk.Button(search_frame, text="✖", command=self.clear_search,
                             bg='#F8F9FA', fg='#95A5A6', font=("Segoe UI", 9),
                             relief=tk.FLAT, cursor='hand2')
        clear_btn.pack(side=tk.LEFT)
        
        # Container da lista de transações com scroll
        list_container = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        list_container.pack(fill=tk.BOTH, expand=True)
        list_container.configure(highlightbackground='#E0E0E0', highlightthickness=1)
        
        # Canvas para scroll
        canvas = tk.Canvas(list_container, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        self.transactions_frame = tk.Frame(canvas, bg='white')
        
        self.transactions_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_window = canvas.create_window((0, 0), window=self.transactions_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        def configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', configure_canvas)
        
        # Contador de transações
        self.counter_label = tk.Label(parent, text="", font=("Segoe UI", 9), 
                                      bg='#F8F9FA', fg='#7F8C8D')
        self.counter_label.pack(pady=(10, 0))
        
        # Atualizar lista
        self.update_transactions_display()
    
    def create_summary_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        card.configure(highlightbackground='#E0E0E0', highlightthickness=1)
        
        inner = tk.Frame(card, bg='white')
        inner.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)
        
        tk.Label(inner, text=title, font=("Segoe UI", 10), bg='white', 
                fg='#7F8C8D').pack()
        tk.Label(inner, text=value, font=("Segoe UI", 14, "bold"), 
                bg='white', fg=color).pack(pady=3)
        
        return card
    
    def create_expense_chart(self, parent):
        # Calcular despesas por categoria
        expenses_by_category = {}
        for trans in self.app.financas:
            if trans["tipo"] == "despesa":
                cat = trans.get("categoria", "🍔 Alimentação")
                expenses_by_category[cat] = expenses_by_category.get(cat, 0) + float(trans["valor"])
        
        if not expenses_by_category:
            return
        
        # Frame do gráfico
        chart_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=1)
        chart_frame.pack(fill=tk.X, pady=(20, 0))
        chart_frame.configure(highlightbackground='#E0E0E0', highlightthickness=1)
        
        chart_inner = tk.Frame(chart_frame, bg='white')
        chart_inner.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(chart_inner, text="📊 Principais Despesas", font=("Segoe UI", 12, "bold"), 
                bg='white', fg='#2C3E50').pack(anchor=tk.W, pady=(0, 10))
        
        # Criar barras horizontais
        sorted_categories = sorted(expenses_by_category.items(), key=lambda x: x[1], reverse=True)[:5]
        max_value = max(expenses_by_category.values())
        
        for cat, value in sorted_categories:
            percent = (value / max_value) * 100
            bar_frame = tk.Frame(chart_inner, bg='white')
            bar_frame.pack(fill=tk.X, pady=4)
            
            # Nome da categoria
            tk.Label(bar_frame, text=cat, font=("Segoe UI", 9), bg='white', 
                    width=14, anchor=tk.W).pack(side=tk.LEFT, padx=(0, 8))
            
            # Barra
            bar_canvas = tk.Canvas(bar_frame, height=20, bg='#ECF0F1', highlightthickness=0)
            bar_canvas.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            bar_canvas.create_rectangle(0, 0, (percent * 2.5), 20, fill='#E74C3C', width=0)
            
            # Valor
            tk.Label(bar_frame, text=f"R$ {value:,.2f}", font=("Segoe UI", 9, "bold"), 
                    bg='white', fg='#2C3E50', width=11, anchor=tk.E).pack(side=tk.RIGHT, padx=(8, 0))
    
    def update_category_menu(self):
        tipo = self.tipo_var.get()
        self.categoria_combo['values'] = self.categories[tipo]
        self.categoria_combo.set(self.categories[tipo][0])
    
    def set_filter(self, filter_type):
        self.current_filter = filter_type
        # Atualizar cores dos botões
        for f_type, btn in self.filter_buttons.items():
            if f_type == filter_type:
                btn.configure(bg='#3498DB', fg='white')
            else:
                btn.configure(bg='#ECF0F1', fg='#2C3E50')
        self.update_transactions_display()
    
    def on_search(self):
        self.search_term = self.search_entry.get().strip().lower()
        self.update_transactions_display()
    
    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.search_term = ""
        self.update_transactions_display()
    
    def clear_form(self):
        self.desc_entry.delete(0, tk.END)
        self.valor_entry.delete(0, tk.END)
        self.tipo_var.set("despesa")
        self.update_category_menu()
        self.data_entry.delete(0, tk.END)
        self.data_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
    
    def validate_and_convert_value(self, valor_str):
        """Valida e converte o valor para float"""
        valor_str = valor_str.strip()
        valor_str = valor_str.replace(',', '.')
        valor_str = re.sub(r'[^\d.-]', '', valor_str)
        
        if not valor_str:
            return None
        
        try:
            valor = float(valor_str)
            return valor
        except ValueError:
            return None
    
    def add_transaction(self):
        try:
            # Validar descrição
            desc = self.desc_entry.get().strip()
            if not desc:
                messagebox.showwarning("Aviso", "Digite uma descrição!")
                return
            
            # Validar valor
            valor_str = self.valor_entry.get().strip()
            if not valor_str:
                messagebox.showwarning("Aviso", "Digite um valor!")
                return
            
            valor = self.validate_and_convert_value(valor_str)
            if valor is None or valor <= 0:
                messagebox.showwarning("Aviso", "Valor inválido!\nUse formato: 99.90 ou 99,90")
                return
            
            # Validar data
            data = self.data_entry.get().strip()
            if not data:
                data = datetime.now().strftime("%d/%m/%Y")
            
            try:
                datetime.strptime(data, "%d/%m/%Y")
            except:
                messagebox.showwarning("Aviso", "Data inválida! Use DD/MM/AAAA")
                return
            
            tipo = self.tipo_var.get()
            categoria = self.categoria_combo.get()
            
            transacao = {
                "descricao": desc,
                "valor": valor,
                "tipo": tipo,
                "categoria": categoria,
                "data": data,
                "timestamp": datetime.now().timestamp()
            }
            
            self.app.financas.append(transacao)
            self.app.save_data()
            
            # Limpar formulário
            self.clear_form()
            
            # Recarregar tudo
            self.open_financas()
            
            messagebox.showinfo("Sucesso", f"✅ Transação adicionada!\n\n{desc}\nR$ {valor:,.2f}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar: {str(e)}")
    
    def get_filtered_transactions(self):
        filtered = self.app.financas.copy()
        
        if self.current_filter != "all":
            filtered = [t for t in filtered if t["tipo"] == self.current_filter]
        
        if self.search_term:
            filtered = [t for t in filtered if self.search_term in t["descricao"].lower() or 
                       self.search_term in t.get("categoria", "").lower()]
        
        # Ordenar por data (mais recentes primeiro)
        filtered.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        
        return filtered
    
    def update_transactions_display(self):
        # Limpar frame
        for widget in self.transactions_frame.winfo_children():
            widget.destroy()
        
        filtered = self.get_filtered_transactions()
        
        # Atualizar contador
        total = len(filtered)
        self.counter_label.config(text=f"Mostrando {total} transação(ões)")
        
        if not filtered:
            empty_frame = tk.Frame(self.transactions_frame, bg='white')
            empty_frame.pack(expand=True, fill=tk.BOTH, pady=50)
            
            if self.search_term or self.current_filter != "all":
                tk.Label(empty_frame, text="🔍", font=("Segoe UI", 48), 
                        bg='white', fg='#BDC3C7').pack()
                tk.Label(empty_frame, text="Nenhuma transação encontrada", 
                        font=("Segoe UI", 12), bg='white', fg='#7F8C8D').pack(pady=10)
            else:
                tk.Label(empty_frame, text="💰", font=("Segoe UI", 48), 
                        bg='white', fg='#BDC3C7').pack()
                tk.Label(empty_frame, text="Nenhuma transação ainda", 
                        font=("Segoe UI", 12), bg='white', fg='#7F8C8D').pack(pady=10)
                tk.Label(empty_frame, text="Adicione sua primeira transação", 
                        font=("Segoe UI", 10), bg='white', fg='#95A5A6').pack()
            return
        
        for trans in filtered:
            # Card da transação
            trans_card = tk.Frame(self.transactions_frame, bg='white', relief=tk.RAISED, bd=1)
            trans_card.pack(fill=tk.X, pady=5)
            trans_card.configure(highlightbackground='#E0E0E0', highlightthickness=1)
            
            inner_card = tk.Frame(trans_card, bg='white')
            inner_card.pack(fill=tk.X, padx=12, pady=10)
            
            # Ícone e tipo
            icon = "💰" if trans["tipo"] == "receita" else "💸"
            color = "#27AE60" if trans["tipo"] == "receita" else "#E74C3C"
            sinal = "+" if trans["tipo"] == "receita" else "-"
            
            # Linha superior
            top_frame = tk.Frame(inner_card, bg='white')
            top_frame.pack(fill=tk.X, pady=(0, 5))
            
            tk.Label(top_frame, text=icon, font=("Segoe UI", 16), bg='white').pack(side=tk.LEFT, padx=(0, 8))
            tk.Label(top_frame, text=trans["descricao"], font=("Segoe UI", 10, "bold"), 
                    bg='white', fg='#2C3E50').pack(side=tk.LEFT, expand=True, anchor=tk.W)
            tk.Label(top_frame, text=f"{sinal} R$ {float(trans['valor']):,.2f}", font=("Segoe UI", 12, "bold"), 
                    bg='white', fg=color).pack(side=tk.RIGHT)
            
            # Linha inferior
            bottom_frame = tk.Frame(inner_card, bg='white')
            bottom_frame.pack(fill=tk.X)
            
            tk.Label(bottom_frame, text=f"📂 {trans.get('categoria', 'Sem categoria')}", 
                    font=("Segoe UI", 8), bg='white', fg='#7F8C8D').pack(side=tk.LEFT)
            tk.Label(bottom_frame, text=f"📅 {trans['data']}", font=("Segoe UI", 8), 
                    bg='white', fg='#7F8C8D').pack(side=tk.RIGHT)
            
            # Botão de excluir
            delete_btn = tk.Button(inner_card, text="🗑️ Excluir", 
                                  command=lambda t=trans: self.delete_transaction(t),
                                  bg='#E74C3C', fg='white', font=("Segoe UI", 8),
                                  relief=tk.FLAT, cursor='hand2', padx=8, pady=2)
            delete_btn.pack(pady=(5, 0))
            
            # Efeito hover
            def on_enter(e, btn=delete_btn):
                btn.configure(bg='#C0392B')
            def on_leave(e, btn=delete_btn):
                btn.configure(bg='#E74C3C')
            delete_btn.bind('<Enter>', on_enter)
            delete_btn.bind('<Leave>', on_leave)
    
    def delete_transaction(self, transaction):
        if messagebox.askyesno("Confirmar Exclusão", 
                               "Tem certeza que deseja excluir esta transação?",
                               icon='warning'):
            self.app.financas.remove(transaction)
            self.app.save_data()
            self.open_financas()
            messagebox.showinfo("Sucesso", "🗑️ Transação excluída!")