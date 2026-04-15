import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class AnotacoesManager:
    def __init__(self, app):
        self.app = app
        
    def open_anotacoes(self):
        self.app.clear_content()
        
        tk.Label(self.app.content_frame, text="Anotações Rápidas", font=("Arial", 16, "bold"), 
                bg='white', fg='#333').pack(pady=20)
        
        # Frame para adicionar anotações
        add_frame = tk.Frame(self.app.content_frame, bg='white')
        add_frame.pack(pady=10, padx=20, fill=tk.X)
        
        note_entry = tk.Entry(add_frame, font=("Arial", 12), width=60)
        note_entry.pack(side=tk.LEFT, padx=5)
        
        def add_note():
            note_text = note_entry.get().strip()
            if note_text:
                note = {
                    "texto": note_text,
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M")
                }
                self.app.notas.append(note)
                self.app.save_data()
                note_entry.delete(0, tk.END)
                update_notes_display()
        
        add_btn = tk.Button(add_frame, text="Adicionar Anotação", command=add_note, 
                           bg='#4CAF50', fg='white', font=("Arial", 10))
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Lista de anotações
        notes_frame = tk.Frame(self.app.content_frame, bg='white')
        notes_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)
        
        def update_notes_display():
            for widget in notes_frame.winfo_children():
                widget.destroy()
            
            for i, note in enumerate(self.app.notas):
                note_container = tk.Frame(notes_frame, bg='#fff9c4', relief=tk.RAISED, bd=1)
                note_container.pack(fill=tk.X, pady=5)
                
                tk.Label(note_container, text=f"📝 {note['texto']}", font=("Arial", 10), 
                        bg='#fff9c4', wraplength=500, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=5)
                tk.Label(note_container, text=f"📅 {note['data']}", font=("Arial", 8), 
                        bg='#fff9c4', fg='#666').pack(anchor=tk.W, padx=10, pady=2)
                
                del_btn = tk.Button(note_container, text="❌", command=lambda idx=i: delete_note(idx),
                                   bg='#fff9c4', fg='red', font=("Arial", 8))
                del_btn.pack(anchor=tk.E, padx=5, pady=2)
        
        def delete_note(index):
            if messagebox.askyesno("Confirmar", "Deseja excluir esta anotação?"):
                del self.app.notas[index]
                self.app.save_data()
                update_notes_display()
        
        update_notes_display()