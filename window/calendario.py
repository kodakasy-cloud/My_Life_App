import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import calendar


class CalendarioManager:
    def __init__(self, app):
        self.app = app
        
    def open_calendario(self):
        self.app.clear_content()
        
        tk.Label(self.app.content_frame, text="Calendário", font=("Arial", 16, "bold"), 
                bg='white', fg='#333').pack(pady=20)
        
        # Frame do calendário
        cal_frame = tk.Frame(self.app.content_frame, bg='white')
        cal_frame.pack(pady=20)
        
        # Ano e mês atual
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        
        def show_calendar(year, month):
            for widget in cal_frame.winfo_children():
                widget.destroy()
            
            # Navegação
            nav_frame = tk.Frame(cal_frame, bg='white')
            nav_frame.pack(pady=10)
            
            tk.Button(nav_frame, text="◀", command=lambda: change_month(-1), 
                     font=("Arial", 12), bg='#2196F3', fg='white').pack(side=tk.LEFT, padx=5)
            tk.Label(nav_frame, text=f"{calendar.month_name[month]} {year}", 
                    font=("Arial", 14, "bold"), bg='white').pack(side=tk.LEFT, padx=20)
            tk.Button(nav_frame, text="▶", command=lambda: change_month(1), 
                     font=("Arial", 12), bg='#2196F3', fg='white').pack(side=tk.LEFT, padx=5)
            
            # Dias da semana
            days_frame = tk.Frame(cal_frame, bg='white')
            days_frame.pack()
            
            weekdays = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
            for i, day in enumerate(weekdays):
                tk.Label(days_frame, text=day, font=("Arial", 10, "bold"), 
                        bg='#e0e0e0', width=8, height=2, relief=tk.RAISED).grid(row=0, column=i, padx=1, pady=1)
            
            # Dias do mês
            cal = calendar.monthcalendar(year, month)
            for week_num, week in enumerate(cal, 1):
                for day_num, day in enumerate(week):
                    if day != 0:
                        day_color = '#ffeb3b' if (day == now.day and month == now.month and year == now.year) else 'white'
                        day_btn = tk.Button(days_frame, text=str(day), width=8, height=2,
                                          bg=day_color, relief=tk.RAISED,
                                          command=lambda d=day: show_day_events(d, month, year))
                        day_btn.grid(row=week_num, column=day_num, padx=1, pady=1)
                    else:
                        tk.Label(days_frame, text="", width=8, height=2, bg='white').grid(row=week_num, column=day_num, padx=1, pady=1)
        
        def change_month(delta):
            nonlocal current_year, current_month
            current_month += delta
            if current_month > 12:
                current_month = 1
                current_year += 1
            elif current_month < 1:
                current_month = 12
                current_year -= 1
            show_calendar(current_year, current_month)
        
        def show_day_events(day, month, year):
            messagebox.showinfo("Eventos", f"Eventos para {day}/{month}/{year}\n\n(Adicione eventos clicando nas anotações)")
        
        show_calendar(current_year, current_month)