import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os


class PerfilManager:
    def __init__(self, app):
        self.app = app
        
    def edit_profile(self, event=None):
        # Janela de edição de perfil
        edit_window = tk.Toplevel(self.app.root)
        edit_window.title("Editar Perfil")
        edit_window.geometry("400x400")
        edit_window.configure(bg='white')
        
        # Nome
        tk.Label(edit_window, text="Nome:", font=("Arial", 12), bg='white').pack(pady=10)
        name_entry = tk.Entry(edit_window, font=("Arial", 12), width=30)
        name_entry.insert(0, self.app.user_data["nome"])
        name_entry.pack()
        
        # Idade
        tk.Label(edit_window, text="Idade:", font=("Arial", 12), bg='white').pack(pady=10)
        age_entry = tk.Entry(edit_window, font=("Arial", 12), width=30)
        age_entry.insert(0, self.app.user_data["idade"])
        age_entry.pack()
        
        # Foto
        tk.Label(edit_window, text="Foto (caminho do arquivo):", font=("Arial", 12), bg='white').pack(pady=10)
        photo_frame = tk.Frame(edit_window, bg='white')
        photo_frame.pack()
        
        photo_entry = tk.Entry(photo_frame, font=("Arial", 10), width=25)
        photo_entry.pack(side=tk.LEFT, padx=5)
        
        def browse_photo():
            filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
            if filename:
                photo_entry.delete(0, tk.END)
                photo_entry.insert(0, filename)
        
        browse_btn = tk.Button(photo_frame, text="Procurar", command=browse_photo, bg='#4CAF50', fg='white')
        browse_btn.pack(side=tk.LEFT)
        
        # Botão salvar
        def save_profile():
            self.app.user_data["nome"] = name_entry.get()
            self.app.user_data["idade"] = age_entry.get()
            self.app.user_data["foto_path"] = photo_entry.get() if photo_entry.get() else None
            
            # Atualizar display do perfil
            self.app.profile_name.config(text=self.app.user_data["nome"])
            self.app.profile_age.config(text=f"Idade: {self.app.user_data['idade'] if self.app.user_data['idade'] else 'Não informada'}")
            
            if self.app.user_data["foto_path"] and os.path.exists(self.app.user_data["foto_path"]):
                try:
                    img = Image.open(self.app.user_data["foto_path"])
                    img = img.resize((80, 80), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.app.profile_icon.config(image=photo, text="")
                    self.app.profile_icon.image = photo
                except:
                    messagebox.showerror("Erro", "Não foi possível carregar a imagem")
            
            self.app.save_data()
            edit_window.destroy()
            messagebox.showinfo("Sucesso", "Perfil atualizado com sucesso!")
        
        save_btn = tk.Button(edit_window, text="Salvar", command=save_profile, 
                            bg='#4CAF50', fg='white', font=("Arial", 12))
        save_btn.pack(pady=20)