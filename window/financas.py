import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class FinancasManager:
    def __init__(self, app):
        self.app = app
        
    def open_financas(self):
        self.app.clear_content()
        
        tk.Label(self.app.content_frame, text="Controle Financeiro", font=("Arial", 16, "bold"), 
                bg='white', fg='#333').pack(pady=20)
        
        # Resumo financeiro
        total_receitas = sum(item["valor"] for item in self.app.financas if item["tipo"] == "receita")
        total_despesas = sum(item["valor"] for item in self.app.financas if item["tipo"] == "despesa")
        saldo = total_receitas - total_despesas
        
        summary_frame = tk.Frame(self.app.content_frame, bg='#e8f5e9', relief=tk.RAISED, bd=2)
        summary_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(summary_frame, text="Resumo Financeiro", font=("Arial", 12, "bold"), 
                bg='#e8f5e9', fg='#333').pack(pady=10)
        
        tk.Label(summary_frame, text=f"💰 Receitas: R$ {total_receitas:.2f}", 
                font=("Arial", 10), bg='#e8f5e9', fg='green').pack()
        tk.Label(summary_frame, text=f"💸 Despesas: R$ {total_despesas:.2f}", 
                font=("Arial", 10), bg='#e8f5e9', fg='red').pack()
        tk.Label(summary_frame, text=f"💵 Saldo: R$ {saldo:.2f}", 
                font=("Arial", 10, "bold"), bg='#e8f5e9', fg='blue').pack(pady=5)
        
        # Frame para adicionar transações
        add_frame = tk.Frame(self.app.content_frame, bg='white')
        add_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(add_frame, text="Descrição:", font=("Arial", 10), bg='white').grid(row=0, column=0, pady=5)
        desc_entry = tk.Entry(add_frame, font=("Arial", 10), width=20)
        desc_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(add_frame, text="Valor:", font=("Arial", 10), bg='white').grid(row=0, column=2, pady=5, padx=10)
        valor_entry = tk.Entry(add_frame, font=("Arial", 10), width=10)
        valor_entry.grid(row=0, column=3, pady=5)
        
        tk.Label(add_frame, text="Tipo:", font=("Arial", 10), bg='white').grid(row=0, column=4, pady=5, padx=10)
        tipo_var = tk.StringVar(value="despesa")
        tipo_menu = ttk.Combobox(add_frame, textvariable=tipo_var, values=["despesa", "receita"], width=10)
        tipo_menu.grid(row=0, column=5, pady=5)
        
        def add_transaction():
            try:
                desc = desc_entry.get().strip()
                valor = float(valor_entry.get())
                tipo = tipo_var.get()
                
                if desc and valor > 0:
                    transacao = {
                        "descricao": desc,
                        "valor": valor,
                        "tipo": tipo,
                        "data": datetime.now().strftime("%d/%m/%Y")
                    }
                    self.app.financas.append(transacao)
                    self.app.save_data()
                    desc_entry.delete(0, tk.END)
                    valor_entry.delete(0, tk.END)
                    update_transactions_display()
                    # Atualizar resumo
                    self.open_financas()
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido!")
        
        add_btn = tk.Button(add_frame, text="Adicionar", command=add_transaction, 
                           bg='#4CAF50', fg='white', font=("Arial", 10))
        add_btn.grid(row=0, column=6, pady=5, padx=10)
        
        # Lista de transações
        trans_frame = tk.Frame(self.app.content_frame, bg='white')
        trans_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)
        
        def update_transactions_display():
            for widget in trans_frame.winfo_children():
                widget.destroy()
            
            for trans in self.app.financas:
                trans_container = tk.Frame(trans_frame, bg='#f9f9f9', relief=tk.RAISED, bd=1)
                trans_container.pack(fill=tk.X, pady=2)
                
                cor = 'red' if trans["tipo"] == "despesa" else 'green'
                sinal = "-" if trans["tipo"] == "despesa" else "+"
                
                tk.Label(trans_container, text=trans["descricao"], font=("Arial", 10), 
                        bg='#f9f9f9', width=20, anchor=tk.W).pack(side=tk.LEFT, padx=10)
                tk.Label(trans_container, text=f"{sinal} R$ {trans['valor']:.2f}", 
                        font=("Arial", 10, "bold"), bg='#f9f9f9', fg=cor).pack(side=tk.LEFT, padx=10)
                tk.Label(trans_container, text=trans["data"], font=("Arial", 8), 
                        bg='#f9f9f9', fg='#666').pack(side=tk.RIGHT, padx=10)
        
        update_transactions_display()