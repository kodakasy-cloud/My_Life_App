import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class DiarioManager:
    def __init__(self, app):
        self.app = app
        
    def open_diario(self):
        self.app.clear_content()
        
        tk.Label(self.app.content_frame, text="Diário Pessoal", font=("Arial", 16, "bold"), 
                bg='white', fg='#333').pack(pady=20)
        
        # Frame para entrada de texto
        entry_frame = tk.Frame(self.app.content_frame, bg='white')
        entry_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(entry_frame, text="Nova entrada:", font=("Arial", 12), bg='white').pack(anchor=tk.W)
        
        text_entry = tk.Text(entry_frame, height=5, width=70, font=("Arial", 10))
        text_entry.pack(pady=5)
        
        def save_entry():
            entry_text = text_entry.get("1.0", tk.END).strip()
            if entry_text:
                entry = {
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "texto": entry_text
                }
                self.app.diario_entries.insert(0, entry)
                self.app.save_data()
                text_entry.delete("1.0", tk.END)
                update_entries_display()
                messagebox.showinfo("Sucesso", "Entrada salva no diário!")
        
        save_btn = tk.Button(entry_frame, text="Salvar", command=save_entry, 
                            bg='#4CAF50', fg='white', font=("Arial", 10))
        save_btn.pack(pady=5)
        
        # Frame para exibir entradas
        entries_frame = tk.Frame(self.app.content_frame, bg='white')
        entries_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)
        
        canvas = tk.Canvas(entries_frame, bg='white')
        scrollbar = tk.Scrollbar(entries_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def update_entries_display():
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            
            for entry in self.app.diario_entries:
                entry_container = tk.Frame(scrollable_frame, bg='#f9f9f9', relief=tk.RAISED, bd=1)
                entry_container.pack(fill=tk.X, pady=5)
                
                tk.Label(entry_container, text=f"📅 {entry['data']}", font=("Arial", 10, "bold"), 
                        bg='#f9f9f9', fg='#666').pack(anchor=tk.W, padx=10, pady=5)
                tk.Label(entry_container, text=entry['texto'], font=("Arial", 10), 
                        bg='#f9f9f9', wraplength=500, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=5)
        
        update_entries_display()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")