import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw
import json
import os
import hashlib
from datetime import datetime
import math

class ModernButton(tk.Frame):
    """Botão moderno com animação - Versão corrigida"""
    def __init__(self, parent, text, command, color="#2196F3", hover_color="#1976D2", 
                 icon="", width=200, height=45):
        super().__init__(parent, width=width, height=height, bg=parent.cget('bg') if hasattr(parent, 'cget') else '#1a1a2e')
        self.pack_propagate(False)
        
        self.command = command
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.icon = icon
        self.is_hovering = False
        
        # Criar botão interno
        self.button = tk.Label(self, text=f"{icon} {text}" if icon else text, 
                               font=("Segoe UI", 11, "bold"),
                               bg=color, fg="white", cursor="hand2")
        self.button.pack(fill=tk.BOTH, expand=True)
        
        # Bind events
        self.button.bind("<Enter>", self.on_enter)
        self.button.bind("<Leave>", self.on_leave)
        self.button.bind("<Button-1>", self.on_click)
    
    def on_enter(self, event):
        self.button.config(bg=self.hover_color)
    
    def on_leave(self, event):
        self.button.config(bg=self.color)
    
    def on_click(self, event):
        if self.command:
            self.command()

class PremiumProfileSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Premium Profile System ✨")
        self.root.geometry("1400x850")
        self.root.configure(bg='#1a1a2e')
        
        # Cores do sistema (apenas cores sólidas, sem transparência)
        self.colors = {
            'bg': '#1a1a2e',
            'card': '#16213e',
            'card_light': '#1f2a4a',
            'accent': '#e94560',
            'accent_hover': '#ff6b6b',
            'text': '#ffffff',
            'text_secondary': '#a0a0b0',
            'success': '#4CAF50',
            'success_hover': '#66BB6A',
            'warning': '#FF9800',
            'warning_hover': '#FFB74D',
            'danger': '#F44336',
            'danger_hover': '#EF5350'
        }
        
        # Dados do perfil
        self.profile_data = self.init_profile_data()
        
        # Carregar dados
        self.load_data()
        
        # Mostrar tela de login
        self.show_login_screen()
    
    def init_profile_data(self):
        return {
            "nome": "Usuário Premium",
            "email": "usuario@premium.com",
            "telefone": "(11) 99999-9999",
            "bio": "✨ Bem-vindo ao meu perfil premium! ✨\n\nDesign moderno com animações suaves.",
            "data_nascimento": "01/01/1990",
            "localizacao": "São Paulo, Brasil",
            "profissao": "Designer/Desenvolvedor",
            "site": "www.meusite.com",
            "senha_hash": hashlib.sha256("123456".encode()).hexdigest(),
            "tema": "dark",
            "foto_path": None,
            "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "ultimo_acesso": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "estatisticas": {
                "total_acessos": 1,
                "ultimo_login": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
        }
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def show_login_screen(self):
        """Tela de login moderna"""
        self.clear_window()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Card de login centralizado
        card = tk.Frame(main_frame, bg=self.colors['card'], relief=tk.RAISED, bd=1)
        card.place(relx=0.5, rely=0.5, anchor='center', width=450, height=550)
        
        # Borda superior colorida
        top_bar = tk.Frame(card, bg=self.colors['accent'], height=5)
        top_bar.pack(fill=tk.X)
        
        # Ícone
        icon_label = tk.Label(card, text="✨", font=("Segoe UI Emoji", 60), 
                              bg=self.colors['card'], fg=self.colors['accent'])
        icon_label.pack(pady=30)
        
        # Título
        tk.Label(card, text="PREMIUM PROFILE", font=("Segoe UI", 20, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack()
        tk.Label(card, text="Faça login para continuar", font=("Segoe UI", 10),
                bg=self.colors['card'], fg=self.colors['text_secondary']).pack(pady=5)
        
        # Formulário
        form_frame = tk.Frame(card, bg=self.colors['card'])
        form_frame.pack(pady=40, padx=40, fill=tk.X)
        
        # Campo senha
        tk.Label(form_frame, text="SENHA", font=("Segoe UI", 10, "bold"),
                bg=self.colors['card'], fg=self.colors['text_secondary']).pack(anchor=tk.W, pady=(0,5))
        
        self.password_entry = tk.Entry(form_frame, font=("Segoe UI", 12),
                                       show="●", bg=self.colors['card_light'],
                                       fg=self.colors['text'], relief=tk.FLAT,
                                       insertbackground=self.colors['text'])
        self.password_entry.pack(fill=tk.X, ipady=10)
        self.password_entry.bind("<Return>", lambda e: self.do_login())
        
        # Mostrar senha
        show_var = tk.BooleanVar(value=False)
        
        def toggle_show():
            self.password_entry.config(show="" if show_var.get() else "●")
        
        cb_frame = tk.Frame(form_frame, bg=self.colors['card'])
        cb_frame.pack(anchor=tk.W, pady=10)
        
        tk.Checkbutton(cb_frame, text="Mostrar senha", variable=show_var,
                      command=toggle_show, bg=self.colors['card'],
                      fg=self.colors['text_secondary'], selectcolor=self.colors['card']).pack()
        
        # Botão login
        login_btn = ModernButton(form_frame, "ENTRAR", self.do_login,
                                color=self.colors['accent'], hover_color=self.colors['accent_hover'],
                                width=370, height=45)
        login_btn.pack(pady=20)
        
        # Informação
        info_label = tk.Label(card, text="Senha padrão: 123456", font=("Segoe UI", 9),
                             bg=self.colors['card'], fg=self.colors['text_secondary'])
        info_label.pack(pady=10)
        
        # Mensagem de erro
        self.error_label = tk.Label(card, text="", font=("Segoe UI", 9),
                                   bg=self.colors['card'], fg=self.colors['danger'])
        self.error_label.pack()
    
    def do_login(self):
        """Processa login"""
        password = self.password_entry.get()
        
        if self.hash_password(password) == self.profile_data["senha_hash"]:
            # Atualizar estatísticas
            self.profile_data["estatisticas"]["total_acessos"] += 1
            self.profile_data["estatisticas"]["ultimo_login"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            self.profile_data["ultimo_acesso"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            self.save_data()
            
            messagebox.showinfo("✅ Sucesso", f"Bem-vindo(a), {self.profile_data['nome']}!")
            self.show_main_profile()
        else:
            self.error_label.config(text="❌ Senha incorreta! Tente novamente.")
            self.password_entry.delete(0, tk.END)
            self.shake_widget(self.password_entry)
    
    def shake_widget(self, widget):
        """Efeito de tremor"""
        original_x = widget.winfo_x()
        
        def shake(count=0):
            if count < 10:
                offset = 8 if count % 2 == 0 else -8
                widget.place_configure(x=original_x + offset)
                self.root.after(30, lambda: shake(count + 1))
            else:
                widget.place_configure(x=original_x)
        
        shake()
    
    def show_main_profile(self):
        """Tela principal do perfil"""
        self.clear_window()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Barra superior
        top_bar = tk.Frame(main_frame, bg=self.colors['card'], height=70)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Logo
        tk.Label(top_bar, text="✨ PREMIUM PROFILE", font=("Segoe UI", 18, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(side=tk.LEFT, padx=30, pady=15)
        
        # Botão sair
        logout_btn = ModernButton(top_bar, "SAIR", self.logout,
                                 color=self.colors['danger'], hover_color=self.colors['danger_hover'],
                                 width=100, height=35)
        logout_btn.pack(side=tk.RIGHT, padx=30)
        
        # Conteúdo
        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Sidebar (perfil)
        sidebar = tk.Frame(content_frame, bg=self.colors['card'], relief=tk.RAISED, bd=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20), ipadx=30, ipady=20)
        
        # Foto de perfil
        self.photo_frame = tk.Frame(sidebar, bg=self.colors['card'])
        self.photo_frame.pack(pady=20)
        
        self.profile_photo = tk.Label(self.photo_frame, bg=self.colors['card'])
        self.profile_photo.pack()
        self.update_profile_photo()
        
        # Botão alterar foto
        change_photo_btn = ModernButton(sidebar, "📸 ALTERAR FOTO", self.change_photo,
                                       color=self.colors['accent'], hover_color=self.colors['accent_hover'],
                                       width=180, height=35)
        change_photo_btn.pack(pady=10)
        
        # Nome
        self.name_label = tk.Label(sidebar, text=self.profile_data["nome"],
                                  font=("Segoe UI", 18, "bold"),
                                  bg=self.colors['card'], fg=self.colors['text'])
        self.name_label.pack(pady=10)
        
        # Botão editar nome
        edit_name_btn = ModernButton(sidebar, "✏️ EDITAR NOME", self.edit_name,
                                    color=self.colors['warning'], hover_color=self.colors['warning_hover'],
                                    width=180, height=35)
        edit_name_btn.pack(pady=5)
        
        # Estatísticas
        stats_frame = tk.Frame(sidebar, bg=self.colors['card_light'], relief=tk.RAISED, bd=1)
        stats_frame.pack(fill=tk.X, pady=20, padx=10)
        
        tk.Label(stats_frame, text="📊 ESTATÍSTICAS", font=("Segoe UI", 11, "bold"),
                bg=self.colors['card_light'], fg=self.colors['text']).pack(pady=10)
        
        stats_data = [
            ("👥 Acessos", self.profile_data["estatisticas"]["total_acessos"]),
            ("📅 Criado", self.profile_data["data_criacao"].split()[0]),
            ("🕐 Último", self.profile_data["ultimo_acesso"].split()[0])
        ]
        
        for icon, value in stats_data:
            stat_row = tk.Frame(stats_frame, bg=self.colors['card_light'])
            stat_row.pack(fill=tk.X, padx=15, pady=5)
            tk.Label(stat_row, text=icon, font=("Segoe UI Emoji", 12),
                    bg=self.colors['card_light']).pack(side=tk.LEFT)
            tk.Label(stat_row, text=str(value), font=("Segoe UI", 10),
                    bg=self.colors['card_light'], fg=self.colors['text_secondary']).pack(side=tk.RIGHT)
        
        # Conteúdo principal com abas
        notebook = ttk.Notebook(content_frame)
        notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Configurar estilo do notebook
        style = ttk.Style()
        style.configure("TNotebook", background=self.colors['bg'], borderwidth=0)
        style.configure("TNotebook.Tab", background=self.colors['card'], 
                       foreground=self.colors['text'], padding=[20, 10],
                       font=("Segoe UI", 10))
        style.map("TNotebook.Tab", background=[("selected", self.colors['accent'])])
        
        # Aba Informações
        info_tab = tk.Frame(notebook, bg=self.colors['card'])
        notebook.add(info_tab, text="📋 INFORMAÇÕES")
        self.create_info_tab(info_tab)
        
        # Aba Configurações
        config_tab = tk.Frame(notebook, bg=self.colors['card'])
        notebook.add(config_tab, text="⚙️ CONFIGURAÇÕES")
        self.create_config_tab(config_tab)
        
        # Aba Temas
        themes_tab = tk.Frame(notebook, bg=self.colors['card'])
        notebook.add(themes_tab, text="🎨 TEMAS")
        self.create_themes_tab(themes_tab)
    
    def create_info_tab(self, parent):
        """Cria aba de informações"""
        # Frame rolável
        canvas = tk.Canvas(parent, bg=self.colors['card'], highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['card'])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Grid de informações
        info_frame = tk.Frame(scrollable_frame, bg=self.colors['card'])
        info_frame.pack(pady=30, padx=30, fill=tk.BOTH, expand=True)
        
        # Configurar grid
        for i in range(2):
            info_frame.columnconfigure(i, weight=1)
        
        fields = [
            ("📧 EMAIL", "email"),
            ("📱 TELEFONE", "telefone"),
            ("🎂 DATA NASC.", "data_nascimento"),
            ("📍 LOCALIZAÇÃO", "localizacao"),
            ("💼 PROFISSÃO", "profissao"),
            ("🌐 SITE", "site")
        ]
        
        for i, (label, key) in enumerate(fields):
            row = i // 2
            col = i % 2
            
            card = tk.Frame(info_frame, bg=self.colors['card_light'], relief=tk.RAISED, bd=1)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            tk.Label(card, text=label, font=("Segoe UI", 10, "bold"),
                    bg=self.colors['card_light'], fg=self.colors['text_secondary']).pack(anchor=tk.W, padx=15, pady=(15,5))
            
            value_label = tk.Label(card, text=self.profile_data.get(key, "Não informado"),
                                  font=("Segoe UI", 12), bg=self.colors['card_light'],
                                  fg=self.colors['text'])
            value_label.pack(anchor=tk.W, padx=15, pady=(0,15))
            
            # Botão editar
            def edit_field(k=key, lbl=value_label):
                self.edit_field_dialog(k, lbl)
            
            edit_btn = tk.Button(card, text="EDITAR", command=edit_field,
                                bg=self.colors['accent'], fg='white',
                                font=("Segoe UI", 9, "bold"), cursor="hand2",
                                relief=tk.FLAT, padx=15, pady=5)
            edit_btn.place(relx=0.85, rely=0.5, anchor='center')
        
        # Bio
        bio_card = tk.Frame(info_frame, bg=self.colors['card_light'], relief=tk.RAISED, bd=1)
        bio_card.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        
        tk.Label(bio_card, text="📝 BIOGRAFIA", font=("Segoe UI", 12, "bold"),
                bg=self.colors['card_light'], fg=self.colors['text']).pack(anchor=tk.W, padx=15, pady=15)
        
        self.bio_text = tk.Text(bio_card, height=5, font=("Segoe UI", 11),
                               bg=self.colors['card'], fg=self.colors['text'],
                               relief=tk.FLAT, wrap=tk.WORD)
        self.bio_text.pack(fill=tk.BOTH, padx=15, pady=(0,15), expand=True)
        self.bio_text.insert("1.0", self.profile_data.get("bio", ""))
        
        def save_bio():
            self.profile_data["bio"] = self.bio_text.get("1.0", tk.END).strip()
            self.save_data()
            messagebox.showinfo("✅ Sucesso", "Biografia atualizada!")
        
        save_btn = ModernButton(bio_card, "SALVAR BIOGRAFIA", save_bio,
                               color=self.colors['success'], hover_color=self.colors['success_hover'],
                               width=180, height=35)
        save_btn.pack(pady=(0,15))
    
    def create_config_tab(self, parent):
        """Cria aba de configurações"""
        config_frame = tk.Frame(parent, bg=self.colors['card'])
        config_frame.pack(pady=30, padx=30, fill=tk.BOTH, expand=True)
        
        # Segurança
        security_card = tk.Frame(config_frame, bg=self.colors['card_light'], relief=tk.RAISED, bd=1)
        security_card.pack(fill=tk.X, pady=10)
        
        tk.Label(security_card, text="🔐 SEGURANÇA", font=("Segoe UI", 14, "bold"),
                bg=self.colors['card_light'], fg=self.colors['text']).pack(anchor=tk.W, padx=20, pady=15)
        
        change_pass_btn = ModernButton(security_card, "ALTERAR SENHA", self.change_password,
                                      color=self.colors['warning'], hover_color=self.colors['warning_hover'],
                                      width=200, height=40)
        change_pass_btn.pack(pady=15, padx=20, anchor=tk.W)
        
        # Backup
        backup_card = tk.Frame(config_frame, bg=self.colors['card_light'], relief=tk.RAISED, bd=1)
        backup_card.pack(fill=tk.X, pady=10)
        
        tk.Label(backup_card, text="💾 BACKUP", font=("Segoe UI", 14, "bold"),
                bg=self.colors['card_light'], fg=self.colors['text']).pack(anchor=tk.W, padx=20, pady=15)
        
        btn_frame = tk.Frame(backup_card, bg=self.colors['card_light'])
        btn_frame.pack(pady=15, padx=20, anchor=tk.W)
        
        export_btn = ModernButton(btn_frame, "EXPORTAR", self.export_data,
                                 color=self.colors['accent'], hover_color=self.colors['accent_hover'],
                                 width=120, height=35)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        import_btn = ModernButton(btn_frame, "IMPORTAR", self.import_data,
                                 color=self.colors['accent'], hover_color=self.colors['accent_hover'],
                                 width=120, height=35)
        import_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = ModernButton(btn_frame, "RESETAR", self.reset_profile,
                                color=self.colors['danger'], hover_color=self.colors['danger_hover'],
                                width=120, height=35)
        reset_btn.pack(side=tk.LEFT, padx=5)
    
    def create_themes_tab(self, parent):
        """Cria aba de temas"""
        themes_frame = tk.Frame(parent, bg=self.colors['card'])
        themes_frame.pack(pady=30, padx=30, fill=tk.BOTH, expand=True)
        
        tk.Label(themes_frame, text="🎨 ESCOLHA SEU TEMA", font=("Segoe UI", 18, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=20)
        
        # Configurar grid
        for i in range(2):
            themes_frame.columnconfigure(i, weight=1)
        
        themes = [
            ("🌙 Dark Premium", "#1a1a2e", "#e94560", "dark"),
            ("☀️ Light Premium", "#f5f5f5", "#2196F3", "light"),
            ("💙 Blue Ocean", "#e3f2fd", "#1565C0", "blue"),
            ("💚 Green Forest", "#e8f5e9", "#2E7D32", "green"),
            ("💜 Purple Dream", "#f3e5f5", "#6A1B9A", "purple")
        ]
        
        for i, (name, bg_color, accent, theme_id) in enumerate(themes):
            row = i // 2
            col = i % 2
            
            theme_card = tk.Frame(themes_frame, bg=bg_color, relief=tk.RAISED, bd=2)
            theme_card.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
            # Preview
            preview = tk.Frame(theme_card, bg=bg_color, width=250, height=150)
            preview.pack(pady=10, padx=10)
            preview.pack_propagate(False)
            
            # Simular elementos do tema
            tk.Label(preview, text=name, font=("Segoe UI", 12, "bold"),
                    bg=bg_color, fg=accent).pack(pady=20)
            
            text_color = '#333' if bg_color == '#f5f5f5' else '#aaa'
            tk.Label(preview, text="Exemplo de texto", font=("Segoe UI", 10),
                    bg=bg_color, fg=text_color).pack()
            
            tk.Label(theme_card, text=name, font=("Segoe UI", 12, "bold"),
                    bg=bg_color, fg=accent).pack(pady=5)
            
            def apply_theme(t=theme_id):
                self.apply_theme(t)
            
            apply_btn = ModernButton(theme_card, "APLICAR TEMA", lambda t=theme_id: apply_theme(t),
                                    color=accent, hover_color=accent,
                                    width=150, height=30)
            apply_btn.pack(pady=10)
    
    def apply_theme(self, theme_name):
        """Aplica tema selecionado"""
        themes = {
            "dark": {"bg": "#1a1a2e", "card": "#16213e", "card_light": "#1f2a4a", "accent": "#e94560"},
            "light": {"bg": "#f5f5f5", "card": "#ffffff", "card_light": "#fafafa", "accent": "#2196F3"},
            "blue": {"bg": "#e3f2fd", "card": "#ffffff", "card_light": "#f5f5f5", "accent": "#1565C0"},
            "green": {"bg": "#e8f5e9", "card": "#ffffff", "card_light": "#f5f5f5", "accent": "#2E7D32"},
            "purple": {"bg": "#f3e5f5", "card": "#ffffff", "card_light": "#fafafa", "accent": "#6A1B9A"}
        }
        
        if theme_name in themes:
            theme = themes[theme_name]
            self.colors.update({
                'bg': theme['bg'],
                'card': theme['card'],
                'card_light': theme['card_light'],
                'accent': theme['accent']
            })
            self.profile_data["tema"] = theme_name
            self.save_data()
            messagebox.showinfo("✅ Tema Aplicado", f"Tema {theme_name.upper()} aplicado com sucesso!")
            self.show_main_profile()
    
    def edit_field_dialog(self, key, value_label):
        """Diálogo para editar campo"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Editar {key}")
        dialog.geometry("400x200")
        dialog.configure(bg=self.colors['card'])
        
        tk.Label(dialog, text=f"EDITAR {key}", font=("Segoe UI", 14, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=20)
        
        entry = tk.Entry(dialog, font=("Segoe UI", 12), bg=self.colors['card_light'],
                        fg=self.colors['text'], relief=tk.FLAT, insertbackground=self.colors['text'])
        entry.pack(pady=20, padx=30, fill=tk.X)
        entry.insert(0, self.profile_data.get(key, ""))
        
        def save():
            new_value = entry.get().strip()
            self.profile_data[key] = new_value
            self.save_data()
            value_label.config(text=new_value if new_value else "Não informado")
            dialog.destroy()
            messagebox.showinfo("✅ Sucesso", f"{key} atualizado!")
        
        save_btn = ModernButton(dialog, "SALVAR", save, color=self.colors['success'],
                               hover_color=self.colors['success_hover'], width=150, height=35)
        save_btn.pack(pady=20)
    
    def change_photo(self):
        """Altera foto de perfil"""
        filename = filedialog.askopenfilename(
            title="Selecionar foto",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        
        if filename:
            try:
                # Processar imagem
                img = Image.open(filename)
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                
                # Adicionar borda arredondada
                mask = Image.new('L', (150, 150), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, 149, 149), fill=255)
                
                output = Image.new('RGBA', (150, 150), (0,0,0,0))
                output.paste(img, (0,0), mask)
                
                # Salvar
                if not os.path.exists("profile_photos"):
                    os.makedirs("profile_photos")
                
                photo_filename = f"profile_photos/foto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                output.save(photo_filename)
                
                self.profile_data["foto_path"] = photo_filename
                self.save_data()
                self.update_profile_photo()
                messagebox.showinfo("✅ Sucesso", "Foto atualizada com sucesso!")
            except Exception as e:
                messagebox.showerror("❌ Erro", f"Erro ao carregar imagem: {e}")
    
    def update_profile_photo(self):
        """Atualiza foto exibida"""
        if self.profile_data["foto_path"] and os.path.exists(self.profile_data["foto_path"]):
            try:
                img = Image.open(self.profile_data["foto_path"])
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.profile_photo.config(image=photo, text="")
                self.profile_photo.image = photo
            except:
                self.profile_photo.config(text="👤", font=("Segoe UI Emoji", 80), bg=self.colors['card'])
        else:
            self.profile_photo.config(text="👤", font=("Segoe UI Emoji", 80), bg=self.colors['card'])
    
    def edit_name(self):
        """Edita nome do usuário"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Editar Nome")
        dialog.geometry("400x200")
        dialog.configure(bg=self.colors['card'])
        
        tk.Label(dialog, text="EDITAR NOME", font=("Segoe UI", 14, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=20)
        
        entry = tk.Entry(dialog, font=("Segoe UI", 12), bg=self.colors['card_light'],
                        fg=self.colors['text'], relief=tk.FLAT, insertbackground=self.colors['text'])
        entry.pack(pady=20, padx=30, fill=tk.X)
        entry.insert(0, self.profile_data["nome"])
        
        def save():
            new_name = entry.get().strip()
            if new_name:
                self.profile_data["nome"] = new_name
                self.name_label.config(text=new_name)
                self.save_data()
                dialog.destroy()
                messagebox.showinfo("✅ Sucesso", "Nome atualizado!")
            else:
                messagebox.showwarning("⚠️ Aviso", "Nome não pode estar vazio!")
        
        save_btn = ModernButton(dialog, "SALVAR", save, color=self.colors['success'],
                               hover_color=self.colors['success_hover'], width=150, height=35)
        save_btn.pack(pady=20)
    
    def change_password(self):
        """Altera senha"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Alterar Senha")
        dialog.geometry("450x400")
        dialog.configure(bg=self.colors['card'])
        
        tk.Label(dialog, text="🔐 ALTERAR SENHA", font=("Segoe UI", 16, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=20)
        
        frame = tk.Frame(dialog, bg=self.colors['card'])
        frame.pack(pady=20, padx=40, fill=tk.X)
        
        # Senha atual
        tk.Label(frame, text="SENHA ATUAL:", font=("Segoe UI", 10),
                bg=self.colors['card'], fg=self.colors['text_secondary']).pack(anchor=tk.W, pady=(0,5))
        current_pass = tk.Entry(frame, font=("Segoe UI", 12), show="●",
                               bg=self.colors['card_light'], fg=self.colors['text'],
                               relief=tk.FLAT)
        current_pass.pack(fill=tk.X, pady=(0,15), ipady=8)
        
        # Nova senha
        tk.Label(frame, text="NOVA SENHA:", font=("Segoe UI", 10),
                bg=self.colors['card'], fg=self.colors['text_secondary']).pack(anchor=tk.W, pady=(0,5))
        new_pass = tk.Entry(frame, font=("Segoe UI", 12), show="●",
                           bg=self.colors['card_light'], fg=self.colors['text'],
                           relief=tk.FLAT)
        new_pass.pack(fill=tk.X, pady=(0,15), ipady=8)
        
        # Confirmar senha
        tk.Label(frame, text="CONFIRMAR SENHA:", font=("Segoe UI", 10),
                bg=self.colors['card'], fg=self.colors['text_secondary']).pack(anchor=tk.W, pady=(0,5))
        confirm_pass = tk.Entry(frame, font=("Segoe UI", 12), show="●",
                               bg=self.colors['card_light'], fg=self.colors['text'],
                               relief=tk.FLAT)
        confirm_pass.pack(fill=tk.X, pady=(0,15), ipady=8)
        
        def save():
            if self.hash_password(current_pass.get()) != self.profile_data["senha_hash"]:
                messagebox.showerror("❌ Erro", "Senha atual incorreta!")
                return
            
            new = new_pass.get()
            confirm = confirm_pass.get()
            
            if len(new) < 4:
                messagebox.showerror("❌ Erro", "A senha deve ter pelo menos 4 caracteres!")
                return
            
            if new != confirm:
                messagebox.showerror("❌ Erro", "As senhas não coincidem!")
                return
            
            self.profile_data["senha_hash"] = self.hash_password(new)
            self.save_data()
            messagebox.showinfo("✅ Sucesso", "Senha alterada com sucesso!")
            dialog.destroy()
        
        save_btn = ModernButton(dialog, "ALTERAR SENHA", save, color=self.colors['warning'],
                               hover_color=self.colors['warning_hover'], width=200, height=40)
        save_btn.pack(pady=20)
    
    def export_data(self):
        """Exporta dados"""
        filename = filedialog.asksaveasfilename(defaultextension=".json",
                                                filetypes=[("JSON files", "*.json")])
        if filename:
            export_data = self.profile_data.copy()
            export_data["senha_hash"] = "***PROTEGIDO***"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("✅ Sucesso", "Dados exportados com sucesso!")
    
    def import_data(self):
        """Importa dados"""
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    imported = json.load(f)
                if "senha_hash" in imported:
                    del imported["senha_hash"]
                self.profile_data.update(imported)
                self.save_data()
                messagebox.showinfo("✅ Sucesso", "Dados importados com sucesso!")
                self.show_main_profile()
            except Exception as e:
                messagebox.showerror("❌ Erro", f"Erro ao importar: {e}")
    
    def reset_profile(self):
        """Reseta perfil"""
        if messagebox.askyesno("⚠️ Atenção", "Isso irá resetar TODOS os dados!\nTem certeza?"):
            self.profile_data = self.init_profile_data()
            self.save_data()
            messagebox.showinfo("✅ Sucesso", "Perfil resetado! Senha: 123456")
            self.logout()
    
    def logout(self):
        """Faz logout"""
        self.show_login_screen()
    
    def save_data(self):
        """Salva dados"""
        try:
            with open("premium_profile_data.json", "w", encoding="utf-8") as f:
                json.dump(self.profile_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar: {e}")
    
    def load_data(self):
        """Carrega dados"""
        if os.path.exists("premium_profile_data.json"):
            try:
                with open("premium_profile_data.json", "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.profile_data.update(loaded)
            except Exception as e:
                print(f"Erro ao carregar: {e}")
    
    def clear_window(self):
        """Limpa janela"""
        for widget in self.root.winfo_children():
            widget.destroy()

# Executar
if __name__ == "__main__":
    root = tk.Tk()
    app = PremiumProfileSystem(root)
    root.mainloop()