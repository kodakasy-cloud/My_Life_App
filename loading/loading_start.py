import tkinter as tk
from tkinter import ttk
import threading
import time
import json
import os
import math
import random


class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("My Life - Inicializando")
        
        # Dimensões
        self.WIDTH = 850
        self.HEIGHT = 600
        
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.configure(bg='#0a0a0f')
        self.root.resizable(False, False)
        
        # Centralizar
        self.center_window()
        
        # Estados
        self.state = "loading"  # loading, transitioning, ready
        self.loading_complete = False
        self.modules_loaded = False
        self.current_progress = 0
        
        # Animações
        self.animation_phase = 0
        self.particles = []
        self.energy_rings = []
        
        # Inicializar
        self.setup_styles()
        self.init_particles()
        self.create_widgets()
        self.start_loading()
        self.start_animation_loop()
        
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.HEIGHT // 2)
        self.root.geometry(f'{self.WIDTH}x{self.HEIGHT}+{x}+{y}')
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Premium.Horizontal.TProgressbar",
                       background='#8b5cf6',
                       troughcolor='#1e1e2e',
                       bordercolor='#1e1e2e',
                       lightcolor='#8b5cf6',
                       darkcolor='#6d28d9',
                       thickness=8)
        
    def init_particles(self):
        """Inicializa sistema de partículas"""
        for _ in range(25):
            self.particles.append({
                'x': random.randint(0, self.WIDTH),
                'y': random.randint(0, self.HEIGHT),
                'vx': random.uniform(-0.3, 0.3),
                'vy': random.uniform(-0.3, 0.3),
                'size': random.randint(2, 5),
                'color': f'#{random.randint(100, 200):02x}{random.randint(50, 150):02x}ff',
                'phase': random.uniform(0, 2 * math.pi)
            })
            
    def create_widgets(self):
        """Cria toda a interface"""
        # Canvas para efeitos de fundo
        self.bg_canvas = tk.Canvas(self.root, bg='#0a0a0f', highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, width=self.WIDTH, height=self.HEIGHT)
        
        # Container principal
        self.main_frame = tk.Frame(self.root, bg='#0a0a0f')
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center', width=700, height=500)
        
        # === SEÇÃO DO LOGO ===
        self.logo_frame = tk.Frame(self.main_frame, bg='#0a0a0f', width=120, height=120)
        self.logo_frame.pack(pady=(0, 15))
        self.logo_frame.pack_propagate(False)
        
        self.logo_canvas = tk.Canvas(self.logo_frame, width=120, height=120,
                                     bg='#0a0a0f', highlightthickness=0)
        self.logo_canvas.pack()
        
        # Título
        self.title_label = tk.Label(self.main_frame, text="MY LIFE",
                                    font=("Segoe UI", 34, "bold"),
                                    bg='#0a0a0f', fg='#ffffff')
        self.title_label.pack()
        
        self.subtitle_label = tk.Label(self.main_frame, text="Sistema Integrado v2.0",
                                       font=("Segoe UI", 11),
                                       bg='#0a0a0f', fg='#6b7280')
        self.subtitle_label.pack(pady=(0, 25))
        
        # === SEÇÃO DE CARREGAMENTO ===
        self.loading_section = tk.Frame(self.main_frame, bg='#0a0a0f')
        self.loading_section.pack(fill=tk.BOTH, expand=True)
        
        # Status
        status_frame = tk.Frame(self.loading_section, bg='#13131f')
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        status_inner = tk.Frame(status_frame, bg='#13131f')
        status_inner.pack(fill=tk.X, padx=20, pady=12)
        
        self.status_indicator = tk.Canvas(status_inner, width=12, height=12,
                                          bg='#13131f', highlightthickness=0)
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 12))
        self.status_dot = self.status_indicator.create_oval(2, 2, 10, 10,
                                                            fill='#8b5cf6', outline='')
        
        self.status_label = tk.Label(status_inner, text="INICIALIZANDO SISTEMA",
                                     font=("Segoe UI", 10, "bold"),
                                     bg='#13131f', fg='#a0a0b0')
        self.status_label.pack(side=tk.LEFT)
        
        # Barra de progresso
        progress_frame = tk.Frame(self.loading_section, bg='#0a0a0f')
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        progress_header = tk.Frame(progress_frame, bg='#0a0a0f')
        progress_header.pack(fill=tk.X)
        
        self.progress_title = tk.Label(progress_header, text="Preparando módulos...",
                                       font=("Segoe UI", 9),
                                       bg='#0a0a0f', fg='#6b7280')
        self.progress_title.pack(side=tk.LEFT)
        
        self.percent_label = tk.Label(progress_header, text="0%",
                                      font=("Segoe UI", 12, "bold"),
                                      bg='#0a0a0f', fg='#8b5cf6')
        self.percent_label.pack(side=tk.RIGHT)
        
        self.progress_bar = ttk.Progressbar(progress_frame,
                                           style="Premium.Horizontal.TProgressbar",
                                           length=660,
                                           mode='determinate')
        self.progress_bar.pack(pady=(5, 0))
        
        # Console de log
        log_frame = tk.Frame(self.loading_section, bg='#13131f')
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        log_header = tk.Frame(log_frame, bg='#13131f')
        log_header.pack(fill=tk.X, padx=20, pady=(12, 8))
        
        tk.Label(log_header, text="CONSOLE DE INICIALIZAÇÃO",
                font=("Segoe UI", 9, "bold"),
                bg='#13131f', fg='#8b5cf6').pack()
        
        tk.Frame(log_frame, bg='#2a2a3e', height=1).pack(fill=tk.X, padx=20)
        
        text_container = tk.Frame(log_frame, bg='#13131f')
        text_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 15))
        
        self.log_text = tk.Text(text_container,
                               height=8,
                               font=("Consolas", 9),
                               bg='#0a0a0f',
                               fg='#c0c0d0',
                               relief=tk.FLAT,
                               borderwidth=1,
                               wrap=tk.WORD,
                               state=tk.DISABLED)
        
        scrollbar = tk.Scrollbar(text_container, orient="vertical",
                                command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tags de cores para o log
        self.log_text.tag_config("success", foreground="#10b981")
        self.log_text.tag_config("error", foreground="#ef4444")
        self.log_text.tag_config("info", foreground="#8b949e")
        self.log_text.tag_config("highlight", foreground="#8b5cf6")
        
        # === SEÇÃO DO BOTÃO INICIAR (inicialmente escondida) ===
        self.ready_section = tk.Frame(self.main_frame, bg='#0a0a0f')
        
        # Espaçador
        tk.Frame(self.ready_section, bg='#0a0a0f', height=60).pack()
        
        # Container do botão
        button_container = tk.Frame(self.ready_section, bg='#0a0a0f')
        button_container.pack()
        
        # Botão INICIAR
        self.start_button = tk.Button(button_container,
                                      text="INICIAR SISTEMA",
                                      command=self.enter_app,
                                      font=("Segoe UI", 20, "bold"),
                                      bg='#8b5cf6',
                                      fg='#ffffff',
                                      width=16,
                                      height=2,
                                      relief=tk.FLAT,
                                      cursor="hand2",
                                      borderwidth=0,
                                      activebackground='#7c3aed',
                                      activeforeground='#ffffff')
        self.start_button.pack()
        
        # Label de status
        self.ready_label = tk.Label(self.ready_section,
                                    text="",
                                    font=("Segoe UI", 11),
                                    bg='#0a0a0f',
                                    fg='#10b981')
        self.ready_label.pack(pady=20)
        
        # Bind eventos do botão
        self.start_button.bind("<Enter>", lambda e: self.start_button.config(bg='#7c3aed'))
        self.start_button.bind("<Leave>", lambda e: self.start_button.config(bg='#8b5cf6'))
        
        # Bind tecla Enter
        self.root.bind('<Return>', lambda e: self.enter_app_if_ready())
        
    def start_animation_loop(self):
        """Loop principal de animação"""
        self.update_particles()
        self.draw_logo()
        self.draw_energy_rings()
        self.animation_phase += 0.02
        self.root.after(33, self.start_animation_loop)
        
    def update_particles(self):
        """Atualiza e desenha partículas"""
        self.bg_canvas.delete('particle')
        
        for p in self.particles:
            # Movimento
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            # Bounce
            if p['x'] <= 0 or p['x'] >= self.WIDTH:
                p['vx'] *= -1
            if p['y'] <= 0 or p['y'] >= self.HEIGHT:
                p['vy'] *= -1
                
            # Manter dentro dos limites
            p['x'] = max(0, min(self.WIDTH, p['x']))
            p['y'] = max(0, min(self.HEIGHT, p['y']))
            
            # Pulsação
            pulse = 0.7 + 0.3 * math.sin(self.animation_phase * 2 + p['phase'])
            size = p['size'] * pulse
            
            # Desenhar
            self.bg_canvas.create_oval(p['x'] - size/2, p['y'] - size/2,
                                       p['x'] + size/2, p['y'] + size/2,
                                       fill=p['color'], outline='', tags='particle')
            
    def draw_logo(self):
        """Desenha o logo animado"""
        self.logo_canvas.delete('all')
        
        cx, cy = 60, 60
        
        # Círculo externo giratório
        for i in range(3):
            angle = self.animation_phase + i * 2 * math.pi / 3
            radius = 45
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            
            size = 8 + 4 * math.sin(self.animation_phase * 3)
            color = f'#{int(139 + 30 * math.sin(angle)):02x}{92 - i*10:02x}{246 - i*20:02x}'
            
            self.logo_canvas.create_oval(x - size/2, y - size/2,
                                         x + size/2, y + size/2,
                                         fill=color, outline='')
            
        # Círculo central pulsante
        pulse = 25 + 8 * math.sin(self.animation_phase * 2)
        gradient_colors = ['#8b5cf6', '#7c3aed', '#6d28d9']
        
        for i, color in enumerate(gradient_colors):
            r = pulse - i * 5
            if r > 0:
                self.logo_canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                            fill=color, outline='')
                
        # Letra M
        self.logo_canvas.create_text(cx, cy, text="M",
                                     font=("Segoe UI", 24, "bold"),
                                     fill='#ffffff')
        
    def draw_energy_rings(self):
        """Desenha anéis de energia"""
        self.bg_canvas.delete('energy_ring')
        
        if self.state == "loading":
            cx, cy = self.WIDTH // 2, self.HEIGHT // 2
            
            for i in range(2):
                radius = 200 + 50 * i + 20 * math.sin(self.animation_phase * 1.5 + i)
                alpha = 0.1 + 0.05 * math.sin(self.animation_phase * 2)
                
                r = int(139 * alpha)
                g = int(92 * alpha)
                b = int(246 * alpha)
                color = f'#{r:02x}{g:02x}{b:02x}'
                
                self.bg_canvas.create_oval(cx - radius, cy - radius,
                                           cx + radius, cy + radius,
                                           outline=color, width=1, tags='energy_ring')
                
    def add_log(self, message, tag="info"):
        """Adiciona mensagem ao log"""
        self.log_text.config(state=tk.NORMAL)
        
        timestamp = time.strftime("%H:%M:%S")
        prefix = "  "
        
        if tag == "success":
            prefix = "✓ "
        elif tag == "error":
            prefix = "✗ "
        elif tag == "highlight":
            prefix = "◆ "
            
        self.log_text.insert(tk.END, f"[{timestamp}] {prefix}{message}\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def update_progress(self, value, status_text="", progress_text=""):
        """Atualiza barra de progresso"""
        self.current_progress = value
        self.progress_bar['value'] = value
        self.percent_label.config(text=f"{int(value)}%")
        
        if status_text:
            self.status_label.config(text=status_text)
        if progress_text:
            self.progress_title.config(text=progress_text)
            
    def start_loading(self):
        """Inicia carregamento em thread separada"""
        thread = threading.Thread(target=self.load_all_modules, daemon=True)
        thread.start()
        
    def load_all_modules(self):
        """Carrega todos os módulos"""
        try:
            modules = [
                ("Núcleo da Interface", 15, self.load_main_window),
                ("Sistema de Perfil", 12, self.load_perfil),
                ("Motor do Diário", 12, self.load_diario),
                ("Gestor de Tarefas", 12, self.load_tarefas),
                ("Módulo Financeiro", 12, self.load_financas),
                ("Calendário Inteligente", 12, self.load_calendario),
                ("Bloco de Anotações", 12, self.load_anotacoes),
                ("Base de Dados", 13, self.load_data)
            ]
            
            total_weight = sum(m[1] for m in modules)
            current = 0
            loaded = 0
            
            self.add_log("Iniciando sequência de inicialização", "highlight")
            self.add_log("─" * 40, "info")
            
            for name, weight, func in modules:
                progress = int((current / total_weight) * 100)
                self.root.after(0, self.update_progress, progress,
                               f"CARREGANDO: {name.upper()}",
                               f"Carregando {name}...")
                
                self.add_log(f"Inicializando {name}...", "info")
                
                success = func()
                
                if success:
                    self.add_log(f"{name} [OK]", "success")
                    loaded += 1
                else:
                    self.add_log(f"{name} [FALHA]", "error")
                    
                current += weight
                time.sleep(0.12)
                
            self.modules_loaded = (loaded == len(modules))
            self.root.after(0, self.finish_loading)
            
        except Exception as e:
            self.add_log(f"ERRO: {str(e)[:40]}", "error")
            self.root.after(0, self.finish_loading)
            
    def load_main_window(self):
        try:
            import main.main_window
            return True
        except:
            return False
            
    def load_perfil(self):
        try:
            from window.perfil import PerfilManager
            return True
        except:
            return False
            
    def load_diario(self):
        try:
            from window.diario import DiarioManager
            return True
        except:
            return False
            
    def load_tarefas(self):
        try:
            from window.tarefa import TarefasManager
            return True
        except:
            return False
            
    def load_financas(self):
        try:
            from window.financas import FinancasManager
            return True
        except:
            return False
            
    def load_calendario(self):
        try:
            from window.calendario import CalendarioManager
            return True
        except:
            return False
            
    def load_anotacoes(self):
        try:
            from window.anotacoes import AnotacoesManager
            return True
        except:
            return False
            
    def load_data(self):
        try:
            if os.path.exists("personal_app_data.json"):
                with open("personal_app_data.json", "r", encoding="utf-8") as f:
                    json.load(f)
            return True
        except:
            return False
            
    def finish_loading(self):
        """Finaliza o carregamento"""
        self.loading_complete = True
        
        self.update_progress(100, "INICIALIZAÇÃO CONCLUÍDA", "Sistema pronto!")
        
        self.add_log("─" * 40, "info")
        
        if self.modules_loaded:
            self.status_indicator.itemconfig(self.status_dot, fill='#10b981')
            self.add_log("Todos os módulos carregados com sucesso", "success")
            self.add_log("Sistema operacional e pronto para uso", "highlight")
            self.ready_label.config(text="✅ SISTEMA PRONTO PARA USO ✅")
        else:
            self.status_indicator.itemconfig(self.status_dot, fill='#f59e0b')
            self.add_log("Alguns módulos apresentaram falhas", "error")
            self.ready_label.config(text="⚠️ SISTEMA CARREGADO COM AVISOS ⚠️")
            
        # Transição para tela de ready
        self.root.after(300, self.transition_to_ready)
        
    def transition_to_ready(self):
        """Transição suave para a tela de botão"""
        self.state = "transitioning"
        
        # Animação de fade out do loading
        def animate_out(step=0):
            if step < 10:
                self.loading_section.place(y=step * 30)
                self.root.after(20, lambda: animate_out(step + 1))
            else:
                self.loading_section.pack_forget()
                self.show_ready_screen()
                
        animate_out()
        
    def show_ready_screen(self):
        """Mostra a tela com botão INICIAR"""
        self.state = "ready"
        
        # Atualizar título
        self.title_label.config(text="PRONTO", fg='#10b981')
        self.subtitle_label.config(text="Clique no botão para iniciar")
        
        # Mostrar seção ready
        self.ready_section.pack(fill=tk.BOTH, expand=True)
        
        # Animar entrada do botão
        self.animate_button_entrance(0)
        
    def animate_button_entrance(self, step):
        """Animação de entrada do botão"""
        if step < 20:
            # Escala
            scale = 0.3 + step * 0.035
            font_size = int(14 + step * 0.4)
            
            self.start_button.config(font=("Segoe UI", font_size, "bold"))
            
            # Cor
            if step < 10:
                r = 139 - step * 8
                g = 92 + step * 9
                b = 246 - step * 16
            else:
                r, g, b = 59, 130, 246
                
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.start_button.config(bg=color)
            
            self.root.after(25, lambda: self.animate_button_entrance(step + 1))
        else:
            self.start_button.config(bg='#3b82f6', font=("Segoe UI", 20, "bold"))
            self.start_button_pulse()
            
    def start_button_pulse(self):
        """Efeito de pulsação no botão"""
        if self.state != "ready":
            return
            
        colors = ['#3b82f6', '#2563eb', '#1d4ed8', '#2563eb']
        idx = int(self.animation_phase * 4) % len(colors)
        
        self.start_button.config(bg=colors[idx])
        self.root.after(150, self.start_button_pulse)
        
    def enter_app_if_ready(self):
        """Entra no app se estiver pronto"""
        if self.state == "ready":
            self.enter_app()
            
    def enter_app(self):
        """Entra na aplicação principal"""
        if self.state != "ready":
            return
            
        self.state = "exiting"
        
        # Animação de saída
        def animate_exit(step=0):
            if step < 15:
                alpha = 1.0 - step * 0.06
                try:
                    self.root.attributes('-alpha', alpha)
                    self.root.after(20, lambda: animate_exit(step + 1))
                except:
                    self.launch_main_app()
            else:
                self.launch_main_app()
                
        animate_exit()
        
    def launch_main_app(self):
        """Lança a aplicação principal"""
        try:
            self.root.destroy()
            
            main_root = tk.Tk()
            
            w, h = 1360, 900
            x = (main_root.winfo_screenwidth() // 2) - (w // 2)
            y = (main_root.winfo_screenheight() // 2) - (h // 2)
            main_root.geometry(f'{w}x{h}+{x}+{y}')
            
            main_root.attributes('-alpha', 0)
            
            def fade_in(a=0):
                if a < 1.0:
                    try:
                        main_root.attributes('-alpha', a)
                        main_root.after(15, lambda: fade_in(a + 0.05))
                    except:
                        pass
                        
            from main.main_window import PersonalApp
            app = PersonalApp(main_root)
            
            fade_in()
            main_root.mainloop()
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Erro", f"Falha ao iniciar:\n{str(e)}")