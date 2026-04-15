import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class TarefasManager:
    def __init__(self, app):
        self.app = app
        
    def open_tarefas(self):
        self.app.clear_content()
        
        tk.Label(self.app.content_frame, text="Lista de Tarefas", font=("Arial", 16, "bold"), 
                bg='white', fg='#333').pack(pady=20)
        
        # Frame para adicionar tarefas
        add_frame = tk.Frame(self.app.content_frame, bg='white')
        add_frame.pack(pady=10, padx=20, fill=tk.X)
        
        task_entry = tk.Entry(add_frame, font=("Arial", 12), width=50)
        task_entry.pack(side=tk.LEFT, padx=5)
        
        def add_task():
            task_text = task_entry.get().strip()
            if task_text:
                task = {
                    "texto": task_text,
                    "concluida": False,
                    "data_criacao": datetime.now().strftime("%d/%m/%Y")
                }
                self.app.tasks.append(task)
                self.app.save_data()
                task_entry.delete(0, tk.END)
                update_tasks_display()
        
        add_btn = tk.Button(add_frame, text="Adicionar Tarefa", command=add_task, 
                           bg='#4CAF50', fg='white', font=("Arial", 10))
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame para lista de tarefas
        tasks_frame = tk.Frame(self.app.content_frame, bg='white')
        tasks_frame.pack(fill=tk.BOTH, expand=True, pady=20, padx=20)
        
        def update_tasks_display():
            for widget in tasks_frame.winfo_children():
                widget.destroy()
            
            for i, task in enumerate(self.app.tasks):
                task_frame = tk.Frame(tasks_frame, bg='white')
                task_frame.pack(fill=tk.X, pady=5)
                
                var = tk.BooleanVar(value=task["concluida"])
                cb = tk.Checkbutton(task_frame, text=task["texto"], variable=var, bg='white',
                                   command=lambda idx=i: toggle_task(idx))
                cb.pack(side=tk.LEFT)
                
                if task["concluida"]:
                    cb.config(fg='gray')
                
                del_btn = tk.Button(task_frame, text="❌", command=lambda idx=i: delete_task(idx),
                                   bg='white', fg='red', font=("Arial", 8))
                del_btn.pack(side=tk.RIGHT, padx=5)
                
                tk.Label(task_frame, text=f"Criada em: {task['data_criacao']}", 
                        font=("Arial", 8), bg='white', fg='#666').pack(side=tk.RIGHT, padx=10)
        
        def toggle_task(index):
            self.app.tasks[index]["concluida"] = not self.app.tasks[index]["concluida"]
            self.app.save_data()
            update_tasks_display()
        
        def delete_task(index):
            if messagebox.askyesno("Confirmar", "Deseja excluir esta tarefa?"):
                del self.app.tasks[index]
                self.app.save_data()
                update_tasks_display()
        
        update_tasks_display()