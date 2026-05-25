import customtkinter as ctk
import tkinter as tk
import math
from datetime import datetime
import pytz

# ==========================================
# CONFIGURACIÓN DEL ENTORNO VISUAL PREMIUM
# ==========================================
ctk.set_appearance_mode("Dark")
# Forzamos tema dark consistente para conservar el contraste premium neón/verde
ctk.set_default_color_theme("green") 

class Theme:
    """Paleta de colores Cyber-Green Premium y estilos globales"""
    ACCENT = "#10b981"          # Verde Esmeralda Líquido
    ACCENT_HOVER = "#059669"    # Verde Bosque Intenso
    NEON_GREEN = "#22c55e"      # Verde Neón Radiactivo (Detalles)
    MINT = "#a7f3d0"            # Verde Menta Pastel (Textos/Contrastes)
    BG_CARD_DARK = "#0f172a"    # Slate/Jet Ultra Oscuro Deep Space
    TEXT_MUTED = "#64748b"      # Gris Neutro UX
    SECOND_HAND = "#10b981"     # Sincronizado en verde para pureza de paleta
    DANGER = "#f43f5e"          # Rosa Alerta / Coral para contrastes críticos
    DARK_SURFACE = "#1e293b"    # Superficies secundarias elegantes

# ==========================================
# COMPONENTE: RELOJ ANALÓGICO & DIGITAL PRO
# ==========================================
class ClockView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        # Grid layout con arquitectura limpia (Dos columnas: Reloj vs Stats Rápidos)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # CONTENEDOR IZQUIERDO: Canvas e info digital principal
        self.left_container = ctk.CTkFrame(self, fg_color="transparent")
        self.left_container.grid(row=0, column=0, sticky="nsew", padx=10)

        # Canvas para Reloj Analógico Modernizado
        self.canvas_size = 280
        self.canvas = tk.Canvas(
            self.left_container, width=self.canvas_size, height=self.canvas_size, 
            bg=Theme.BG_CARD_DARK, highlightthickness=0
        )
        self.canvas.pack(pady=(10, 15))
        
        # Display Digital Integrado
        self.digital_label = ctk.CTkLabel(
            self.left_container, text="00:00:00", 
            font=ctk.CTkFont(family="Consolas", size=48, weight="bold"),
            text_color=Theme.NEON_GREEN
        )
        self.digital_label.pack()

        self.date_label = ctk.CTkLabel(
            self.left_container, text="Cargando cronograma...", 
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="normal"), 
            text_color=Theme.MINT
        )
        self.date_label.pack(pady=(2, 0))

        # CONTENEDOR DERECHO: Centro de Utilidades Avanzadas del Reloj
        self.right_container = ctk.CTkFrame(self, fg_color=("#f1f5f9", "#111827"), corner_radius=16, border_width=1, border_color="#334155")
        self.right_container.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=10)
        self.right_container.grid_columnconfigure(0, weight=1)
        
        # Utilidad 1: Progreso del día actual
        self.day_progress_title = ctk.CTkLabel(self.right_container, text="RENDIMIENTO DIARIO", font=ctk.CTkFont(size=10, weight="bold"), text_color=Theme.TEXT_MUTED)
        self.day_progress_title.pack(pady=(20, 2), padx=20, anchor="w")
        
        self.day_progress_bar = ctk.CTkProgressBar(self.right_container, progress_color=Theme.ACCENT, fg_color="#334155")
        self.day_progress_bar.pack(fill="x", padx=20, pady=5)
        
        self.day_progress_text = ctk.CTkLabel(self.right_container, text="0.0% completado", font=ctk.CTkFont(family="Consolas", size=12), text_color=Theme.ACCENT)
        self.day_progress_text.pack(padx=20, anchor="w")

        # Utilidad 2: Estado Solar/Astronómico Dinámico
        self.astro_frame = ctk.CTkFrame(self.right_container, fg_color=Theme.BG_CARD_DARK, corner_radius=10)
        self.astro_frame.pack(fill="x", padx=20, pady=20)
        
        self.astro_icon = ctk.CTkLabel(self.astro_frame, text="🌙", font=ctk.CTkFont(size=28))
        self.astro_icon.pack(side="left", padx=15, pady=10)
        
        self.astro_status = ctk.CTkLabel(self.astro_frame, text="Ciclo: Nocturno\nFase de Enfoque", font=ctk.CTkFont(size=12), justify="left", text_color="#ffffff")
        self.astro_status.pack(side="left", padx=5)

        # Utilidad 3: Segundero Lineal de Alta Frecuencia (UX Adicional)
        self.linear_sec_title = ctk.CTkLabel(self.right_container, text="SWEEP LINEAL DE MILISEGUNDOS", font=ctk.CTkFont(size=10, weight="bold"), text_color=Theme.TEXT_MUTED)
        self.linear_sec_title.pack(pady=(10, 2), padx=20, anchor="w")
        
        self.ms_progress = ctk.CTkProgressBar(self.right_container, progress_color=Theme.NEON_GREEN, fg_color="#1e293b", height=6)
        self.ms_progress.pack(fill="x", padx=20, pady=5)

    def update_view(self, now, is_24h):
        # 1. Actualizar Textos y Formatos Digitales
        fmt = "%H:%M:%S" if is_24h else "%I:%M:%S %p"
        self.digital_label.configure(text=now.strftime(fmt))
        
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        self.date_label.configure(text=f"{dias[now.weekday()]}, {now.day} de {meses[now.month - 1]} del 2026")

        # 2. Computar Utilidad: Porcentaje del día transcurrido
        segundos_hoy = now.hour * 3600 + now.minute * 60 + now.second
        porcentaje_dia = segundos_hoy / 86400.0
        self.day_progress_bar.set(porcentaje_dia)
        self.day_progress_text.configure(text=f"{porcentaje_dia * 100:.2f}% del día transcurrido")

        # 3. Computar Utilidad: Estado Solar Estilizado
        if 6 <= now.hour < 18:
            self.astro_icon.configure(text="☀️")
            self.astro_status.configure(text="Ciclo: Diurno\nProductividad Activa")
        else:
            self.astro_icon.configure(text="🌙")
            self.astro_status.configure(text="Ciclo: Nocturno\nModo de Descanso/Enfoque")

        # 4. Sweep Lineal de Precisión de Milisegundos
        self.ms_progress.set(now.microsecond / 1000000.0)

        # 5. Redibujar Reloj Analógico Premium
        self.canvas.delete("all")
        is_dark = ctk.get_appearance_mode() == "Dark"
        
        bg_color = Theme.BG_CARD_DARK if is_dark else "#ffffff"
        self.canvas.config(bg=bg_color)
        dial_fill = "#070b12" if is_dark else "#f8fafc"
        text_color = "#ffffff" if is_dark else "#0f172a"
        ticks_color = "#334155" if is_dark else "#cbd5e1"

        center = self.canvas_size / 2
        r = center - 15

        # Capa Esfera externa de precisión minimalista
        self.canvas.create_oval(center-r, center-r, center+r, center+r, fill=dial_fill, outline="#1e293b", width=2)
        
        # Anillo interno de carga sutil (Indica el avance del minuto actual)
        sec_ratio = now.second / 60.0
        self.canvas.create_arc(center-r+5, center-r+5, center+r-5, center+r-5, start=90, extent=-sec_ratio*360, outline=Theme.ACCENT_HOVER, width=2, style="arc")

        # Marcadores Horarios e Índices Numéricos Avanzados
        for i in range(12):
            angle = i * math.pi / 6
            is_main = i % 3 == 0
            tick_len = 12 if is_main else 6
            
            x1 = center + (r - tick_len) * math.sin(angle)
            y1 = center - (r - tick_len) * math.cos(angle)
            x2 = center + r * math.sin(angle)
            y2 = center - r * math.cos(angle)
            
            self.canvas.create_line(x1, y1, x2, y2, fill=Theme.ACCENT if is_main else ticks_color, width=3 if is_main else 1)
            
            # Números clave estilizados de cabina (12, 3, 6, 9)
            if is_main:
                num_text = "12" if i == 0 else str(i)
                tx = center + (r - 24) * math.sin(angle)
                ty = center - (r - 24) * math.cos(angle)
                self.canvas.create_text(tx, ty, text=num_text, font=("Consolas", 11, "bold"), fill=Theme.MINT)

        # Cálculo de Ángulos de Manecillas (Smooth Continuous Sweep)
        ms_frac = now.microsecond / 1000000.0
        sec_angle = (now.second + ms_frac) * (math.pi / 30)
        min_angle = (now.minute + now.second / 60.0) * (math.pi / 30)
        hr_angle = (now.hour % 12 + now.minute / 60.0) * (math.pi / 6)

        len_hr, len_min, len_sec = r * 0.48, r * 0.72, r * 0.82

        # Manecilla de Horas (Gruesa y Sólida)
        self.canvas.create_line(center, center, center + len_hr * math.sin(hr_angle), center - len_hr * math.cos(hr_angle), fill=text_color, width=5, capstyle="round")
        
        # Manecilla de Minutos (Estilizada con Acabado Verde)
        self.canvas.create_line(center, center, center + len_min * math.sin(min_angle), center - len_min * math.cos(min_angle), fill=Theme.ACCENT, width=3.5, capstyle="round")
        
        # Manecilla de Segundos (Línea Neón delgada de alta tecnología con contrapeso trasero)
        self.canvas.create_line(center - 15 * math.sin(sec_angle), center + 15 * math.cos(sec_angle), center + len_sec * math.sin(sec_angle), center - len_sec * math.cos(sec_angle), fill=Theme.NEON_GREEN, width=1.5)

        # Centro de la maquinaría (Eje pivotante)
        self.canvas.create_oval(center-4, center-4, center+4, center+4, fill=dial_fill, outline=Theme.NEON_GREEN, width=2)


