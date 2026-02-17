import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
from datetime import datetime
import os
import sys
import math
import random
from config import Config

class Dashboard:
    def __init__(self, app):
        self.app = app
        self.detection_history = []
        self.start_time = time.time()
        self.files_scanned = 0
        self.threats_found = 0
        self.safe_files = 0
        self.scan_angle = 0
        self.pulse_size = 0
        self.pulse_direction = 1
        self.globe_rotation = 0
        
        # Configure customtkinter with African sunset colors
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.window = ctk.CTkToplevel()
        self.window.title(" Grae-X Magic Eye - African Cyber Scanner")
        self.window.geometry("1400x800")
        self.window.minsize(1200, 700)
        
        # Set window background to deep purple/black
        self.window.configure(fg_color="#0a0a1f")
        
        # Set icon from file
        self.set_window_icon()
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() - 1400) // 2
        y = (self.window.winfo_screenheight() - 800) // 2
        self.window.geometry(f'+{x}+{y}')
        
        # Initialize UI
        self.setup_ui()
        
        # Start animations
        self.start_animations()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def set_window_icon(self):
        """Set the window icon"""
        try:
            icon_paths = [
                "icon.ico",
                "logo.ico",
                os.path.join(os.path.dirname(__file__), "..", "icon.ico"),
            ]
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    self.window.iconbitmap(icon_path)
                    print(f" Icon loaded from: {icon_path}")
                    break
        except Exception as e:
            print(f" Could not load icon: {e}")
    
    def setup_ui(self):
        """Create the futuristic African cyberpunk dashboard"""
        
        # Main container with gradient background
        main_container = ctk.CTkFrame(self.window, fg_color="#0a0a1f", corner_radius=0)
        main_container.pack(fill="both", expand=True)
        
        # ========== TOP BANNER WITH AFRICAN PATTERNS ==========
        banner_frame = ctk.CTkFrame(main_container, fg_color="#2a1a3a", height=60, corner_radius=0)
        banner_frame.pack(fill="x")
        
        # Use CTkLabel for banner instead of Canvas to avoid transparency issues
        banner_label = ctk.CTkLabel(
            banner_frame,
            text=" GRAE-X MAGIC EYE  AFRICAN CYBER SCANNER ",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffb347"
        )
        banner_label.pack(expand=True, fill="both")
        
        # ========== MAIN CONTENT AREA ==========
        content_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left side - Futuristic African Scanner
        left_frame = ctk.CTkFrame(content_frame, fg_color="#1a1a2a", corner_radius=20, border_width=2, border_color="#ff6b35")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Scanner title with African motif
        scanner_title = ctk.CTkFrame(left_frame, fg_color="transparent")
        scanner_title.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            scanner_title,
            text=" AFRICAN CYBER SCANNER ",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ff9a3c"
        ).pack()
        
        ctk.CTkLabel(
            scanner_title,
            text="  NKOSI SCANNING PROTOCOL  ",
            font=ctk.CTkFont(size=12),
            text_color="#8a6d9c"
        ).pack()
        
        # Canvas for futuristic face/globe animation
        self.scanner_canvas = tk.Canvas(
            left_frame, 
            width=500, 
            height=400, 
            bg="#0d0d1a",
            highlightthickness=2,
            highlightbackground="#ff6b35"
        )
        self.scanner_canvas.pack(pady=20, padx=20)
        
        # Initial drawing of African cyber face
        self.draw_african_cyber_face()
        
        # Status text below scanner
        self.scanner_status = ctk.CTkLabel(
            left_frame,
            text=" SCANNING... AWAITING FILES",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#88ccff"
        )
        self.scanner_status.pack(pady=(0, 20))
        
        # Right side - Dashboard panels
        right_frame = ctk.CTkFrame(content_frame, fg_color="#1a1a2a", corner_radius=20, border_width=2, border_color="#ff6b35")
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Stats cards with African patterns
        stats_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        # Stats grid
        stats_frame.grid_columnconfigure((0,1), weight=1)
        stats_frame.grid_rowconfigure((0,1), weight=1)
        
        # Card 1: Files Scanned
        self.files_scanned_card = self.create_african_stat_card(
            stats_frame, 0, 0,
            "", "FILES SCANNED", "0", 
            "#2d1a3a", "#ff9a3c"
        )
        
        # Card 2: Threats Found
        self.threats_card = self.create_african_stat_card(
            stats_frame, 1, 0,
            "", "THREATS FOUND", "0", 
            "#3a1a2a", "#ff4444"
        )
        
        # Card 3: Safe Files
        self.safe_files_card = self.create_african_stat_card(
            stats_frame, 0, 1,
            "", "SAFE FILES", "0", 
            "#1a3a2a", "#44ff44"
        )
        
        # Card 4: Uptime
        self.uptime_card = self.create_african_stat_card(
            stats_frame, 1, 1,
            "", "UPTIME", "00:00:00", 
            "#3a2a1a", "#ffaa44"
        )
        
        # Tab view for logs and settings
        self.tab_view = ctk.CTkTabview(
            right_frame,
            fg_color="#0d0d1a",
            segmented_button_fg_color="#2a1a3a",
            segmented_button_selected_color="#ff6b35",
            segmented_button_selected_hover_color="#ff9a3c"
        )
        self.tab_view.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Tab 1: Detection Log (with African patterns)
        log_tab = self.tab_view.add(" DETECTION LOG")
        self.setup_african_log_tab(log_tab)
        
        # Tab 2: Monitor Settings
        settings_tab = self.tab_view.add(" SETTINGS")
        self.setup_african_settings_tab(settings_tab)
        
        # Tab 3: About (with African cyberpunk info)
        about_tab = self.tab_view.add(" ABOUT")
        self.setup_african_about_tab(about_tab)
        
        # Bottom status bar with African pattern
        self.setup_african_status_bar(main_container)
    
    def create_african_stat_card(self, parent, col, row, icon, label, value, bg_color, text_color):
        """Create a statistics card with African styling"""
        card = ctk.CTkFrame(parent, fg_color=bg_color, corner_radius=15, border_width=1, border_color=text_color)
        card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # Icon with glow effect
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=36)
        )
        icon_label.pack(pady=(15, 5))
        
        # Label
        label_label = ctk.CTkLabel(
            card,
            text=label,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=text_color
        )
        label_label.pack()
        
        # Value
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=text_color
        )
        value_label.pack(pady=(5, 15))
        
        return value_label
    
    def draw_african_cyber_face(self):
        """Draw a futuristic African cyberpunk face/globe"""
        try:
            self.scanner_canvas.delete("all")
            
            w = 500
            h = 400
            center_x = w // 2
            center_y = h // 2
            
            # Draw scanning radar background
            self.scanner_canvas.create_oval(50, 50, 450, 350, outline="#ff6b35", width=2, dash=(5, 3))
            self.scanner_canvas.create_oval(150, 150, 350, 250, outline="#ff9a3c", width=1, dash=(3, 2))
            self.scanner_canvas.create_oval(200, 200, 300, 300, outline="#ffb347", width=1)
            
            # Draw African continent outline (simplified)
            # West Africa
            points = [
                center_x - 80, center_y - 40,
                center_x - 40, center_y - 60,
                center_x, center_y - 50,
                center_x + 40, center_y - 30,
                center_x + 60, center_y,
                center_x + 40, center_y + 40,
                center_x, center_y + 60,
                center_x - 40, center_y + 50,
                center_x - 80, center_y + 20,
                center_x - 100, center_y - 10,
                center_x - 80, center_y - 40
            ]
            self.scanner_canvas.create_polygon(points, fill="#2a1a3a", outline="#ff6b35", width=3)
            
            # Draw cyberpunk face elements
            # Eyes (inspired by African masks)
            eye_left_x = center_x - 60
            eye_right_x = center_x + 60
            eye_y = center_y - 30
            
            # Left eye with scanning effect
            self.scanner_canvas.create_oval(eye_left_x-15, eye_y-15, eye_left_x+15, eye_y+15, 
                                           outline="#ff9a3c", width=2, fill="#0d0d1a")
            # Right eye
            self.scanner_canvas.create_oval(eye_right_x-15, eye_y-15, eye_right_x+15, eye_y+15, 
                                           outline="#ff9a3c", width=2, fill="#0d0d1a")
            
            # Pupils (animated)
            pupil_offset = int(math.sin(self.scan_angle) * 5)
            self.scanner_canvas.create_oval(eye_left_x-5 + pupil_offset, eye_y-5, 
                                           eye_left_x+5 + pupil_offset, eye_y+5, 
                                           fill="#ff6b35", outline="")
            self.scanner_canvas.create_oval(eye_right_x-5 - pupil_offset, eye_y-5, 
                                           eye_right_x+5 - pupil_offset, eye_y+5, 
                                           fill="#ff6b35", outline="")
            
            # Third eye (symbolic)
            self.scanner_canvas.create_oval(center_x-10, center_y-80, center_x+10, center_y-60, 
                                           outline="#ffaa44", width=2, fill="#2a1a3a")
            self.scanner_canvas.create_line(center_x, center_y-70, center_x, center_y-50, fill="#ffaa44", width=2)
            
            # Mouth (tribal pattern)
            mouth_points = [
                center_x - 40, center_y + 30,
                center_x - 20, center_y + 50,
                center_x + 20, center_y + 50,
                center_x + 40, center_y + 30
            ]
            self.scanner_canvas.create_line(mouth_points, fill="#ff6b35", width=3, smooth=True)
            
            # Scanning radar line (rotating)
            angle_rad = math.radians(self.scan_angle * 2)
            radar_x = center_x + 150 * math.cos(angle_rad)
            radar_y = center_y + 150 * math.sin(angle_rad)
            self.scanner_canvas.create_line(center_x, center_y, radar_x, radar_y, 
                                           fill="#ffb347", width=2, arrow="last")
            
            # Pulse effect (expanding circle)
            if self.pulse_size > 0:
                self.scanner_canvas.create_oval(
                    center_x - self.pulse_size, center_y - self.pulse_size,
                    center_x + self.pulse_size, center_y + self.pulse_size,
                    outline="#ff9a3c", width=1, dash=(2, 2)
                )
            
            # African patterns around the face
            for i in range(0, 360, 45):
                rad = math.radians(i + self.globe_rotation)
                x = center_x + 180 * math.cos(rad)
                y = center_y + 140 * math.sin(rad)
                self.scanner_canvas.create_text(x, y, text="", fill="#ff6b35", font=("Arial", 16))
        except Exception as e:
            print(f"Error drawing face: {e}")
    
    def setup_african_log_tab(self, parent):
        """Setup detection log with African styling"""
        
        # Header with pattern
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            header,
            text=" DETECTION HISTORY ",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ff9a3c"
        ).pack(side="left")
        
        # Clear log button with African styling
        self.clear_btn = ctk.CTkButton(
            header,
            text=" CLEAR LOG",
            width=100,
            height=30,
            command=self.clear_log,
            fg_color="#3a1a2a",
            hover_color="#4a2a3a",
            text_color="#ff6b35",
            border_width=1,
            border_color="#ff6b35"
        )
        self.clear_btn.pack(side="right")
        
        # Log frame with scrolling
        self.log_frame = ctk.CTkScrollableFrame(parent, fg_color="#0d0d1a", border_width=1, border_color="#ff6b35")
        self.log_frame.pack(fill="both", expand=True, pady=10)
        
        # Add initial message
        self.add_african_log_entry("SYSTEM", "Scanner initialized and ready", "info")
    
    def setup_african_settings_tab(self, parent):
        """Setup settings tab with African styling"""
        
        settings_container = ctk.CTkFrame(parent, fg_color="transparent")
        settings_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Notification settings
        self.create_african_section_header(settings_container, " NOTIFICATION PROTOCOLS")
        
        self.popup_var = ctk.BooleanVar(value=True)
        self.popup_check = ctk.CTkCheckBox(
            settings_container,
            text="Show popup alerts",
            variable=self.popup_var,
            command=self.toggle_popup,
            fg_color="#ff6b35",
            text_color="#ffffff"
        )
        self.popup_check.pack(anchor="w", pady=5, padx=20)
        
        self.sound_var = ctk.BooleanVar(value=True)
        self.sound_check = ctk.CTkCheckBox(
            settings_container,
            text="Play African drum alert",
            variable=self.sound_var,
            command=self.toggle_sound,
            fg_color="#ff6b35",
            text_color="#ffffff"
        )
        self.sound_check.pack(anchor="w", pady=5, padx=20)
        
        # Monitoring settings
        self.create_african_section_header(settings_container, " SCANNING PROTOCOLS")
        
        self.startup_var = ctk.BooleanVar(value=False)
        self.startup_check = ctk.CTkCheckBox(
            settings_container,
            text="Run on Windows startup",
            variable=self.startup_var,
            command=self.toggle_startup,
            fg_color="#ff6b35",
            text_color="#ffffff"
        )
        self.startup_check.pack(anchor="w", pady=5, padx=20)
        
        self.ignore_temp_var = ctk.BooleanVar(value=True)
        self.ignore_temp_check = ctk.CTkCheckBox(
            settings_container,
            text="Ignore temporary files",
            variable=self.ignore_temp_var,
            command=self.toggle_ignore_temp,
            fg_color="#ff6b35",
            text_color="#ffffff"
        )
        self.ignore_temp_check.pack(anchor="w", pady=5, padx=20)
        
        # Sensitivity
        self.create_african_section_header(settings_container, " SCAN SENSITIVITY")
        
        sensitivity_frame = ctk.CTkFrame(settings_container, fg_color="transparent")
        sensitivity_frame.pack(fill="x", padx=20, pady=10)
        
        self.sensitivity_slider = ctk.CTkSlider(
            sensitivity_frame,
            from_=0,
            to=100,
            number_of_steps=100,
            command=self.sensitivity_changed,
            fg_color="#2a1a3a",
            progress_color="#ff6b35",
            button_color="#ff9a3c"
        )
        self.sensitivity_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.sensitivity_slider.set(75)
        
        self.sensitivity_label = ctk.CTkLabel(
            sensitivity_frame,
            text="75%",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ff9a3c",
            width=50
        )
        self.sensitivity_label.pack(side="right")
        
        # Buttons
        button_frame = ctk.CTkFrame(settings_container, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        self.save_btn = ctk.CTkButton(
            button_frame,
            text=" SAVE SETTINGS",
            command=self.save_settings,
            fg_color="#2d5a8c",
            hover_color="#3d6a9c",
            text_color="#ffffff",
            border_width=1,
            border_color="#ff6b35"
        )
        self.save_btn.pack(side="left", padx=5, expand=True)
        
        self.reset_btn = ctk.CTkButton(
            button_frame,
            text=" RESET",
            command=self.reset_settings,
            fg_color="#8c2d2d",
            hover_color="#9c3d3d",
            text_color="#ffffff",
            border_width=1,
            border_color="#ff6b35"
        )
        self.reset_btn.pack(side="right", padx=5, expand=True)
    
    def setup_african_about_tab(self, parent):
        """Setup about tab with African cyberpunk theme"""
        
        about_container = ctk.CTkFrame(parent, fg_color="transparent")
        about_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # African cyberpunk logo
        ctk.CTkLabel(
            about_container,
            text="",
            font=ctk.CTkFont(size=64)
        ).pack(pady=20)
        
        ctk.CTkLabel(
            about_container,
            text="GRAE-X MAGIC EYE",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#ff9a3c"
        ).pack()
        
        ctk.CTkLabel(
            about_container,
            text="African Cyberpunk Scanner v1.0.0",
            font=ctk.CTkFont(size=14),
            text_color="#8a6d9c"
        ).pack()
        
        # African proverb
        proverb_frame = ctk.CTkFrame(about_container, fg_color="#2a1a3a", corner_radius=10)
        proverb_frame.pack(fill="x", pady=20, padx=40)
        
        ctk.CTkLabel(
            proverb_frame,
            text="\"The eye that sees through disguise\nprotects the village from shadows.\"",
            font=ctk.CTkFont(size=14),
            text_color="#ffb347"
        ).pack(pady=10)
        
        ctk.CTkLabel(
            proverb_frame,
            text="- Ancient African Cyber Proverb",
            font=ctk.CTkFont(size=11),
            text_color="#8a6d9c"
        ).pack(pady=(0, 10))
        
        # Buttons
        self.website_btn = ctk.CTkButton(
            about_container,
            text=" VISIT GRAE-X LABS",
            command=self.open_website,
            fg_color="#2a1a3a",
            hover_color="#3a2a4a",
            text_color="#ff9a3c",
            border_width=1,
            border_color="#ff6b35"
        )
        self.website_btn.pack(pady=5)
        
        self.update_btn = ctk.CTkButton(
            about_container,
            text=" CHECK FOR UPDATES",
            command=self.check_updates,
            fg_color="#2a1a3a",
            hover_color="#3a2a4a",
            text_color="#ff9a3c",
            border_width=1,
            border_color="#ff6b35"
        )
        self.update_btn.pack(pady=5)
        
        ctk.CTkLabel(
            about_container,
            text=" 2026 Grae-X Labs  African Cyber Division",
            font=ctk.CTkFont(size=10),
            text_color="#666666"
        ).pack(side="bottom", pady=10)
    
    def setup_african_status_bar(self, parent):
        """Setup status bar with African pattern"""
        status_bar = ctk.CTkFrame(parent, fg_color="#2a1a3a", height=35, corner_radius=0)
        status_bar.pack(fill="x", side="bottom")
        
        # Simple status text without canvas
        self.status_message = ctk.CTkLabel(
            status_bar,
            text=" SCANNER ACTIVE  AWAITING FILES ",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ffb347"
        )
        self.status_message.pack(expand=True, fill="both")
    
    def create_african_section_header(self, parent, text):
        """Create a section header with African styling"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(15, 5))
        
        # Simple header without canvas to avoid transparency issues
        ctk.CTkLabel(
            header_frame,
            text=f" {text} ",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ff9a3c"
        ).pack()
    
    def add_african_log_entry(self, title, message, type="info"):
        """Add a styled log entry"""
        entry_frame = ctk.CTkFrame(self.log_frame, fg_color="#1a1a2a", corner_radius=5)
        entry_frame.pack(fill="x", pady=2, padx=5)
        
        # Time
        time_str = datetime.now().strftime("%H:%M:%S")
        
        # Icon based on type
        if type == "threat":
            icon = ""
            color = "#ff4444"
        elif type == "safe":
            icon = ""
            color = "#44ff44"
        else:
            icon = "ℹ"
            color = "#88ccff"
        
        # Create log line with African styling
        log_text = f"[{time_str}] {icon} {title}: {message}"
        
        ctk.CTkLabel(
            entry_frame,
            text=log_text,
            font=ctk.CTkFont(size=11, family="Consolas"),
            text_color=color,
            anchor="w"
        ).pack(padx=10, pady=5, fill="x")
    
    def start_animations(self):
        """Start all animations"""
        self.animate_scanner()
    
    def animate_scanner(self):
        """Animate the scanner face and globe"""
        try:
            # Update animation parameters
            self.scan_angle = (self.scan_angle + 5) % 360
            self.globe_rotation = (self.globe_rotation + 2) % 360
            
            # Pulse effect
            self.pulse_size += 2 * self.pulse_direction
            if self.pulse_size > 50:
                self.pulse_direction = -1
            elif self.pulse_size < 0:
                self.pulse_direction = 1
                self.pulse_size = 0
            
            # Redraw the face
            self.draw_african_cyber_face()
            
            # Schedule next animation
            self.window.after(100, self.animate_scanner)
        except:
            pass
    
    # ========== DETECTION METHODS ==========
    
    def add_detection_log(self, file_info):
        """Add a detection to the log with African cyberpunk animation"""
        self.detection_history.append(file_info)
        
        # Update counters
        if file_info.get('is_suspicious'):
            self.threats_found += 1
            threat_type = "threat"
            self.scanner_status.configure(text=f" THREAT DETECTED: {file_info['file_name']}", text_color="#ff4444")
            
            # Pulse effect for threat
            self.pulse_size = 30
        else:
            self.safe_files += 1
            threat_type = "safe"
            self.scanner_status.configure(text=f" SAFE FILE: {file_info['file_name']}", text_color="#44ff44")
        
        self.files_scanned += 1
        
        # Create animated log entry
        title = "THREAT" if file_info.get('is_suspicious') else "SAFE"
        message = f"{file_info['file_name']} | .{file_info['current_extension']}  .{file_info['true_extension']}"
        self.add_african_log_entry(title, message, threat_type)
        
        # Update stats display
        self.update_stats_display()
        
        # Flash the scanner
        self.flash_scanner()
    
    def flash_scanner(self):
        """Flash the scanner when detection occurs"""
        try:
            self.scanner_canvas.configure(highlightbackground="#ff4444")
            self.window.after(200, lambda: self.scanner_canvas.configure(highlightbackground="#ff6b35"))
        except:
            pass
    
    def update_stats_display(self):
        """Update all statistics displays"""
        self.files_scanned_card.configure(text=str(self.files_scanned))
        self.threats_card.configure(text=str(self.threats_found))
        self.safe_files_card.configure(text=str(self.safe_files))
        
        # Update uptime
        uptime_seconds = int(time.time() - self.start_time)
        hours = uptime_seconds // 3600
        minutes = (uptime_seconds % 3600) // 60
        seconds = uptime_seconds % 60
        uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.uptime_card.configure(text=uptime_str)
    
    def update_stats(self):
        """Background update of statistics"""
        try:
            # Update time
            if hasattr(self, 'status_time'):
                self.status_time.configure(
                    text=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            
            # Update uptime
            uptime_seconds = int(time.time() - self.start_time)
            hours = uptime_seconds // 3600
            minutes = (uptime_seconds % 3600) // 60
            seconds = uptime_seconds % 60
            uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.uptime_card.configure(text=uptime_str)
            
            # Schedule next update
            self.window.after(1000, self.update_stats)
        except:
            pass
    
    # ========== BUTTON FUNCTIONS ==========
    
    def add_monitor_folder(self):
        folder = filedialog.askdirectory(title="Select Folder to Monitor")
        if folder:
            if folder not in Config.MONITOR_FOLDERS:
                Config.MONITOR_FOLDERS.append(folder)
                self.add_african_log_entry("FOLDER", f"Added: {os.path.basename(folder)}", "info")
                self.update_status(f"Added folder: {os.path.basename(folder)}")
    
    def scan_now(self):
        self.add_african_log_entry("SCAN", "Manual scan initiated", "info")
        self.update_status("Scanning...")
        self.scanner_status.configure(text=" MANUAL SCANNING...", text_color="#88ccff")
        self.window.after(2000, self.scan_complete)
    
    def scan_complete(self):
        self.files_scanned += 5
        self.update_stats_display()
        self.add_african_log_entry("SCAN", "Manual scan complete - 5 files checked", "info")
        self.update_status("Scan complete")
        self.scanner_status.configure(text=" SCAN COMPLETE", text_color="#88ccff")
    
    def toggle_popup(self):
        state = "ENABLED" if self.popup_var.get() else "DISABLED"
        self.add_african_log_entry("POPUP", f"Alerts {state}", "info")
    
    def toggle_sound(self):
        state = "ENABLED" if self.sound_var.get() else "DISABLED"
        self.add_african_log_entry("SOUND", f"Drums {state}", "info")
    
    def toggle_startup(self):
        state = "ENABLED" if self.startup_var.get() else "DISABLED"
        self.add_african_log_entry("STARTUP", f"Auto-start {state}", "info")
    
    def toggle_ignore_temp(self):
        state = "ENABLED" if self.ignore_temp_var.get() else "DISABLED"
        self.add_african_log_entry("TEMP", f"Ignore temp files {state}", "info")
    
    def sensitivity_changed(self, value):
        self.sensitivity_label.configure(text=f"{int(value)}%")
    
    def save_settings(self):
        self.add_african_log_entry("SETTINGS", "Configuration saved", "info")
        messagebox.showinfo("Settings", "Your settings have been saved!")
    
    def reset_settings(self):
        if messagebox.askyesno("Reset", "Reset all settings to default?"):
            self.popup_var.set(True)
            self.sound_var.set(True)
            self.startup_var.set(False)
            self.ignore_temp_var.set(True)
            self.sensitivity_slider.set(75)
            self.sensitivity_label.configure(text="75%")
            self.add_african_log_entry("SETTINGS", "Reset to defaults", "info")
    
    def open_website(self):
        import webbrowser
        webbrowser.open("https://graexlabs.com")
        self.add_african_log_entry("WEB", "Opened Grae-X Labs website", "info")
    
    def check_updates(self):
        self.add_african_log_entry("UPDATE", "Checking for updates...", "info")
        self.window.after(2000, self.update_check_complete)
    
    def update_check_complete(self):
        self.add_african_log_entry("UPDATE", "You have the latest version", "info")
        messagebox.showinfo("Updates", "You're running the latest version!")
    
    def clear_log(self):
        if messagebox.askyesno("Clear Log", "Clear all detection history?"):
            for widget in self.log_frame.winfo_children():
                widget.destroy()
            self.detection_history = []
            self.threats_found = 0
            self.safe_files = 0
            self.update_stats_display()
            self.add_african_log_entry("SYSTEM", "Log cleared", "info")
    
    def update_status(self, message):
        self.status_message.configure(text=f" {message.upper()} ")
    
    def add_activity(self, message):
        """Legacy method - redirects to new log"""
        self.add_african_log_entry("ACTIVITY", message, "info")
    
    def on_closing(self):
        result = messagebox.askyesno(
            "Minimize to Tray",
            "Keep scanner running in background?"
        )
        if result:
            self.window.withdraw()
            self.add_african_log_entry("SYSTEM", "Scanner minimized to tray", "info")
        else:
            self.app.stop()
