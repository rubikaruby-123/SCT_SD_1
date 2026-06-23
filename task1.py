import os
import math
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import pyttsx3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Initialize voice engine
try:
    engine = pyttsx3.init()
except Exception:
    engine = None

# --- CYBER PINK X / NEON SAKURA PALETTE CONFIG ---
BG_COLOR        = "#0D1117"   # Deep Obsidian
CARD_COLOR      = "#161B22"   # Dark Tech Gray
PRIMARY_COLOR   = "#FF00FF"   # Electric Neon Pink
HOVER_COLOR     = "#D946EF"   # Cyber Magenta
TEXT_COLOR      = "#FFFFFF"   # Pure White
ACCENT_COLOR    = "#00F5FF"   # Electric Cyber Cyan
INPUT_BG        = "#21262D"   # Accent Input Slate

# Vector UI Thermometer Dynamic Fluid States
COLOR_COLD      = "#00F5FF"   # Electric Cyan
COLOR_NORMAL    = "#00FF99"   # Neon Green
COLOR_WARM      = "#FFD700"   # Bright Yellow-Gold
COLOR_HOT       = "#FF00FF"   # Neon Cyber Pink

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

history_data = []
favorites_data = []

class CyberTempX(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("⚡ CyberTemp X - Premium Temperature Suite")
        self.geometry("1200x760")
        self.configure(fg_color=BG_COLOR)
        
        # State tracking values for vector thermometer
        self.current_mercury_y = 150.0
        self.target_mercury_y = 150.0

        # Primary utility application tabs framework
        self.tabview = ctk.CTkTabview(
            self, 
            segmented_button_fg_color=CARD_COLOR, 
            segmented_button_selected_color=PRIMARY_COLOR,
            segmented_button_selected_hover_color=HOVER_COLOR,
            text_color=TEXT_COLOR
        )
        self.tabview.pack(fill="both", expand=True, padx=15, pady=10)
        self.tabview.configure(fg_color=BG_COLOR)
        
        self.main_tab = self.tabview.add("📊 Cyber Dashboard")
        self.calc_tab = self.tabview.add("🧮 Matrix Calculator")

        self.setup_converter_dashboard()
        self.setup_scientific_calculator()
        
        # Start core vector update loops
        self.refresh_canvas_vector_animations()

    # ---------------- MAIN CONVERTER HUB ---------------- #
    def setup_converter_dashboard(self):
        # Left Panel Workspace Layout
        left_panel = ctk.CTkFrame(self.main_tab, fg_color="transparent")
        left_panel.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        # Right Side Analytics Panel Frame
        right_panel = ctk.CTkFrame(self.main_tab, width=370, fg_color=CARD_COLOR, border_width=1, border_color="#30363D", corner_radius=16)
        right_panel.pack(side="right", fill="both", expand=False, padx=(5, 10), pady=10)
        right_panel.pack_propagate(False)

        # --- LEFT PANEL ELEMENTS ---
        # Decorative Title Header Card
        header_card = ctk.CTkFrame(left_panel, fg_color=CARD_COLOR, border_width=1, border_color="#30363D", corner_radius=12)
        header_card.pack(fill="x", pady=(0, 10), padx=5)

        main_title = ctk.CTkLabel(header_card, text="⚡ TEMPERATURE CONVERTOR", font=("Arial", 28, "bold"), text_color=PRIMARY_COLOR)
        main_title.pack(pady=(12, 2))
        
        subtitle = ctk.CTkLabel(header_card, text="Advanced Temperature Virtualization Interface • SkillCraft Engineering Suite", font=("Arial", 12), text_color=ACCENT_COLOR)
        subtitle.pack(pady=(0, 12))

        # Precision Config Adjustment Grid Segment Row
        control_row = ctk.CTkFrame(left_panel, fg_color="transparent")
        control_row.pack(pady=5)
        
        input_lbl = ctk.CTkLabel(control_row, text="✏️ Telemetry Input Value:", font=("Arial", 13, "bold"), text_color=TEXT_COLOR)
        input_lbl.grid(row=0, column=0, padx=10)
        
        self.live_convert_var = tk.BooleanVar(value=True)
        self.live_chk = ctk.CTkCheckBox(control_row, text="Continuous Real-time Parsing", variable=self.live_convert_var, font=("Arial", 12), text_color=TEXT_COLOR, fg_color=PRIMARY_COLOR, hover_color=HOVER_COLOR)
        self.live_chk.grid(row=0, column=1, padx=10)
        
        prec_lbl = ctk.CTkLabel(control_row, text="Precision:", font=("Arial", 12), text_color=TEXT_COLOR)
        prec_lbl.grid(row=0, column=2, padx=(10, 2))
        
        self.precision_var = tk.StringVar(value="2")
        self.precision_menu = ctk.CTkOptionMenu(control_row, values=["1", "2", "3", "4"], width=65, variable=self.precision_var, fg_color=CARD_COLOR, button_color=PRIMARY_COLOR, button_hover_color=HOVER_COLOR, command=self.trigger_live_conversion)
        self.precision_menu.grid(row=0, column=3, padx=5)

        # Main Entry Field
        self.temp_entry = ctk.CTkEntry(left_panel, width=450, height=50, font=("Arial", 22), justify="center", placeholder_text="Inject data values...", fg_color=INPUT_BG, text_color=TEXT_COLOR, border_color=PRIMARY_COLOR, corner_radius=8)
        self.temp_entry.pack(pady=10)
        self.temp_entry.bind("<KeyRelease>", self.trigger_live_conversion)

        # Macro Presets Acceleration Bar Row
        preset_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        preset_frame.pack(pady=5)
        
        presets = [("❄️ Cryo (0°C)", 0), ("🏠 Habitual (25°C)", 25), ("🧬 Bio (37°C)", 37), ("🔥 Thermal (100°C)", 100)]
        for text, val in presets:
            btn = ctk.CTkButton(preset_frame, text=text, width=115, height=34, fg_color=CARD_COLOR, hover_color="#21262D", border_width=1, border_color=PRIMARY_COLOR, text_color=TEXT_COLOR, font=("Arial", 11, "bold"), command=lambda v=val: self.load_preset(v))
            btn.pack(side="left", padx=4)

        # Mathematical Transformation Scale Directives Matrix
        unit_frame = ctk.CTkFrame(left_panel, fg_color=CARD_COLOR, border_width=1, border_color="#30363D", corner_radius=12)
        unit_frame.pack(pady=15, padx=5, fill="x")
        unit_frame.grid_columnconfigure(0, weight=1)
        unit_frame.grid_columnconfigure(2, weight=1)
        
        from_lbl = ctk.CTkLabel(unit_frame, text="Source Transmit Scale", font=("Arial", 12, "bold"), text_color=ACCENT_COLOR)
        from_lbl.grid(row=0, column=0, pady=(8, 2))
        self.from_unit = ctk.CTkOptionMenu(unit_frame, values=["Celsius", "Fahrenheit", "Kelvin"], width=160, height=35, fg_color=INPUT_BG, button_color=PRIMARY_COLOR, button_hover_color=HOVER_COLOR, command=self.trigger_live_conversion)
        self.from_unit.grid(row=1, column=0, padx=20, pady=(0, 12))
        self.from_unit.set("Celsius")

        swap_btn = ctk.CTkButton(unit_frame, text="🔄 Invert Vectors", width=130, height=35, fg_color=PRIMARY_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR, font=("Arial", 12, "bold"), command=self.swap_units)
        swap_btn.grid(row=1, column=1, pady=(0, 12))

        to_lbl = ctk.CTkLabel(unit_frame, text="Target Resolution Scale", font=("Arial", 12, "bold"), text_color=ACCENT_COLOR)
        to_lbl.grid(row=0, column=2, pady=(8, 2))
        self.to_unit = ctk.CTkOptionMenu(unit_frame, values=["Celsius", "Fahrenheit", "Kelvin"], width=160, height=35, fg_color=INPUT_BG, button_color=PRIMARY_COLOR, button_hover_color=HOVER_COLOR, command=self.trigger_live_conversion)
        self.to_unit.grid(row=1, column=2, padx=20, pady=(0, 12))
        self.to_unit.set("Fahrenheit")

        # Execution Controls Activation Strip Row
        action_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        action_frame.pack(pady=5)
        
        self.convert_btn = ctk.CTkButton(action_frame, text="⚡ Compute Matrix", width=180, height=45, fg_color=PRIMARY_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR, font=("Arial", 14, "bold"), command=self.perform_explicit_conversion)
        self.convert_btn.grid(row=0, column=0, padx=10)
        
        clear_btn = ctk.CTkButton(action_frame, text="🧹 Flush Telemetry Entry", width=180, height=45, fg_color="#21262D", hover_color="#30363D", text_color=TEXT_COLOR, font=("Arial", 14, "bold"), command=self.clear_all_fields)
        clear_btn.grid(row=0, column=1, padx=10)

        # Output Card Evaluation Banner Readouts
        self.result_display_lbl = ctk.CTkLabel(left_panel, text="0.00° Celsius = 32.00° Fahrenheit", font=("Arial", 22, "bold"), text_color=COLOR_NORMAL)
        self.result_display_lbl.pack(pady=15)
        
        self.formula_lbl = ctk.CTkLabel(left_panel, text="Formula Matrix Vector: (Celsius × 9/5) + 32", font=("Arial", 13, "italic"), text_color=ACCENT_COLOR)
        self.formula_lbl.pack()

        # Operational Archive Memory Commits Row Actions Bar
        utility_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        utility_frame.pack(pady=15)
        
        copy_btn = ctk.CTkButton(utility_frame, text="📋 Copy Log Result", width=150, fg_color=CARD_COLOR, hover_color="#21262D", text_color=TEXT_COLOR, border_width=1, border_color=PRIMARY_COLOR, font=("Arial", 12, "bold"), command=self.copy_output_to_clipboard)
        copy_btn.grid(row=0, column=0, padx=6)
        
        fav_btn = ctk.CTkButton(utility_frame, text="⭐ Pin To Core Deck", width=150, fg_color=CARD_COLOR, hover_color="#21262D", text_color=TEXT_COLOR, border_width=1, border_color=PRIMARY_COLOR, font=("Arial", 12, "bold"), command=self.add_current_to_favorites)
        fav_btn.grid(row=0, column=1, padx=6)

        # Core Technical System Information Signatures Footer Row
        footer_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", pady=5)
        
        credit_lbl = ctk.CTkLabel(footer_frame, text="👾 CyberCore System Status: Active", font=("Arial", 11, "bold", "italic"), text_color=PRIMARY_COLOR)
        credit_lbl.pack(side="left", padx=15)
        
        about_btn = ctk.CTkButton(footer_frame, text="ℹ️ Environmental Suite Profile", width=160, fg_color=CARD_COLOR, hover_color="#21262D", text_color=TEXT_COLOR, font=("Arial", 11), command=lambda: messagebox.showinfo("Suite Build Manifest", "CyberTemp X Pro Engine\nSkillCraft Technology Internship Automated Portfolio Module"))
        about_btn.pack(side="right", padx=15)

        # --- RIGHT SIDEBAR PANEL ELEMENTS ---
        measuring_title = ctk.CTkLabel(right_panel, text="🗺️ Real-time Measuring Tube Gauge", font=("Arial", 14, "bold"), text_color=PRIMARY_COLOR)
        measuring_title.pack(pady=(12, 2))

        # Custom Cyber-Stitched Vector Gauges Graphic Canvas Model
        self.thermometer_canvas = tk.Canvas(right_panel, width=330, height=170, bg=BG_COLOR, highlightthickness=1, highlightbackground="#30363D")
        self.thermometer_canvas.pack(fill="x", padx=15, pady=5)

        hist_title = ctk.CTkLabel(right_panel, text="📝 Serial Conversion History Registers", font=("Arial", 14, "bold"), text_color=TEXT_COLOR)
        hist_title.pack(pady=(10, 2))

        self.search_entry = ctk.CTkEntry(right_panel, height=30, placeholder_text="🔍 Filter localized database index values...", fg_color=INPUT_BG, text_color=TEXT_COLOR, border_color="#30363D", corner_radius=6)
        self.search_entry.pack(fill="x", padx=15, pady=2)
        self.search_entry.bind("<KeyRelease>", self.filter_history_display_log)

        self.history_textbox = ctk.CTkTextbox(right_panel, height=105, font=("Courier New", 11), fg_color=INPUT_BG, border_width=1, border_color="#30363D", text_color=TEXT_COLOR)
        self.history_textbox.pack(fill="x", padx=15, pady=4)
        self.history_textbox.configure(state="disabled")

        # Serial File Synchronization Exporters Action Strip Row Bar
        export_row = ctk.CTkFrame(right_panel, fg_color="transparent")
        export_row.pack(fill="x", padx=15, pady=2)
        
        txt_btn = ctk.CTkButton(export_row, text="📄 TXT Log", fg_color=PRIMARY_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR, font=("Arial", 11, "bold"), width=105, command=lambda: self.export_raw_data_logs("txt"))
        txt_btn.grid(row=0, column=0, padx=(0, 4))
        
        csv_btn = ctk.CTkButton(export_row, text="📊 CSV Matrix", fg_color=PRIMARY_COLOR, hover_color=HOVER_COLOR, text_color=TEXT_COLOR, font=("Arial", 11, "bold"), width=110, command=lambda: self.export_raw_data_logs("csv"))
        csv_btn.grid(row=0, column=1, padx=4)
        
        clear_hist_btn = ctk.CTkButton(export_row, text="🗑️ Purge Logs", fg_color="#21262D", hover_color="#30363D", text_color=TEXT_COLOR, font=("Arial", 11), width=105, command=self.clear_history_log_database)
        clear_hist_btn.grid(row=0, column=2, padx=(4, 0))

        pdf_report_btn = ctk.CTkButton(right_panel, text="📂 Generate Executive PDF Analytics Data", fg_color="#16a34a", hover_color="#15803d", text_color=TEXT_COLOR, height=35, font=("Arial", 12, "bold"), corner_radius=6, command=self.compile_pdf_analytics_report)
        pdf_report_btn.pack(fill="x", padx=15, pady=6)

        # Embedded Live Data Variations Chart Module Graph Frame Canvas Area
        trend_title = ctk.CTkLabel(right_panel, text="📈 Historical Session Variations Plot Line", font=("Arial", 12, "bold"), text_color=TEXT_COLOR)
        trend_title.pack(pady=(6, 2))
        
        self.chart_container_frame = ctk.CTkFrame(right_panel, height=135, fg_color=BG_COLOR, border_width=1, border_color="#30363D")
        self.chart_container_frame.pack(fill="both", expand=True, padx=15, pady=(2, 6))
        self.initialize_empty_embedded_trend_chart()

        # Favorites Array Pin Storage Core Deck UI Panel View Box Module Frame
        fav_title_lbl = ctk.CTkLabel(right_panel, text="⭐ Core Favorites Reference Pin Deck Registry", font=("Arial", 12, "bold"), text_color=PRIMARY_COLOR)
        fav_title_lbl.pack(pady=(4, 2))
        
        self.favorites_textbox = ctk.CTkTextbox(right_panel, height=65, font=("Arial", 11), fg_color=INPUT_BG, border_width=1, border_color="#30363D", text_color=TEXT_COLOR)
        self.favorites_textbox.pack(fill="x", padx=15, pady=(0, 12))
        self.favorites_textbox.insert("end", "No calculated metric coordinates pinned onto favorite core deck references index registry yet.")
        self.favorites_textbox.configure(state="disabled")

    # ---------------- GRAPHICS RENDER ENGINE GAUGE PROCEDURES ---------------- #
    def refresh_canvas_vector_animations(self):
        # Linearly interpolate gaps differences coordinates calculations steps
        gap = self.target_mercury_y - self.current_mercury_y
        if abs(gap) > 0.2:
            self.current_mercury_y += gap * 0.15
        else:
            self.current_mercury_y = self.target_mercury_y

        self.thermometer_canvas.delete("all")
        
        # Adaptive fluid assignments based on temperature bounds
        if self.current_mercury_y < 75.0:
            fluid_color = COLOR_HOT
        elif self.current_mercury_y < 120.0:
            fluid_color = COLOR_WARM
        elif self.current_mercury_y < 180.0:
            fluid_color = COLOR_NORMAL
        else:
            fluid_color = COLOR_COLD

        # Shell drawing structural operations tags markers
        self.thermometer_canvas.create_rectangle(30, 75, 250, 95, fill=INPUT_BG, outline="#30363D", width=2, tags="shell")
        self.thermometer_canvas.create_oval(240, 65, 275, 105, fill=INPUT_BG, outline="#30363D", width=2, tags="bulb")
        
        # Inner levels fluid tracking vector overlay matrices
        self.thermometer_canvas.create_rectangle(32, 78, int(self.current_mercury_y), 92, fill=fluid_color, outline="")
        self.thermometer_canvas.create_oval(243, 68, 272, 102, fill=fluid_color, outline="")

        # Markers layout values scaling mapping definitions parameters overrides
        for x_val, label in [(40, "-20°C"), (90, "0°C"), (140, "25°C"), (190, "50°C"), (235, "100°C")]:
            self.thermometer_canvas.create_line(x_val, 95, x_val, 102, fill=PRIMARY_COLOR, width=1)
            self.thermometer_canvas.create_text(x_val, 114, text=label, fill=TEXT_COLOR, font=("Arial", 9, "bold"))

        # Re-trigger pipeline update callback tick rate sequences logs
        self.after(30, self.refresh_canvas_vector_animations)

    # ---------------- CALCULATIONS PIPELINES WORKFLOW ENGINE ---------------- #
    def execute_conversion_pipeline(self, explicit=False):
        try:
            raw_input = self.temp_entry.get()
            if not raw_input:
                return
            
            val = float(raw_input)
            f_unit = self.from_unit.get()
            t_unit = self.to_unit.get()
            precision = int(self.precision_var.get())

            if f_unit == "Celsius":
                c = val
            elif f_unit == "Fahrenheit":
                c = (val - 32) * 5/9
            else:
                c = val - 273.15

            if f_unit == "Kelvin" and val < 0:
                messagebox.showerror("Validation Edge Restriction Hit", "Absolute Zero limit boundary reached. Kelvin expressions cannot evaluate values below zero.")
                return

            if t_unit == "Celsius":
                res = c
                formula = "C = C" if f_unit == "Celsius" else ("C = (F - 32) × 5/9" if f_unit == "Fahrenheit" else "C = K - 273.15")
            elif t_unit == "Fahrenheit":
                res = (c * 9/5) + 32
                formula = "F = (C × 9/5) + 32" if f_unit == "Celsius" else ("F = F" if f_unit == "Fahrenheit" else "F = (K - 273.15) × 9/5 + 32")
            else:
                res = c + 273.15
                formula = "K = C + 273.15" if f_unit == "Celsius" else ("K = (F - 32) × 5/9 + 273.15" if f_unit == "Fahrenheit" else "K = K")

            # Determine localized text readouts dynamic status colorization layers
            if c <= 0:
                display_color = COLOR_COLD
            elif c <= 25:
                display_color = COLOR_NORMAL
            elif c <= 40:
                display_color = COLOR_WARM
            else:
                display_color = COLOR_HOT

            # Update core labels readout string properties configurations tokens
            self.result_display_lbl.configure(text=f"{val:.{precision}f}° {f_unit} = {res:.{precision}f}° {t_unit}", text_color=display_color)
            self.formula_lbl.configure(text=f"Formula Matrix Vector: {formula}")

            # Slide thermometer vector tracking needles points map metrics bounds
            clamped_c = max(-20, min(100, c))
            percentage = (clamped_c - (-20)) / (100 - (-20))
            self.target_mercury_y = 32.0 + (percentage * (243.0 - 32.0))

            if explicit:
                timestamp = datetime.now().strftime("%H:%M:%S")
                record = {
                    "time": timestamp,
                    "log_line": f"[{timestamp}] {val:.2f}° {f_unit} ➔ {res:.2f}° {t_unit}",
                    "raw_celsius": c,
                    "conversion_text": f"{val:.2f}° {f_unit} = {res:.2f}° {t_unit}"
                }
                history_data.append(record)
                self.refresh_history_log_viewer()
                self.update_embedded_trend_chart_graphics()
                
                if engine:
                    engine.say(f"{val:.1f} degrees {f_unit} is equivalent to {res:.1f} degrees {t_unit}")
                    engine.runAndWait()

        except ValueError:
            if explicit:
                messagebox.showerror("Parse Pipeline Exception", "Failed to resolve characters string structure. Ensure entry expression values are clean numerics matrix structures.")

    def trigger_live_conversion(self, *args):
        if self.live_convert_var.get():
            self.execute_conversion_pipeline(explicit=False)

    def perform_explicit_conversion(self):
        self.execute_conversion_pipeline(explicit=True)

    def load_preset(self, val):
        self.from_unit.set("Celsius")
        self.temp_entry.delete(0, "end")
        self.temp_entry.insert("end", str(val))
        self.execute_conversion_pipeline(explicit=True)

    def swap_units(self):
        f, t = self.from_unit.get(), self.to_unit.get()
        self.from_unit.set(t)
        self.to_unit.set(f)
        self.trigger_live_conversion()

    def clear_all_fields(self):
        self.temp_entry.delete(0, "end")
        self.result_display_lbl.configure(text="0.00° Celsius = 0.00° Fahrenheit", text_color=COLOR_NORMAL)
        self.formula_lbl.configure(text="Formula Matrix Vector: --")
        self.target_mercury_y = 120.0

    def copy_output_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.result_display_lbl.cget("text"))
        messagebox.showinfo("Clipboard Frame Synced", "Text data readout strings successfully piped to core clipboard memory allocations buffers.")

    def add_current_to_favorites(self):
        curr_text = self.result_display_lbl.cget("text")
        if curr_text and curr_text not in favorites_data:
            favorites_data.append(curr_text)
            self.favorites_textbox.configure(state="normal")
            self.favorites_textbox.delete("1.0", "end")
            for fav in favorites_data:
                self.favorites_textbox.insert("end", f"⭐ {fav}\n")
            self.favorites_textbox.configure(state="disabled")

    # ---------------- HISTORY LOG REGISTRY SELECTION WORKSPACE ---------------- #
    def refresh_history_log_viewer(self, filter_text=""):
        self.history_textbox.configure(state="normal")
        self.history_textbox.delete("1.0", "end")
        for item in history_data:
            if filter_text.lower() in item["log_line"].lower():
                self.history_textbox.insert("end", item["log_line"] + "\n")
        self.history_textbox.configure(state="disabled")

    def filter_history_display_log(self, event):
        self.refresh_history_log_viewer(self.search_entry.get())

    def clear_history_log_database(self):
        global history_data
        history_data = []
        self.refresh_history_log_viewer()
        self.initialize_empty_embedded_trend_chart()

    def export_raw_data_logs(self, file_type):
        if not history_data:
            messagebox.showwarning("Log Trace Exception", "Log data structures empty. Export process halted.")
            return
        
        filename = f"history.{file_type}"
        with open(filename, "w", encoding="utf-8") as f:
            if file_type == "csv":
                f.write("Time,Conversion Details\n")
            for item in history_data:
                if file_type == "csv":
                    f.write(f"{item['time']},{item['conversion_text']}\n")
                else:
                    f.write(f"{item['log_line']}\n")
        messagebox.showinfo("Export Synchronization Complete", f"Data records successfully written and saved locally within system path workspace file environments as '{filename}'.")

    # ---------------- MATPLOTLIB PLOT LIVE CORE ---------------- #
    def initialize_empty_embedded_trend_chart(self):
        for widget in self.chart_container_frame.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots(figsize=(3.4, 1.4), dpi=100)
        ax.plot([], [])
        ax.set_facecolor(BG_COLOR)
        fig.patch.set_facecolor(BG_COLOR)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        canvas_plot = FigureCanvasTkAgg(fig, master=self.chart_container_frame)
        canvas_plot.draw()
        canvas_plot.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    def update_embedded_trend_chart_graphics(self):
        if not history_data:
            return
        
        for widget in self.chart_container_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(3.4, 1.4), dpi=100)
        celsius_points = [item["raw_celsius"] for item in history_data]
        
        # Cyber-glowing lines vector mapping configurations paths
        ax.plot(celsius_points, marker='o', color=PRIMARY_COLOR, linestyle='-', linewidth=2, markersize=4)
        ax.set_facecolor(BG_COLOR)
        fig.patch.set_facecolor(BG_COLOR)
        
        ax.tick_params(colors=TEXT_COLOR, labelsize=8)
        ax.grid(True, linestyle='--', alpha=0.15, color=TEXT_COLOR)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color("#30363D")
        ax.spines['left'].set_color("#30363D")
        
        canvas_plot = FigureCanvasTkAgg(fig, master=self.chart_container_frame)
        canvas_plot.draw()
        canvas_plot.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)

    # ---------------- REPORTLAB PDF EXPORTER MODULE ---------------- #
    def compile_pdf_analytics_report(self):
        if not history_data:
            messagebox.showwarning("Log Database Underflow", "Zero tracked metrics coordinates present within system workspace logs arrays.")
            return
            
        pdf_filename = "Temperature_Conversion_Report.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        
        c.setFont("Helvetica-Bold", 22)
        c.drawString(50, 740, "Temperature Converter Pro V6")
        c.setFont("Helvetica", 10)
        c.drawString(50, 722, "Developed by Rashmi | SkillCraft Technology Internship Data Suite Pro")
        c.drawString(50, 708, f"Generated: {datetime.now().strftime('%d %b %Y %H:%M:%S')}")
        c.line(50, 695, 560, 695)
        
        y = 660
        c.setFont("Helvetica-Bold", 12)
        c.setFillColorRGB(1.0, 0.0, 1.0) # Cyber Pink token reference RGB specifications mappings formulas
        c.rect(50, y-4, 510, 20, fill=True, stroke=False)
        c.setFillColorRGB(1, 1, 1)
        c.drawString(60, y, "Time")
        c.drawString(150, y, "Conversion Details Log Summary")
        
        y -= 25
        c.setFillColorRGB(0.05, 0.05, 0.05)
        c.setFont("Helvetica", 10)
        
        for item in history_data[-15:]:
            if y < 80:
                break
            c.drawString(60, y, item["time"])
            c.drawString(150, y, item["conversion_text"])
            c.line(50, y-6, 560, y-6)
            y -= 24

        c.save()
        messagebox.showinfo("PDF Summary Engine Export Completed", f"Analytical documentation trace successfully summarized and output onto local files workspace directory paths as '{pdf_filename}'.")

    # ---------------- MATRIX SCIENTIFIC CALCULATOR ---------------- #
    def setup_scientific_calculator(self):
        self.calc_display = ctk.CTkEntry(self.calc_tab, width=450, height=55, font=("Arial", 22), justify="right", fg_color=INPUT_BG, text_color=TEXT_COLOR, border_color=PRIMARY_COLOR)
        self.calc_display.pack(pady=20, padx=20)
        
        grid_frame = ctk.CTkFrame(self.calc_tab, fg_color="transparent")
        grid_frame.pack(pady=5)
        
        button_matrix = [
            ('7', '8', '9', '/', 'sin'),
            ('4', '5', '6', '*', 'cos'),
            ('1', '2', '3', '-', 'tan'),
            ('0', '.', '+', '=', 'log'),
            ('(', ')', 'sqrt', '^', 'C')
        ]
        
        for r, row in enumerate(button_matrix):
            for c, text in enumerate(row):
                cmd = lambda t=text: self.on_calc_button_click(t)
                
                if text.isalpha() or text in ['/', '*', '-', '+', '=', '^']:
                    b_color = PRIMARY_COLOR
                    h_color = HOVER_COLOR
                else:
                    b_color = CARD_COLOR
                    h_color = "#21262D"
                    
                if text == '=': 
                    b_color = "#16a34a"
                    h_color = "#15803d"
                if text == 'C': 
                    b_color = "#dc2626"
                    h_color = "#b91c1c"
                
                btn = ctk.CTkButton(grid_frame, text=text, width=85, height=48, fg_color=b_color, hover_color=h_color, text_color=TEXT_COLOR, font=("Arial", 14, "bold"), border_width=1 if b_color == CARD_COLOR else 0, border_color=PRIMARY_COLOR)
                btn.grid(row=r, column=c, padx=6, pady=6)

    def on_calc_button_click(self, char):
        current_text = self.calc_display.get()
        if char == 'C':
            self.calc_display.delete(0, "end")
        elif char == '=':
            try:
                expr = current_text.replace('^', '**')
                safe_dict = {
                    "sin": lambda x: math.sin(math.radians(x)),
                    "cos": lambda x: math.cos(math.radians(x)),
                    "tan": lambda x: math.tan(math.radians(x)),
                    "log": lambda x: math.log10(x) if x > 0 else ValueError,
                    "sqrt": math.sqrt
                }
                res = eval(expr, {"__builtins__": None}, safe_dict)
                self.calc_display.delete(0, "end")
                self.calc_display.insert("end", f"{res:.6g}")
            except Exception:
                self.calc_display.delete(0, "end")
                self.calc_display.insert("end", "Error")
        else:
            if char in ['sin', 'cos', 'tan', 'log', 'sqrt']:
                self.calc_display.insert("end", f"{char}(")
            else:
                self.calc_display.insert("end", char)

if __name__ == "__main__":
    app = CyberTempX()
    app.mainloop()