# ==========================================
# COMPONENTE: CRONÓMETRO PROFESIONAL CON LAPS
# ==========================================
class StopwatchView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.running = False
        self.start_time = 0.0
        self.elapsed = 0.0
        self.laps = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Display Principal Estilo Matriz Verde
        self.display = ctk.CTkLabel(
            self, text="00:00.00", 
            font=ctk.CTkFont(family="Consolas", size=76, weight="bold"), 
            text_color=Theme.NEON_GREEN
        )
        self.display.grid(row=0, column=0, pady=(30, 15), sticky="ew")

        # Botonera Controladora
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=1, column=0, pady=10)

        self.start_btn = ctk.CTkButton(self.btn_frame, text="Iniciar", fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER, width=130, font=ctk.CTkFont(weight="bold"), command=self.toggle)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.lap_btn = ctk.CTkButton(self.btn_frame, text="Vuelta", fg_color="#334155", hover_color="#475569", width=130, state="disabled", font=ctk.CTkFont(weight="bold"), command=self.record_lap)
        self.lap_btn.grid(row=0, column=1, padx=10)

        self.reset_btn = ctk.CTkButton(self.btn_frame, text="Reiniciar", fg_color="#1e293b", hover_color="#334155", width=130, command=self.reset)
        self.reset_btn.grid(row=0, column=2, padx=10)

        # Historial de Vueltas Terminal-Style
        self.laps_box = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=14), corner_radius=12, border_width=1, border_color="#334155", fg_color="#070b12", text_color=Theme.MINT)
        self.laps_box.grid(row=2, column=0, padx=40, pady=(15, 10), sticky="nsew")
        self.laps_box.insert("0.0", " [SISTEMA] Historial de telemetría listo...\n" + "-" * 50)
        self.laps_box.configure(state="disabled")

    def toggle(self):
        if not self.running:
            self.running = True
            self.start_time = datetime.now().timestamp() - self.elapsed
            self.start_btn.configure(text="Pausar", fg_color="#eab308", hover_color="#ca8a04")
            self.lap_btn.configure(state="normal")
        else:
            self.running = False
            self.start_btn.configure(text="Continuar", fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER)
            self.lap_btn.configure(state="disabled")

    def record_lap(self):
        if self.running:
            minutes, seconds = divmod(self.elapsed, 60)
            lap_str = f" » REGISTRO {len(self.laps)+1:02d} --------> {int(minutes):02d}:{seconds:05.2f}\n"
            self.laps.append(lap_str)
            
            self.laps_box.configure(state="normal")
            if len(self.laps) == 1: self.laps_box.delete("1.0", "end")
            self.laps_box.insert("1.0", lap_str)
            self.laps_box.configure(state="disabled")

    def reset(self):
        self.running = False
        self.elapsed = 0.0
        self.laps.clear()
        self.display.configure(text="00:00.00")
        self.start_btn.configure(text="Iniciar", fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER)
        self.lap_btn.configure(state="disabled")
        
        self.laps_box.configure(state="normal")
        self.laps_box.delete("1.0", "end")
        self.laps_box.insert("0.0", " [SISTEMA] Historial de telemetría listo...\n" + "-" * 50)
        self.laps_box.configure(state="disabled")

    def tick(self):
        if self.running:
            self.elapsed = datetime.now().timestamp() - self.start_time
            minutes, seconds = divmod(self.elapsed, 60)
            self.display.configure(text=f"{int(minutes):02d}:{seconds:05.2f}")


