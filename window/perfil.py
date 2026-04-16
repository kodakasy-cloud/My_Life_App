import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import os
import hashlib
from datetime import datetime
import re
import shutil
from pathlib import Path

class PerfilManager:
    def __init__(self, app):
        self.app = app
        self.temp_photo = None
        self.photo_preview = None
        self.preview_image = None
        
    def edit_profile(self, event=None):
        # Janela de edição de perfil com design moderno
        edit_window = tk.Toplevel(self.app.root)
        edit_window.title("✏️ Editar Perfil - Personalize sua experiência")
        edit_window.geometry("550x750")
        edit_window.configure(bg='#f0f2f5')
        edit_window.resizable(False, False)
        
        # Centralizar janela
        edit_window.transient(self.app.root)
        edit_window.grab_set()
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal com scroll
        main_frame = tk.Frame(edit_window, bg='#f0f2f5')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg='#f0f2f5', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f2f5')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=530)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Cabeçalho decorativo
        header_frame = tk.Frame(scrollable_frame, bg='#667eea', height=100)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="✏️ EDITAR PERFIL", 
                font=("Segoe UI", 18, "bold"), bg='#667eea', fg='white').pack(pady=30)
        
        # Frame principal do formulário
        form_frame = tk.Frame(scrollable_frame, bg='white', relief=tk.FLAT)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 25))
        
        # Adicionar borda arredondada simulada
        form_frame.configure(highlightthickness=1, highlightbackground='#e0e0e0')
        
        # ========== SEÇÃO FOTO ==========
        photo_frame = tk.LabelFrame(form_frame, text="📸 Foto do Perfil", 
                                    font=("Segoe UI", 11, "bold"),
                                    bg='white', fg='#333', padx=15, pady=15)
        photo_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Container da foto
        photo_container = tk.Frame(photo_frame, bg='white')
        photo_container.pack()
        
        # Preview da foto (circular)
        preview_container = tk.Frame(photo_container, bg='#e0e0e0', width=120, height=120,
                                     highlightthickness=2, highlightbackground='#667eea',
                                     highlightcolor='#667eea')
        preview_container.pack(pady=10)
        preview_container.pack_propagate(False)
        
        self.preview_label = tk.Label(preview_container, bg='#e0e0e0', text="📷", 
                                      font=("Segoe UI", 45))
        self.preview_label.pack(expand=True)
        
        # Carregar foto atual se existir
        current_photo = self.app.user_data.get("foto_path", "")
        if current_photo and os.path.exists(current_photo):
            self.load_circular_photo(current_photo, self.preview_label, 116)
        
        # Botões de ação da foto
        btn_frame = tk.Frame(photo_container, bg='white')
        btn_frame.pack(pady=10)
        
        def browse_photo():
            filename = filedialog.askopenfilename(
                title="Selecionar foto de perfil",
                filetypes=[
                    ("Imagens", "*.jpg *.jpeg *.png *.gif *.bmp"),
                    ("Todos os arquivos", "*.*")
                ]
            )
            if filename:
                # Validar tamanho (max 5MB)
                if os.path.getsize(filename) > 5 * 1024 * 1024:
                    messagebox.showwarning("Aviso", "A imagem deve ter no máximo 5MB!")
                    return
                
                self.temp_photo = filename
                self.load_circular_photo(filename, self.preview_label, 116)
        
        def remove_photo():
            self.temp_photo = None
            self.preview_label.config(text="📷", image='', font=("Segoe UI", 45))
            self.preview_label.image = None
        
        btn_style = {"font": ("Segoe UI", 9), "padx": 15, "pady": 5, "cursor": "hand2"}
        
        tk.Button(btn_frame, text="📁 Escolher Foto", command=browse_photo,
                 bg='#667eea', fg='white', relief=tk.FLAT, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Remover", command=remove_photo,
                 bg='#e74c3c', fg='white', relief=tk.FLAT, **btn_style).pack(side=tk.LEFT, padx=5)
        
        tk.Label(photo_frame, text="Formatos: JPG, PNG, GIF | Máx: 5MB",
                font=("Segoe UI", 8), bg='white', fg='#999').pack()
        
        # ========== SEÇÃO INFORMAÇÕES PESSOAIS ==========
        info_frame = tk.LabelFrame(form_frame, text="👤 Informações Pessoais", 
                                   font=("Segoe UI", 11, "bold"),
                                   bg='white', fg='#333', padx=15, pady=15)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Nome
        tk.Label(info_frame, text="Nome Completo:", font=("Segoe UI", 10, "bold"),
                bg='white', fg='#555').pack(anchor='w', pady=(0, 5))
        self.name_entry = tk.Entry(info_frame, font=("Segoe UI", 10), 
                                   bg='#f8f9fa', relief=tk.FLAT, bd=1)
        self.name_entry.pack(fill=tk.X, pady=(0, 12))
        self.name_entry.insert(0, self.app.user_data.get("nome", ""))
        self.name_entry.configure(highlightthickness=1, highlightcolor='#667eea',
                                  highlightbackground='#ddd')
        
        # Idade
        tk.Label(info_frame, text="Idade:", font=("Segoe UI", 10, "bold"),
                bg='white', fg='#555').pack(anchor='w', pady=(0, 5))
        self.age_entry = tk.Entry(info_frame, font=("Segoe UI", 10), 
                                  bg='#f8f9fa', relief=tk.FLAT, bd=1)
        self.age_entry.pack(fill=tk.X, pady=(0, 12))
        self.age_entry.insert(0, self.app.user_data.get("idade", ""))
        self.age_entry.configure(highlightthickness=1, highlightcolor='#667eea',
                                 highlightbackground='#ddd')
        
        # Email
        tk.Label(info_frame, text="E-mail:", font=("Segoe UI", 10, "bold"),
                bg='white', fg='#555').pack(anchor='w', pady=(0, 5))
        self.email_entry = tk.Entry(info_frame, font=("Segoe UI", 10), 
                                    bg='#f8f9fa', relief=tk.FLAT, bd=1)
        self.email_entry.pack(fill=tk.X, pady=(0, 12))
        self.email_entry.insert(0, self.app.user_data.get("email", ""))
        self.email_entry.configure(highlightthickness=1, highlightcolor='#667eea',
                                   highlightbackground='#ddd')
        
        # Telefone (novo)
        tk.Label(info_frame, text="Telefone:", font=("Segoe UI", 10, "bold"),
                bg='white', fg='#555').pack(anchor='w', pady=(0, 5))
        self.phone_entry = tk.Entry(info_frame, font=("Segoe UI", 10), 
                                    bg='#f8f9fa', relief=tk.FLAT, bd=1)
        self.phone_entry.pack(fill=tk.X, pady=(0, 12))
        self.phone_entry.insert(0, self.app.user_data.get("telefone", ""))
        self.phone_entry.configure(highlightthickness=1, highlightcolor='#667eea',
                                   highlightbackground='#ddd')
        
        # Bio
        tk.Label(info_frame, text="Bio / Sobre mim:", font=("Segoe UI", 10, "bold"),
                bg='white', fg='#555').pack(anchor='w', pady=(0, 5))
        self.bio_text = tk.Text(info_frame, height=3, font=("Segoe UI", 10),
                                bg='#f8f9fa', relief=tk.FLAT, bd=1, wrap=tk.WORD)
        self.bio_text.pack(fill=tk.X, pady=(0, 5))
        self.bio_text.insert("1.0", self.app.user_data.get("bio", ""))
        self.bio_text.configure(highlightthickness=1, highlightcolor='#667eea',
                                highlightbackground='#ddd')
        
        # Contador de caracteres da bio
        self.bio_counter = tk.Label(info_frame, text="0/200 caracteres", 
                                    font=("Segoe UI", 8), bg='white', fg='#999')
        self.bio_counter.pack(anchor='e')
        
        def update_bio_counter(event=None):
            count = len(self.bio_text.get("1.0", tk.END).strip())
            self.bio_counter.config(text=f"{count}/200 caracteres")
            if count > 200:
                self.bio_counter.config(fg='red')
            else:
                self.bio_counter.config(fg='#999')
        
        self.bio_text.bind('<KeyRelease>', update_bio_counter)
        update_bio_counter()
        
        # ========== SEÇÃO PREFERÊNCIAS ==========
        prefs_frame = tk.LabelFrame(form_frame, text="⚙️ Preferências", 
                                    font=("Segoe UI", 11, "bold"),
                                    bg='white', fg='#333', padx=15, pady=15)
        prefs_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Tema
        tk.Label(prefs_frame, text="Tema da Interface:", font=("Segoe UI", 10, "bold"),
                bg='white', fg='#555').pack(anchor='w', pady=(0, 5))
        
        self.theme_var = tk.StringVar(value=self.app.user_data.get("tema", "Claro"))
        theme_options_frame = tk.Frame(prefs_frame, bg='white')
        theme_options_frame.pack(fill=tk.X, pady=(0, 12))
        
        themes = [
            ("🌞 Claro", "Claro"),
            ("🌙 Escuro", "Escuro"),
            ("🎨 Sistema", "Sistema")
        ]
        
        for text, value in themes:
            rb = tk.Radiobutton(theme_options_frame, text=text, variable=self.theme_var,
                               value=value, bg='white', font=("Segoe UI", 9),
                               cursor="hand2", selectcolor='white')
            rb.pack(side=tk.LEFT, padx=15)
        
        # Notificações
        self.notifications_var = tk.BooleanVar(value=self.app.user_data.get("notificacoes", True))
        notif_frame = tk.Frame(prefs_frame, bg='white')
        notif_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Checkbutton(notif_frame, text="🔔 Receber notificações", 
                      variable=self.notifications_var,
                      bg='white', font=("Segoe UI", 10), cursor="hand2").pack(anchor='w')
        
        # Idioma (novo)
        tk.Label(prefs_frame, text="Idioma:", font=("Segoe UI", 10, "bold"),
                bg='white', fg='#555').pack(anchor='w', pady=(10, 5))
        
        self.language_var = tk.StringVar(value=self.app.user_data.get("idioma", "Português"))
        language_combo = ttk.Combobox(prefs_frame, textvariable=self.language_var,
                                      values=["Português", "English", "Español"],
                                      state="readonly", font=("Segoe UI", 9))
        language_combo.pack(fill=tk.X)
        
        # ========== SEÇÃO SEGURANÇA ==========
        security_frame = tk.LabelFrame(form_frame, text="🔒 Segurança", 
                                       font=("Segoe UI", 11, "bold"),
                                       bg='white', fg='#333', padx=15, pady=15)
        security_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Alterar senha
        tk.Label(security_frame, text="Alterar Senha:", font=("Segoe UI", 10, "bold"),
                bg='white', fg='#555').pack(anchor='w', pady=(0, 5))
        
        pass_frame = tk.Frame(security_frame, bg='white')
        pass_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.new_pass_entry = tk.Entry(pass_frame, font=("Segoe UI", 10), 
                                       width=25, relief=tk.FLAT, bd=1, show="•")
        self.new_pass_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.new_pass_entry.configure(highlightthickness=1, highlightcolor='#667eea',
                                      highlightbackground='#ddd')
        
        tk.Button(pass_frame, text="Atualizar Senha", command=self.change_password,
                 bg='#3498db', fg='white', font=("Segoe UI", 9), relief=tk.FLAT,
                 cursor="hand2", padx=15, pady=5).pack(side=tk.LEFT)
        
        # Força da senha indicator
        self.password_strength = tk.Label(security_frame, text="", 
                                          font=("Segoe UI", 8), bg='white')
        self.password_strength.pack(anchor='w', pady=(5, 0))
        
        def check_password_strength(event=None):
            password = self.new_pass_entry.get()
            strength = self.calculate_password_strength(password)
            colors = {"Fraca": "#e74c3c", "Média": "#f39c12", "Forte": "#2ecc71"}
            if strength:
                self.password_strength.config(text=f"Força: {strength}", fg=colors.get(strength, "#999"))
            else:
                self.password_strength.config(text="")
        
        self.new_pass_entry.bind('<KeyRelease>', check_password_strength)
        
        # ========== BOTÕES DE AÇÃO ==========
        action_frame = tk.Frame(form_frame, bg='white')
        action_frame.pack(pady=(10, 15))
        
        def save_profile():
            if self.validate_form():
                self.save_profile_data()
                edit_window.destroy()
        
        def cancel_edit():
            if messagebox.askyesno("Confirmar", "Deseja cancelar as alterações?"):
                edit_window.destroy()
        
        # Botões estilizados
        save_btn = tk.Button(action_frame, text="💾 SALVAR ALTERAÇÕES", command=save_profile,
                            bg='#2ecc71', fg='white', font=("Segoe UI", 11, "bold"),
                            padx=35, pady=10, cursor="hand2", relief=tk.FLAT)
        save_btn.pack(side=tk.LEFT, padx=10)
        
        cancel_btn = tk.Button(action_frame, text="❌ CANCELAR", command=cancel_edit,
                              bg='#e74c3c', fg='white', font=("Segoe UI", 11, "bold"),
                              padx=35, pady=10, cursor="hand2", relief=tk.FLAT)
        cancel_btn.pack(side=tk.LEFT, padx=10)
        
        # Efeitos hover
        def on_enter(btn, color):
            btn.configure(bg=color)
        
        def on_leave(btn, color):
            btn.configure(bg=color)
        
        save_btn.bind("<Enter>", lambda e: on_enter(save_btn, '#27ae60'))
        save_btn.bind("<Leave>", lambda e: on_leave(save_btn, '#2ecc71'))
        cancel_btn.bind("<Enter>", lambda e: on_enter(cancel_btn, '#c0392b'))
        cancel_btn.bind("<Leave>", lambda e: on_leave(cancel_btn, '#e74c3c'))
        
        # Atalhos do teclado
        edit_window.bind('<Return>', lambda e: save_profile())
        edit_window.bind('<Escape>', lambda e: cancel_edit())
    
    def load_circular_photo(self, photo_path, label, size):
        """Carrega e redimensiona a foto para preview circular com borda"""
        try:
            img = Image.open(photo_path)
            
            # Converter para RGBA se necessário
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Redimensionar
            img = img.resize((size, size), Image.Resampling.LANCZOS)
            
            # Criar máscara circular
            mask = Image.new('L', (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)
            
            # Aplicar máscara
            circular_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            circular_img.paste(img, (0, 0))
            circular_img.putalpha(mask)
            
            # Adicionar borda
            bordered_size = size + 8
            bordered = Image.new('RGBA', (bordered_size, bordered_size), (102, 126, 234, 255))
            bordered.paste(circular_img, (4, 4), circular_img)
            
            photo = ImageTk.PhotoImage(bordered)
            label.config(image=photo, text="")
            label.image = photo
            
        except Exception as e:
            print(f"Erro ao carregar foto: {e}")
            label.config(text="📷", image='', font=("Segoe UI", 45))
    
    def calculate_password_strength(self, password):
        """Calcula a força da senha"""
        if len(password) == 0:
            return ""
        
        score = 0
        if len(password) >= 8:
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[0-9]', password):
            score += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        
        if score <= 2:
            return "Fraca"
        elif score <= 4:
            return "Média"
        else:
            return "Forte"
    
    def validate_form(self):
        """Valida os campos do formulário"""
        nome = self.name_entry.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, insira seu nome!")
            self.name_entry.focus()
            return False
        
        if len(nome) < 3:
            messagebox.showwarning("Aviso", "Nome deve ter pelo menos 3 caracteres!")
            self.name_entry.focus()
            return False
        
        idade = self.age_entry.get().strip()
        if idade:
            try:
                idade_num = int(idade)
                if idade_num < 0 or idade_num > 150:
                    messagebox.showwarning("Aviso", "Idade inválida (0-150)!")
                    self.age_entry.focus()
                    return False
            except ValueError:
                messagebox.showwarning("Aviso", "Idade deve ser um número válido!")
                self.age_entry.focus()
                return False
        
        email = self.email_entry.get().strip()
        if email:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                messagebox.showwarning("Aviso", "E-mail inválido!\nExemplo: nome@dominio.com")
                self.email_entry.focus()
                return False
        
        # Validar bio (max 200 caracteres)
        bio = self.bio_text.get("1.0", tk.END).strip()
        if len(bio) > 200:
            messagebox.showwarning("Aviso", "A bio deve ter no máximo 200 caracteres!")
            self.bio_text.focus()
            return False
        
        return True
    
    def change_password(self):
        """Altera a senha do usuário"""
        new_password = self.new_pass_entry.get()
        if not new_password:
            messagebox.showwarning("Aviso", "Digite uma nova senha!")
            self.new_pass_entry.focus()
            return
        
        if len(new_password) < 6:
            messagebox.showwarning("Aviso", "A senha deve ter pelo menos 6 caracteres!")
            self.new_pass_entry.focus()
            return
        
        # Verificar força da senha
        strength = self.calculate_password_strength(new_password)
        if strength == "Fraca":
            if not messagebox.askyesno("Aviso", "Sua senha está fraca. Deseja continuar mesmo assim?"):
                return
        
        # Hash da senha
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        self.app.user_data["senha_hash"] = password_hash
        self.app.user_data["ultima_alteracao_senha"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        messagebox.showinfo("Sucesso", "✅ Senha alterada com sucesso!")
        self.new_pass_entry.delete(0, tk.END)
        self.password_strength.config(text="")
        self.app.save_data()
    
    def save_profile_data(self):
        """Salva todos os dados do perfil"""
        # Validar bio novamente
        bio = self.bio_text.get("1.0", tk.END).strip()
        if len(bio) > 200:
            bio = bio[:200]
        
        # Atualizar dados do usuário
        self.app.user_data["nome"] = self.name_entry.get().strip()
        self.app.user_data["idade"] = self.age_entry.get().strip()
        self.app.user_data["email"] = self.email_entry.get().strip()
        self.app.user_data["telefone"] = self.phone_entry.get().strip()
        self.app.user_data["bio"] = bio
        self.app.user_data["tema"] = self.theme_var.get()
        self.app.user_data["notificacoes"] = self.notifications_var.get()
        self.app.user_data["idioma"] = self.language_var.get()
        self.app.user_data["ultima_atualizacao"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Salvar foto se foi alterada
        if self.temp_photo:
            # Criar diretório de fotos se não existir
            photos_dir = Path("profile_photos")
            photos_dir.mkdir(exist_ok=True)
            
            # Gerar nome único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"profile_{timestamp}.png"
            filepath = photos_dir / filename
            
            try:
                img = Image.open(self.temp_photo)
                img = img.resize((300, 300), Image.Resampling.LANCZOS)
                img.save(filepath, "PNG")
                
                # Remover foto antiga se existir
                old_photo = self.app.user_data.get("foto_path", "")
                if old_photo and os.path.exists(old_photo) and old_photo != str(filepath):
                    try:
                        os.remove(old_photo)
                    except:
                        pass
                
                self.app.user_data["foto_path"] = str(filepath)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar foto: {e}")
        
        # Atualizar display do perfil na interface principal
        self.update_profile_display()
        
        # Salvar dados
        self.app.save_data()
        messagebox.showinfo("Sucesso", "✅ Perfil atualizado com sucesso!")
    
    def update_profile_display(self):
        """Atualiza a exibição do perfil na interface principal"""
        # Atualizar nome
        if hasattr(self.app, 'profile_name'):
            self.app.profile_name.config(text=self.app.user_data["nome"])
        
        # Atualizar idade
        if hasattr(self.app, 'profile_age'):
            idade = self.app.user_data.get("idade", "")
            if idade:
                idade_text = f"Idade: {idade} anos"
            else:
                idade_text = "Idade não informada"
            self.app.profile_age.config(text=idade_text)
        
        # Atualizar email
        if hasattr(self.app, 'profile_email'):
            email = self.app.user_data.get("email", "")
            if email:
                self.app.profile_email.config(text=f"📧 {email}")
        
        # Atualizar foto
        if hasattr(self.app, 'profile_icon'):
            photo_path = self.app.user_data.get("foto_path", "")
            if photo_path and os.path.exists(photo_path):
                try:
                    self.load_circular_photo(photo_path, self.app.profile_icon, 80)
                except:
                    self.app.profile_icon.config(text="👤", font=("Segoe UI", 40), image='')
            else:
                self.app.profile_icon.config(text="👤", font=("Segoe UI", 40), image='')

# Classe utilitária para gerar avatar a partir de iniciais
class AvatarGenerator:
    @staticmethod
    def generate_avatar(name, size=100):
        """Gera um avatar com as iniciais do nome"""
        import random
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', 
                  '#98D8C8', '#F7D794', '#786FA6', '#F19066', '#F5CD79']
        
        # Pegar iniciais
        words = name.split()
        if len(words) >= 2:
            initials = words[0][0].upper() + words[1][0].upper()
        elif len(words) == 1:
            initials = words[0][0].upper()
        else:
            initials = "U"
        
        # Cor baseada no nome
        color_index = hash(name) % len(colors)
        bg_color = colors[color_index]
        
        # Criar imagem
        img = Image.new('RGB', (size, size), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Desenhar texto
        try:
            from PIL import ImageFont
            font_size = size // 3
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Centralizar texto
        try:
            bbox = draw.textbbox((0, 0), initials, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except:
            text_width = len(initials) * font_size // 2
            text_height = font_size
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        draw.text((x, y), initials, fill='white', font=font)
        
        return img