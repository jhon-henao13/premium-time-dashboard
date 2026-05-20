import customtkinter as ctk
import tkinter as tk
import math
from datetime import datetime
import pytz

# Configuración del ecosistema visual
ctk.set_appearance_mode("Dark")  # Inicializado en modo Premium Dark por defecto
ctk.set_default_color_theme("blue")

class PremiumClockApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ventana Principal Estilo Dashboard
        self.title("AuraClock Horizon - Ultimate Edition")
        self.geometry("1000(x)600")
        self.geometry("1000x600")
        self.resizable(False, False)

        # Variables de Estado de la App
        self.is_24h_format = True
        self.current_timezone = "Local"
        
        # Estado del Cronómetro
        self.stopwatch_running = False
        self.stopwatch_start_time = 0.0
        self.stopwatch_elapsed = 0.0
        
        # Estado del Temporizador (Pomodoro)
        self.timer_running = False
        self.timer_duration = 25 * 60  # 25 minutos por defecto
        self.timer_remaining = self.timer_duration

        # Paleta de Colores Exclusiva
        self.accent_color = "#6366f1"       # Índigo Eléctrico
        self.second_hand_color = "#f43f5e"  # Rosa Neón / Coral Rose
        self.stopwatch_color = "#10b981"    # Verde Esmeralda

        self.setup_ui()
        self.update_core_engine()

    def setup_ui(self):
        # Grid Principal de la Aplicación
        self.grid_columnconfigure(0, weight=1, minsize=320)
        self.grid_columnconfigure(1, weight=2, minsize=680)
        self.grid_rowconfigure(0, weight=1)

        # ==================== SIDEBAR IZQUIERDO (CONTROLES) ====================
        self.sidebar = ctk.CTkFrame(self, corner_radius=24, fg_color=("#ffffff", "#1e1e2e"))
        self.sidebar.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(
            self.sidebar, text="AuraClock Pro", 
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold")
        )
        self.title_label.pack(pady=(30, 5), padx=25, anchor="w")
        
        self.subtitle_label = ctk.CTkLabel(
            self.sidebar, text="Premium Time Engine", text_color="gray",
            font=ctk.CTkFont(family="Segoe UI", size=12)
        )
        self.subtitle_label.pack(pady=(0, 25), padx=25, anchor="w")

        # Módulo de Configuración General
        self.config_box = ctk.CTkFrame(self.sidebar, fg_color=("#f1f5f9", "#11111b"), corner_radius=16)
        self.config_box.pack(pady=10, padx=20, fill="x")

        self.tz_label = ctk.CTkLabel(self.config_box, text="ZONA HORARIA MUNDIAL", font=ctk.CTkFont(size=10, weight="bold"))
        self.tz_label.pack(pady=(15, 5), padx=15, anchor="w")
        
        self.tz_selector = ctk.CTkOptionMenu(
            self.config_box, 
            values=["Local", "America/New_York", "Europe/London", "Asia/Tokyo", "Europe/Paris", "Australia/Sydney"],
            command=self.change_timezone, fg_color=self.accent_color, button_hover_color="#4f46e5"
        )
        self.tz_selector.pack(pady=(0, 15), padx=15, fill="x")

        # Selectores Rápidos de Preferencias
        self.format_switch = ctk.CTkSwitch(self.sidebar, text="Formato de 24 Horas", command=self.toggle_format)
        self.format_switch.select()
        self.format_switch.pack(pady=12, padx=25, anchor="w")

        self.theme_switch = ctk.CTkSwitch(self.sidebar, text="Modo Oscuro Profundo", command=self.toggle_theme)
        self.theme_switch.select()
        self.theme_switch.pack(pady=12, padx=25, anchor="w")

        # Footer Técnico Académico
        self.info_card = ctk.CTkFrame(self.sidebar, fg_color=("#e2e8f0", "#181825"), corner_radius=16)
        self.info_card.pack(pady=(40, 20), padx=20, fill="both", expand=True)
        
        self.info_title = ctk.CTkLabel(self.info_card, text="SYSTEM STATUS", font=ctk.CTkFont(family="Consolas", size=12, weight="bold"), text_color=self.accent_color)
        self.info_title.pack(pady=(15, 2), padx=15, anchor="w")
        self.info_desc = ctk.CTkLabel(self.info_card, text="• Render: Canvas Vectorial\n• Sweep: 100Hz Real-Time\n• UX: Neumorphic Adapt", font=ctk.CTkFont(family="Consolas", size=11), justify="left")
        self.info_desc.pack(pady=(0, 15), padx=15, anchor="w")

        # ==================== CONTROLADOR DE PESTAÑAS (DASHBOARD) ====================
        self.tabs = ctk.CTkTabview(self, corner_radius=24, fg_color=("#ffffff", "#1e1e2e"), segmented_button_selected_color=self.accent_color)
        self.tabs.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        
        self.tab_clock = self.tabs.add("Reloj Principal")
        self.tab_stopwatch = self.tabs.add("Cronómetro Pro")
        self.tab_timer = self.tabs.add("Enfoque Pomodoro")

        self.build_clock_tab()
        self.build_stopwatch_tab()
        self.build_timer_tab()

    # ==================== PESTAÑA 1: RELOJ PREMIUM ====================
    def build_clock_tab(self):
        self.canvas_size = 300
        self.canvas = tk.Canvas(self.tab_clock, width=self.canvas_size, height=self.canvas_size, bg="#1e1e2e", highlightthickness=0)
        self.canvas.pack(pady=(15, 5))
        
        self.digital_label = ctk.CTkLabel(self.tab_clock, text="00:00:00", font=ctk.CTkFont(family="Segoe UI Semibold", size=48))
        self.digital_label.pack(pady=0)

        self.date_label = ctk.CTkLabel(self.tab_clock, text="Cargando calendario...", font=ctk.CTkFont(family="Segoe UI Semibold", size=15), text_color="gray")
        self.date_label.pack(pady=(0, 10))

    # ==================== PESTAÑA 2: CRONÓMETRO AVANZADO ====================
    def build_stopwatch_tab(self):
        self.sw_display = ctk.CTkLabel(self.tab_stopwatch, text="00:00.00", font=ctk.CTkFont(family="Consolas", size=72, weight="bold"), text_color=self.stopwatch_color)
        self.sw_display.pack(pady=(80, 20))

        self.sw_btn_frame = ctk.CTkFrame(self.tab_stopwatch, fg_color="transparent")
        self.sw_btn_frame.pack(pady=10)

        self.sw_start_btn = ctk.CTkButton(self.sw_btn_frame, text="Iniciar", fg_color=self.stopwatch_color, hover_color="#059669", width=120, command=self.start_stopwatch)
        self.sw_start_btn.grid(row=0, column=0, padx=10)

        self.sw_reset_btn = ctk.CTkButton(self.sw_btn_frame, text="Reiniciar", fg_color="#4b5563", hover_color="#374151", width=120, command=self.reset_stopwatch)
        self.sw_reset_btn.grid(row=0, column=1, padx=10)

    # ==================== PESTAÑA 3: TEMPORIZADOR POMODORO ====================
    def build_timer_tab(self):
        self.timer_display = ctk.CTkLabel(self.tab_timer, text="25:00", font=ctk.CTkFont(family="Consolas", size=72, weight="bold"), text_color=self.accent_color)
        self.timer_display.pack(pady=(50, 10))

        # Preset Selectors
        self.preset_frame = ctk.CTkFrame(self.tab_timer, fg_color="transparent")
        self.preset_frame.pack(pady=10)
        
        presets = [("Pomodoro (25m)", 25), ("Short Break (5m)", 5), ("Long Break (15m)", 15)]
        for idx, (label, mins) in enumerate(presets):
            btn = ctk.CTkButton(self.preset_frame, text=label, fg_color=("#e2e8f0", "#2d2d3f"), text_color=("#1a1a1a", "#ffffff"), width=110, command=lambda m=mins: self.set_timer_preset(m))
            btn.grid(row=0, column=idx, padx=5)

        self.tm_btn_frame = ctk.CTkFrame(self.tab_timer, fg_color="transparent")
        self.tm_btn_frame.pack(pady=20)

        self.tm_start_btn = ctk.CTkButton(self.tm_btn_frame, text="Comenzar Enfoque", fg_color=self.accent_color, hover_color="#4f46e5", width=140, command=self.start_timer)
        self.tm_start_btn.grid(row=0, column=0, padx=10)

        self.tm_reset_btn = ctk.CTkButton(self.tm_btn_frame, text="Abortar", fg_color="#ef4444", hover_color="#dc2626", width=140, command=self.reset_timer)
        self.tm_reset_btn.grid(row=0, column=1, padx=10)

    # ==================== INTERACTIVIDAD & CONTROLADORES ====================
    def toggle_format(self): self.is_24h_format = self.format_switch.get() == 1
    def change_timezone(self, choice): self.current_timezone = choice

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Dark")
            self.canvas.config(bg="#1e1e2e")
        else:
            ctk.set_appearance_mode("Light")
            self.canvas.config(bg="#f0f2f5")

    def get_current_time(self):
        if self.current_timezone == "Local": return datetime.now()
        return datetime.now(pytz.timezone(self.current_timezone))

    # ==================== LÓGICA DE HERRAMIENTAS ADICIONALES ====================
    def start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_running = True
            self.stopwatch_start_time = datetime.now().timestamp() - self.stopwatch_elapsed
            self.sw_start_btn.configure(text="Pausar", fg_color="#f59e0b", hover_color="#d97706")
        else:
            self.stopwatch_running = False
            self.sw_start_btn.configure(text="Continuar", fg_color=self.stopwatch_color, hover_color="#059669")

    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_elapsed = 0.0
        self.sw_display.configure(text="00:00.00")
        self.sw_start_btn.configure(text="Iniciar", fg_color=self.stopwatch_color, hover_color="#059669")

    def set_timer_preset(self, minutes):
        self.timer_running = False
        self.timer_duration = minutes * 60
        self.timer_remaining = self.timer_duration
        self.tm_start_btn.configure(text="Comenzar Enfoque", fg_color=self.accent_color)
        self.update_timer_ui()

    def start_timer(self):
        if not self.timer_running and self.timer_remaining > 0:
            self.timer_running = True
            self.timer_last_tick = datetime.now().timestamp()
            self.tm_start_btn.configure(text="Pausar", fg_color="#f59e0b", hover_color="#d97706")
        elif self.timer_running:
            self.timer_running = False
            self.tm_start_btn.configure(text="Reanudar", fg_color=self.accent_color, hover_color="#4f46e5")

    def reset_timer(self):
        self.timer_running = False
        self.timer_remaining = self.timer_duration
        self.tm_start_btn.configure(text="Comenzar Enfoque", fg_color=self.accent_color)
        self.update_timer_ui()

    def update_timer_ui(self):
        mins, secs = divmod(int(self.timer_remaining), 60)
        self.timer_display.configure(text=f"{mins:02d}:{secs:02d}")

    # ==================== MOTOR CENTRAL DE REDIBUJADO (10ms Hz) ====================
    def draw_analog_clock(self, now):
        self.canvas.delete("all")
        is_dark = ctk.get_appearance_mode() == "Dark"
        
        # Colores Dinámicos Adaptativos
        dial_bg = "#24243e" if is_dark else "#ffffff"
        ticks_color = "#475569" if is_dark else "#cbd5e1"
        text_color = "#ffffff" if is_dark else "#0f172a"
        
        center = self.canvas_size / 2
        r = center - 15

        # Dial base con iluminación ambiental sutil perimetral
        self.canvas.create_oval(center-r, center-r, center+r, center+r, fill=dial_bg, outline=self.accent_color, width=1)

        # Indicador de estado del cielo interior (Día/Noche UI)
        is_pm = now.hour >= 12
        sky_indicator_color = "#312e81" if is_pm else "#bae6fd"
        self.canvas.create_oval(center-25, center+45, center+25, center+65, fill=sky_indicator_color, outline="")
        self.canvas.create_text(center, center+55, text="PM" if is_pm else "AM", font=("Segoe UI", 8, "bold"), fill="#ffffff" if is_pm else "#0369a1")

        # Dibujar Marcas Horarias Estilizadas (Ticks)
        for i in range(12):
            angle = i * math.pi / 6
            is_cardinal = i % 3 == 0
            len_tick = 14 if is_cardinal else 8
            
            x1 = center + (r - len_tick) * math.sin(angle)
            y1 = center - (r - len_tick) * math.cos(angle)
            x2 = center + r * math.sin(angle)
            y2 = center - r * math.cos(angle)
            
            self.canvas.create_line(x1, y1, x2, y2, fill=self.accent_color if is_cardinal else ticks_color, width=3 if is_cardinal else 1.5)

        # Mecánica de física de movimiento continuo de manecillas (Smooth Sweep)
        ms_frac = now.microsecond / 1000000.0
        seconds_angle = (now.second + ms_frac) * (math.pi / 30)
        minutes_angle = (now.minute + now.second / 60.0) * (math.pi / 30)
        hours_angle = (now.hour % 12 + now.minute / 60.0) * (math.pi / 6)

        # Proporciones Áureas de Longitud
        hr_len, min_len, sec_len = r * 0.48, r * 0.72, r * 0.82

        # 1. Horas
        self.canvas.create_line(center, center, center + hr_len * math.sin(hours_angle), center - hr_len * math.cos(hours_angle), fill=text_color, width=6, capstyle="round")
        # 2. Minutos
        self.canvas.create_line(center, center, center + min_len * math.sin(minutes_angle), center - min_len * math.cos(minutes_angle), fill=self.accent_color, width=4, capstyle="round")
        # 3. Segunderos Continuos (Efecto mecánico fluido de Alta Relojería)
        self.canvas.create_line(center - 20 * math.sin(seconds_angle), center + 20 * math.cos(seconds_angle), center + sec_len * math.sin(seconds_angle), center - sec_len * math.cos(seconds_angle), fill=self.second_hand_color, width=2, capstyle="round")

        # Joya Central (Efecto Corona Cromada)
        self.canvas.create_oval(center-5, center-5, center+5, center+5, fill=dial_bg, outline=self.second_hand_color, width=2)

    def update_core_engine(self):
        # 1. Obtención de Tiempo Sincronizado
        now = self.get_current_time()

        # 2. Renderizado del Reloj Activo (Pestaña actual seleccionada por UX)
        current_active_tab = self.tabs.get()
        
        if current_active_tab == "Reloj Principal":
            self.draw_analog_clock(now)
            time_str = now.strftime("%H:%M:%S") if self.is_24h_format else now.strftime("%I:%M:%S %p")
            self.digital_label.configure(text=time_str)
            
            días = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            self.date_label.configure(text=f"{días[now.weekday()]}, {now.day} de {meses[now.month - 1]}")

        # 3. Lógica interna del Cronómetro de Precisión
        elif current_active_tab == "Cronómetro Pro" and self.stopwatch_running:
            current_ts = datetime.now().timestamp()
            self.stopwatch_elapsed = current_ts - self.stopwatch_start_time
            minutes, seconds = divmod(self.stopwatch_elapsed, 60)
            self.sw_display.configure(text=f"{int(minutes):02d}:{seconds:05.2f}")

        # 4. Lógica interna del Temporizador Pomodoro de Enfoque
        elif current_active_tab == "Enfoque Pomodoro" and self.timer_running:
            current_ts = datetime.now().timestamp()
            elapsed_chunk = current_ts - self.timer_last_tick
            if elapsed_chunk >= 1.0:
                self.timer_remaining -= int(elapsed_chunk)
                self.timer_last_tick = current_ts
                if self.timer_remaining <= 0:
                    self.timer_remaining = 0
                    self.timer_running = False
                    self.tm_start_btn.configure(text="¡Completado!", fg_color="#10b981")
                self.update_timer_ui()

        # Tasa de Refresco Ultra Veloz (Cada 20 milisegundos para garantizar el Sweep Fluido de los Segundos)
        self.after(20, self.update_core_engine)

if __name__ == "__main__":
    app = PremiumClockApp()
    app.mainloop()