# ==========================================
# COMPONENTE: ENFOQUE POMODORO CON AVANCE
# ==========================================
class PomodoroView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.running = False
        self.duration = 25 * 60
        self.remaining = self.duration
        self.last_tick = 0.0

        self.grid_columnconfigure(0, weight=1)

        # Display de Tiempo Reloj
        self.display = ctk.CTkLabel(
            self, text="25:00", 
            font=ctk.CTkFont(family="Consolas", size=82, weight="bold"), 
            text_color=Theme.ACCENT
        )
        self.display.grid(row=0, column=0, pady=(25, 5))

        # Barra de progreso integrada
        self.progress_bar = ctk.CTkProgressBar(self, width=380, progress_color=Theme.ACCENT, fg_color="#1e293b")
        self.progress_bar.set(1.0)
        self.progress_bar.grid(row=1, column=0, pady=(0, 20))

        # Selectores rápidos Presets (UX Estilo Cyber)
        self.preset_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.preset_frame.grid(row=2, column=0, pady=10)
        
        presets = [("Bloque Foco (25m)", 25), ("Descanso Corto (5m)", 5), ("Descanso Largo (15m)", 15)]
        for idx, (label, mins) in enumerate(presets):
            btn = ctk.CTkButton(
                self.preset_frame, text=label, 
                fg_color="#1e293b", text_color="#ffffff",
                hover_color="#334155", width=130, 
                command=lambda m=mins: self.set_preset(m)
            )
            btn.grid(row=0, column=idx, padx=6)

        # Botonera de Acción
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.grid(row=3, column=0, pady=25)

        self.start_btn = ctk.CTkButton(self.action_frame, text="Comenzar Enfoque", fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER, width=160, font=ctk.CTkFont(weight="bold"), command=self.toggle)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.reset_btn = ctk.CTkButton(self.action_frame, text="Abortar", fg_color=Theme.DANGER, hover_color="#e11d48", width=160, command=self.reset)
        self.reset_btn.grid(row=0, column=1, padx=10)

    def set_preset(self, minutes):
        self.running = False
        self.duration = minutes * 60
        self.remaining = self.duration
        self.start_btn.configure(text="Comenzar Enfoque", fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER)
        self.update_ui()

    def toggle(self):
        if not self.running and self.remaining > 0:
            self.running = True
            self.last_tick = datetime.now().timestamp()
            self.start_btn.configure(text="Pausar Sesión", fg_color="#eab308", hover_color="#ca8a04")
        elif self.running:
            self.running = False
            self.start_btn.configure(text="Reanudar", fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER)

    def reset(self):
        self.running = False
        self.remaining = self.duration
        self.start_btn.configure(text="Comenzar Enfoque", fg_color=Theme.ACCENT, hover_color=Theme.ACCENT_HOVER)
        self.update_ui()

    def update_ui(self):
        mins, secs = divmod(int(self.remaining), 60)
        self.display.configure(text=f"{mins:02d}:{secs:02d}")
        ratio = self.remaining / self.duration if self.duration > 0 else 0
        self.progress_bar.set(ratio)

    def tick(self):
        if self.running:
            now_ts = datetime.now().timestamp()
            elapsed = now_ts - self.last_tick
            if elapsed >= 1.0:
                self.remaining -= int(elapsed)
                self.last_tick = now_ts
                if self.remaining <= 0:
                    self.remaining = 0
                    self.running = False
                    self.start_btn.configure(text="¡Completado!", fg_color=Theme.NEON_GREEN)
                self.update_ui()




