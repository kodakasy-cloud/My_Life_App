import tkinter as tk
from tkinter import ttk
import threading
import time
import math
import random


class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicializando Sistema...")

        self.WIDTH = 800
        self.HEIGHT = 500

        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.configure(bg='#0f0f1a')
        self.root.resizable(False, False)

        self.center_window()

        self.loading_complete = False
        self.animation_angle = 0
        self.on_complete_callback = None
        self.particles = []

        self.setup_ui()
        self.init_particles()
        self.start_animations()
        self.start_loading()

    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.HEIGHT // 2)
        self.root.geometry(f'{self.WIDTH}x{self.HEIGHT}+{x}+{y}')

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, bg='#0f0f1a', highlightthickness=0)
        self.canvas.place(x=0, y=0, width=self.WIDTH, height=self.HEIGHT)

        center_frame = tk.Frame(self.root, bg='#0f0f1a')
        center_frame.place(relx=0.5, rely=0.4, anchor='center')

        self.logo_canvas = tk.Canvas(center_frame, width=100, height=100,
                                     bg='#0f0f1a', highlightthickness=0)
        self.logo_canvas.pack(pady=(0, 20))

        self.title = tk.Label(center_frame, text="MY LIFE",
                              font=("Segoe UI", 32, "bold"),
                              fg='#ffffff', bg='#0f0f1a')
        self.title.pack()

        self.subtitle = tk.Label(center_frame, text="Sistema Pessoal Integrado",
                                 font=("Segoe UI", 10),
                                 fg='#6b7280', bg='#0f0f1a')
        self.subtitle.pack(pady=(5, 30))

        progress_frame = tk.Frame(center_frame, bg='#0f0f1a')
        progress_frame.pack(fill='x', pady=(0, 10))

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Modern.Horizontal.TProgressbar',
                        background='#6366f1',
                        troughcolor='#1f1f2e',
                        bordercolor='#1f1f2e',
                        thickness=6)

        self.progress_bar = ttk.Progressbar(progress_frame,
                                            length=400,
                                            mode='determinate',
                                            style='Modern.Horizontal.TProgressbar')
        self.progress_bar.pack()

        self.percent_label = tk.Label(center_frame, text="0%",
                                      font=("Segoe UI", 11, "bold"),
                                      fg='#6366f1', bg='#0f0f1a')
        self.percent_label.pack(pady=(5, 0))

        self.status_label = tk.Label(center_frame, text="Inicializando...",
                                     font=("Segoe UI", 9),
                                     fg='#8b949e', bg='#0f0f1a')
        self.status_label.pack(pady=(15, 0))

        self.button_frame = tk.Frame(self.root, bg='#0f0f1a')

        self.start_button = tk.Button(self.button_frame,
                                      text="▶  INICIAR SISTEMA",
                                      command=self.on_start_clicked,
                                      font=("Segoe UI", 14, "bold"),
                                      bg='#6366f1',
                                      fg='#ffffff',
                                      padx=30,
                                      pady=12,
                                      relief='flat',
                                      cursor='hand2',
                                      activebackground='#4f46e5',
                                      activeforeground='#ffffff')
        self.start_button.pack()

        self.start_button.bind('<Enter>', lambda e: self.start_button.config(bg='#4f46e5'))
        self.start_button.bind('<Leave>', lambda e: self.start_button.config(bg='#6366f1'))
        self.root.bind('<Return>', lambda e: self.on_start_clicked() if self.loading_complete else None)

    def init_particles(self):
        for _ in range(30):
            self.particles.append({
                'x': random.randint(0, self.WIDTH),
                'y': random.randint(0, self.HEIGHT),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'size': random.randint(2, 4),
                'alpha': random.uniform(0.3, 0.8)
            })

    def start_animations(self):
        self.animate_logo()
        self.animate_particles()

    def animate_logo(self):
        if not self._widget_alive(self.logo_canvas):
            return

        self.logo_canvas.delete('all')
        cx, cy = 50, 50
        self.animation_angle += 0.05

        for i in range(3):
            angle = self.animation_angle + (i * 2 * math.pi / 3)
            radius = 35
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            size = 6 + 2 * math.sin(self.animation_angle * 2)
            color = f'#{int(99 + 30 * i):02x}{int(102 + 30 * i):02x}{int(241 - 30 * i):02x}'
            self.logo_canvas.create_oval(x - size, y - size,
                                         x + size, y + size,
                                         fill=color, outline='')

        pulse = 20 + 5 * math.sin(self.animation_angle * 3)
        self.logo_canvas.create_oval(cx - pulse, cy - pulse,
                                     cx + pulse, cy + pulse,
                                     fill='#6366f1', outline='')
        self.logo_canvas.create_text(cx, cy, text="⚡",
                                     font=("Segoe UI", 28),
                                     fill='#ffffff')

        if self._widget_alive(self.root):
            self.root.after(50, self.animate_logo)

    def animate_particles(self):
        if not self._widget_alive(self.canvas):
            return

        self.canvas.delete('particle')

        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']

            if p['x'] <= 0 or p['x'] >= self.WIDTH:
                p['vx'] *= -1
            if p['y'] <= 0 or p['y'] >= self.HEIGHT:
                p['vy'] *= -1

            p['x'] = max(0, min(self.WIDTH, p['x']))
            p['y'] = max(0, min(self.HEIGHT, p['y']))

            color = '#6366f1'
            stipple = 'gray50' if p['alpha'] < 0.6 else ''
            self.canvas.create_oval(p['x'] - p['size'], p['y'] - p['size'],
                                    p['x'] + p['size'], p['y'] + p['size'],
                                    fill=color, outline='', tags='particle',
                                    stipple=stipple)

        if self._widget_alive(self.root):
            self.root.after(33, self.animate_particles)

    def start_loading(self):
        thread = threading.Thread(target=self._loading_worker, daemon=True)
        thread.start()

    def _loading_worker(self):
        """Roda em background; comunica com a UI via `after`."""
        steps = [
            (10,  "Verificando sistema..."),
            (25,  "Carregando módulos..."),
            (40,  "Inicializando interface..."),
            (55,  "Configurando ambiente..."),
            (70,  "Estabelecendo conexões..."),
            (85,  "Otimizando performance..."),
            (100, "Sistema pronto!"),
        ]
        for progress, message in steps:
            time.sleep(0.3)
            # Agendar atualização na thread principal (thread-safe)
            if self._widget_alive(self.root):
                self.root.after(0, self._update_progress, progress, message)

        # Sinalizar conclusão também na thread principal
        if self._widget_alive(self.root):
            self.root.after(0, self._on_loading_done)

    def _update_progress(self, value, message):
        if not self._widget_alive(self.progress_bar):
            return
        self.progress_bar['value'] = value
        self.percent_label.config(text=f"{value}%")
        self.status_label.config(text=message)

    def _on_loading_done(self):
        self.loading_complete = True
        self._show_start_button()

    def _show_start_button(self):
        if not self._widget_alive(self.button_frame):
            return

        self.button_frame.place(relx=0.5, rely=0.7, anchor='center')
        self.title.config(text="PRONTO!", fg='#10b981')
        self.subtitle.config(text="Clique no botão para iniciar")
        self.status_label.config(text="✅ Sistema carregado com sucesso!", fg='#10b981')
        self._pulse_button()

    def _pulse_button(self):
        if not self.loading_complete or not self._widget_alive(self.start_button):
            return
        current = self.start_button.cget('bg')
        next_color = '#4f46e5' if current == '#6366f1' else '#6366f1'
        self.start_button.config(bg=next_color)
        self.root.after(500, self._pulse_button)

    def on_start_clicked(self):
        if not self.loading_complete:
            return
        self._fade_out(1.0)

    def _fade_out(self, alpha):
        if not self._widget_alive(self.root):
            return
        if alpha > 0:
            self.root.attributes('-alpha', alpha)
            self.root.after(20, self._fade_out, round(alpha - 0.05, 2))
        else:
            self._finish()

    def _finish(self):
        callback = self.on_complete_callback
        try:
            self.root.destroy()
        except Exception:
            pass
        if callback:
            try:
                callback()
            except Exception:
                import logging
                logging.getLogger(__name__).exception(
                    "Erro ao executar on_complete_callback do LoadingScreen"
                )

    def set_on_complete(self, callback):
        self.on_complete_callback = callback

    # ------------------------------------------------------------------ #
    @staticmethod
    def _widget_alive(widget) -> bool:
        """Retorna True se o widget ainda existe e não foi destruído."""
        try:
            return bool(widget.winfo_exists())
        except Exception:
            return False