# ==========================================
# COMPONENTE: SISTEMA DE ALARMAS PREMIUM
# ==========================================
class AlarmView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header de Estado
        self.status_title = ctk.CTkLabel(self, text="SISTEMA DE ALARMAS AUTOMATIZADO", font=ctk.CTkFont(size=12, weight="bold"), text_color=Theme.TEXT_MUTED)
        self.status_title.grid(row=0, column=0, pady=(10, 5))

        self.display_status = ctk.CTkLabel(self, text="ALARMA INACTIVA", font=ctk.CTkFont(family="Consolas", size=24, weight="bold"), text_color=Theme.TEXT_MUTED)
        self.display_status.grid(row=1, column=0, pady=(0, 20))

        # Panel Central Selector Premium
        self.selector_frame = ctk.CTkFrame(self, fg_color="#111827", corner_radius=16, border_width=1, border_color="#334155")
        self.selector_frame.grid(row=2, column=0, padx=40, pady=10, sticky="nsew")
        self.selector_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.selector_frame.grid_rowconfigure((0, 1), weight=1)

        # OptionMenu de Horas (00-23)
        hours_values = [f"{i:02d}" for i in range(24)]
        self.hour_label = ctk.CTkLabel(self.selector_frame, text="HORA", font=ctk.CTkFont(size=11, weight="bold"), text_color=Theme.MINT)
        self.hour_label.grid(row=0, column=0, sticky="s", pady=5)
        self.hour_menu = ctk.CTkOptionMenu(self.selector_frame, values=hours_values, fg_color=Theme.DARK_SURFACE, button_color="#334155", button_hover_color=Theme.ACCENT_HOVER, width=100)
        self.hour_menu.grid(row=1, column=0, sticky="n", pady=10)

        # Separador visual de dos puntos corporativo
        self.dots_label = ctk.CTkLabel(self.selector_frame, text=":", font=ctk.CTkFont(family="Consolas", size=36, weight="bold"), text_color=Theme.TEXT_MUTED)
        self.dots_label.grid(row=1, column=1, sticky="n", pady=2)

        # OptionMenu de Minutos (00-59)
        minutes_values = [f"{i:02d}" for i in range(60)]
        self.minute_label = ctk.CTkLabel(self.selector_frame, text="MINUTO", font=ctk.CTkFont(size=11, weight="bold"), text_color=Theme.MINT)
        self.minute_label.grid(row=0, column=2, sticky="s", pady=5)
        self.minute_menu = ctk.CTkOptionMenu(self.selector_frame, values=minutes_values, fg_color=Theme.DARK_SURFACE, button_color="#334155", button_hover_color=Theme.ACCENT_HOVER, width=100)
        self.minute_menu.grid(row=1, column=2, sticky="n", pady=10)

        # Switch maestro de Armado de Alarma
        self.switch_alarm = ctk.CTkSwitch(self, text="Armar Alarma del Sistema", progress_color=Theme.ACCENT, font=ctk.CTkFont(weight="bold"), command=self.toggle_alarm_state)
        self.switch_alarm.grid(row=3, column=0, pady=20)

        # Botón de Interrupción Crítico (Snooze/Stop) - Oculto por defecto
        self.stop_btn = ctk.CTkButton(self, text="DESACTIVAR ALARMA EN CURSO", fg_color=Theme.DANGER, hover_color="#e11d48", height=45, font=ctk.CTkFont(weight="bold"), command=self.dismiss_triggered_alarm)
        # Se guarda la referencia pero no se hace .grid() inicial para control UX

    def toggle_alarm_state(self):
        if self.switch_alarm.get() == 1:
            self.controller.alarm_time["hour"] = self.hour_menu.get()
            self.controller.alarm_time["minute"] = self.minute_menu.get()
            self.controller.alarm_active = True
            
            # Bloquear selectores mientras está armada para evitar desajustes accidentales
            self.hour_menu.configure(state="disabled")
            self.minute_menu.configure(state="disabled")
            self.display_status.configure(text=f"PROGRAMADA -> {self.controller.alarm_time['hour']}:{self.controller.alarm_time['minute']}", text_color=Theme.NEON_GREEN)
        else:
            self.controller.alarm_active = False
            self.hour_menu.configure(state="normal")
            self.minute_menu.configure(state="normal")
            self.display_status.configure(text="ALARMA INACTIVA", text_color=Theme.TEXT_MUTED)

    def show_trigger_ui(self):
        self.switch_alarm.grid_remove() # Ocultar interruptor común
        self.display_status.configure(text="¡SISTEMA EN ALERTA CRÍTICA!", text_color=Theme.DANGER)
        self.stop_btn.grid(row=3, column=0, pady=20, padx=40, sticky="ew")

    def dismiss_triggered_alarm(self):
        self.controller.stop_alarm()

    def reset_ui_state(self):
        self.stop_btn.grid_remove()
        self.switch_alarm.grid()
        self.switch_alarm.deselect()
        self.hour_menu.configure(state="normal")
        self.minute_menu.configure(state="normal")
        self.display_status.configure(text="ALARMA INACTIVA", text_color=Theme.TEXT_MUTED)

    def update_view(self):
        # Reservado para micro-interacciones adicionales de renderizado si fuesen necesarias
        pass


# ==========================================
# VENTANA PRINCIPAL / DASHBOARD CORE ENGINE
# ==========================================
class AuraClockHorizon(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Estructura e Identidad del Dashboard
        self.title("AuraClock - jhon-henao13")
        self.geometry("1060x650")
        self.resizable(False, False)

        self.is_24h_format = True
        self.current_timezone = "Local"

        self.setup_layout()

    def setup_layout(self):
        self.grid_columnconfigure(0, weight=0, minsize=320)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ----------------------------------------------------
        # SIDEBAR IZQUIERDA (CONTROLES GLOBALES)
        # ----------------------------------------------------
        sidebar = ctk.CTkFrame(self, corner_radius=20, fg_color=("#f8fafc", "#0b0f19"), border_width=1, border_color="#1e293b")
        sidebar.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        brand_label = ctk.CTkLabel(sidebar, text="AuraClock", font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"), text_color=Theme.ACCENT)
        brand_label.pack(pady=(30, 2), padx=25, anchor="w")
        
        sub_brand = ctk.CTkLabel(sidebar, text="Horizon Green OS Engine v3.0", text_color=Theme.TEXT_MUTED, font=ctk.CTkFont(family="Segoe UI", size=11, weight="normal"))
        sub_brand.pack(pady=(0, 25), padx=25, anchor="w")

        # Configuración de localización
        config_card = ctk.CTkFrame(sidebar, fg_color="#111827", corner_radius=14, border_width=1, border_color="#1e293b")
        config_card.pack(pady=10, padx=20, fill="x")

        tz_title = ctk.CTkLabel(config_card, text="ZONA HORARIA MUNDIAL", font=ctk.CTkFont(size=10, weight="bold"), text_color=Theme.TEXT_MUTED)
        tz_title.pack(pady=(12, 6), padx=15, anchor="w")
        
        self.tz_menu = ctk.CTkOptionMenu(
            config_card, 
            values=["Local", "America/New_York", "Europe/London", "Asia/Tokyo", "Europe/Paris", "Australia/Sydney"],
            command=self.set_timezone, fg_color=Theme.ACCENT, button_hover_color=Theme.ACCENT_HOVER, dynamic_resizing=False
        )
        self.tz_menu.pack(pady=(0, 15), padx=15, fill="x")

        # Switches Interactivos
        self.switch_format = ctk.CTkSwitch(sidebar, text="Formato de 24 Horas", progress_color=Theme.ACCENT, command=self.toggle_format)
        self.switch_format.select()
        self.switch_format.pack(pady=12, padx=25, anchor="w")

        self.switch_theme = ctk.CTkSwitch(sidebar, text="Estilo Matrix / Oscuro", progress_color=Theme.ACCENT, command=self.toggle_theme)
        self.switch_theme.select()
        self.switch_theme.pack(pady=12, padx=25, anchor="w")

        # Módulo de Diagnóstico del Sistema Dinámico
        self.status_card = ctk.CTkFrame(sidebar, fg_color="#070b12", corner_radius=14, border_width=1, border_color="#1e293b")
        self.status_card.pack(pady=(25, 20), padx=20, fill="both", expand=True)
        
        status_title = ctk.CTkLabel(self.status_card, text="TELEMETRÍA EN VIVO", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), text_color=Theme.NEON_GREEN)
        status_title.pack(pady=(12, 4), padx=15, anchor="w")
        
        self.telemetry_label = ctk.CTkLabel(self.status_card, text="", font=ctk.CTkFont(family="Consolas", size=10), justify="left", text_color=Theme.TEXT_MUTED)
        self.telemetry_label.pack(pady=(0, 12), padx=15, anchor="w")

        # ----------------------------------------------------
        # WORKSPACE CENTRAL DE PESTAÑAS
        # ----------------------------------------------------
        self.tabs = ctk.CTkTabview(
            self, corner_radius=20, 
            fg_color=("#f8fafc", "#0f172a"), 
            segmented_button_selected_color=Theme.ACCENT,
            segmented_button_selected_hover_color=Theme.ACCENT_HOVER,
            segmented_button_unselected_hover_color="#1e293b"
        )
        self.tabs.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        
        tab_clock_ref = self.tabs.add("Reloj Principal")
        tab_sw_ref = self.tabs.add("Cronómetro Pro")
        tab_pomodoro_ref = self.tabs.add("Enfoque Pomodoro")
        tab_alarm_ref = self.tabs.add("Alarmas Pro")

        # Inicialización e inyección
        self.clock_view = ClockView(tab_clock_ref, self)
        self.clock_view.pack(fill="both", expand=True, padx=15, pady=15)

        self.stopwatch_view = StopwatchView(tab_sw_ref)
        self.stopwatch_view.pack(fill="both", expand=True, padx=15, pady=15)

        self.pomodoro_view = PomodoroView(tab_pomodoro_ref)
        self.pomodoro_view.pack(fill="both", expand=True, padx=15, pady=15)

        # Inicialización del Sistema de Alarma Integrado
        self.alarm_time = {"hour": "00", "minute": "00"}
        self.alarm_active = False
        self.alarm_triggering = False
        
        self.alarm_view = AlarmView(tab_alarm_ref, self)
        self.alarm_view.pack(fill="both", expand=True, padx=15, pady=15)

        self.update_loop()

    def toggle_format(self):
        self.is_24h_format = self.switch_format.get() == 1

    def set_timezone(self, choice):
        self.current_timezone = choice

    def toggle_theme(self):
        if self.switch_theme.get() == 1:
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")

    def get_time(self):
        if self.current_timezone == "Local":
            return datetime.now()
        return datetime.now(pytz.timezone(self.current_timezone))

    def update_loop(self):
        now = self.get_time()
        active_tab = self.tabs.get()

        # Renderizar vista activa
        if active_tab == "Reloj Principal":
            self.clock_view.update_view(now, self.is_24h_format)
        elif active_tab == "Cronómetro Pro":
            self.stopwatch_view.tick()
        elif active_tab == "Enfoque Pomodoro":
            self.pomodoro_view.tick()
        elif active_tab == "Alarmas Pro":
            self.alarm_view.update_view()

        # Monitor de Alarma Core (Comprobación a nivel de minuto)
        if self.alarm_active and not self.alarm_triggering:
            current_hour = now.strftime("%H")
            current_min = now.strftime("%M")
            if current_hour == self.alarm_time["hour"] and current_min == self.alarm_time["minute"]:
                self.trigger_alarm()

        # Manejo de Interrupción Visual en Pantalla si la alarma está disparada
        if self.alarm_triggering:
            # Efecto estroboscópico alternando colores en el fondo del panel de telemetría
            color_flash = Theme.DANGER if now.second % 2 == 0 else "#070b12"
            self.status_card.configure(fg_color=color_flash)
            if now.second % 2 == 0:
                self.bell() # Pitido nativo del OS sin usar librerías externas pesadas
        else:
            self.status_card.configure(fg_color="#070b12")

        # Actualizar Telemetría Dinámica en el Sidebar
        ms = now.microsecond // 1000
        alarm_status_string = f"ON ({self.alarm_time['hour']}:{self.alarm_time['minute']})" if self.alarm_active else "OFF"
        telemetry_text = (
            f"• Core Freq: 50Hz (20ms)\n"
            f"• Sync Ref: pytz {self.current_timezone}\n"
            f"• Alarm Engine: {alarm_status_string}\n"
            f"• Engine Cycle: {ms:03d}ms"
        )
        self.telemetry_label.configure(text=telemetry_text)

        # Loop continuo balanceado de alto rendimiento
        self.after(20, self.update_loop)


    def trigger_alarm(self):
        self.alarm_triggering = True
        self.tabs.set("Alarmas Pro") # Forzar foco a la pestaña para que el usuario responda
        self.alarm_view.show_trigger_ui()

    def stop_alarm(self):
        self.alarm_triggering = False
        self.alarm_active = False
        self.alarm_view.reset_ui_state()

if __name__ == "__main__":
    app = AuraClockHorizon()
    app.mainloop()