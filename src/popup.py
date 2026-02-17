import customtkinter as ctk
import tkinter as tk
import os
import sys
from PIL import Image

class PopupManager:
    def __init__(self, root):
        self.root = root
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Load your logo
        self.logo_image = self.load_logo()
        
    def load_logo(self):
        """Load your company logo for display"""
        try:
            # Look for logo.png first (better for display)
            logo_paths = [
                "logo.png",
                "logo.ico",
                os.path.join(os.path.dirname(__file__), "..", "logo.png"),
                os.path.join(os.path.dirname(__file__), "..", "logo.ico"),
                os.path.join(os.path.dirname(sys.executable), "logo.png"),
            ]
            
            for logo_path in logo_paths:
                if os.path.exists(logo_path):
                    print(f"✅ Logo loaded from: {logo_path}")
                    # Create CTkImage for customtkinter
                    return ctk.CTkImage(
                        light_image=Image.open(logo_path),
                        dark_image=Image.open(logo_path),
                        size=(60, 60)  # Adjust size as needed
                    )
        except Exception as e:
            print(f"⚠️ Could not load logo: {e}")
        return None
        
    def set_window_icon(self, popup_window):
        """Set the window icon (small icon in title bar)"""
        try:
            icon_paths = [
                "logo.ico",
                "icon.ico",
                os.path.join(os.path.dirname(__file__), "..", "logo.ico"),
            ]
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    popup_window.iconbitmap(icon_path)
                    break
        except:
            pass

    def show_alert(self, info):
        if not info.get('is_suspicious'):
            return
            
        # Create popup window
        win = ctk.CTkToplevel(self.root)
        win.title("⚠️ Grae-X Magic Eye Alert")
        win.geometry("600x500")  # Larger to accommodate logo
        win.attributes('-topmost', True)
        win.after(10000, win.destroy)
        
        # Set window icon (small icon in title bar)
        self.set_window_icon(win)

        # Center on screen
        win.update_idletasks()
        x = (win.winfo_screenwidth() - 600) // 2
        y = (win.winfo_screenheight() - 500) // 2
        win.geometry(f'+{x}+{y}')

        # Main container
        main_container = ctk.CTkFrame(win, fg_color="#0a0a1a", corner_radius=15)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Header with YOUR LOGO prominently displayed
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent", height=100)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        # Display your logo prominently
        if self.logo_image:
            # Show your actual logo
            logo_label = ctk.CTkLabel(
                header_frame, 
                image=self.logo_image, 
                text=""
            )
            logo_label.pack(side="left", padx=(0, 20))
        else:
            # Fallback if logo not found
            ctk.CTkLabel(
                header_frame, 
                text="🛡️", 
                font=ctk.CTkFont(size=60)
            ).pack(side="left", padx=(0, 20))

        # Company name and warning
        company_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        company_frame.pack(side="left", fill="both", expand=True)

        # Your company name
        ctk.CTkLabel(
            company_frame,
            text="GRAE-X LABS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#00aaff"
        ).pack(anchor="w")

        # Warning title
        warning_title = ctk.CTkFrame(company_frame, fg_color="transparent")
        warning_title.pack(anchor="w", pady=(5, 0))

        ctk.CTkLabel(
            warning_title,
            text="⚠️",
            font=ctk.CTkFont(size=24),
            text_color="#FF4444"
        ).pack(side="left", padx=(0, 5))

        ctk.CTkLabel(
            warning_title,
            text="SUSPICIOUS FILE DETECTED",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FF8888"
        ).pack(side="left")

        # Decorative line with your brand color
        border_frame = ctk.CTkFrame(main_container, fg_color="#00aaff", height=2)
        border_frame.pack(fill="x", padx=20, pady=5)

        # File details card
        card = ctk.CTkFrame(main_container, fg_color="#1a1a2e", 
                           border_width=2, border_color="#00aaff",
                           corner_radius=10)
        card.pack(fill="both", expand=True, padx=20, pady=10)

        # File name with highlight
        name_frame = ctk.CTkFrame(card, fg_color="#2d2d4d", corner_radius=8)
        name_frame.pack(fill="x", padx=15, pady=(15, 10))

        file_name = info['file_name']
        if len(file_name) > 40:
            file_name = file_name[:37] + "..."

        ctk.CTkLabel(
            name_frame,
            text=file_name,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#88ccff"
        ).pack(pady=8, padx=10)

        # Detection details grid
        details = ctk.CTkFrame(card, fg_color="transparent")
        details.pack(fill="x", padx=20, pady=5)

        # Detected type
        detected_frame = ctk.CTkFrame(details, fg_color="transparent")
        detected_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(
            detected_frame,
            text="🔍 DETECTED:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#ffaa00",
            width=100
        ).pack(side="left")
        ctk.CTkLabel(
            detected_frame,
            text=info['description'][:50] + ("..." if len(info['description']) > 50 else ""),
            font=ctk.CTkFont(size=11),
            text_color="#ffffff"
        ).pack(side="left", padx=(10, 0))

        # Disguised as
        disguised_frame = ctk.CTkFrame(details, fg_color="transparent")
        disguised_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(
            disguised_frame,
            text="🎭 DISGUISED AS:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#ff4444",
            width=100
        ).pack(side="left")
        ctk.CTkLabel(
            disguised_frame,
            text=f".{info['current_extension']}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ff8888"
        ).pack(side="left", padx=(10, 0))

        # True type
        true_frame = ctk.CTkFrame(details, fg_color="transparent")
        true_frame.pack(fill="x", pady=2)
        ctk.CTkLabel(
            true_frame,
            text="✅ TRUE TYPE:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#88cc88",
            width=100
        ).pack(side="left")
        ctk.CTkLabel(
            true_frame,
            text=f".{info['true_extension']}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#88ff88"
        ).pack(side="left", padx=(10, 0))

        # Separator
        separator = ctk.CTkFrame(card, fg_color="#333333", height=1)
        separator.pack(fill="x", padx=20, pady=10)

        # Technical details
        tech = ctk.CTkFrame(card, fg_color="transparent")
        tech.pack(fill="x", padx=20, pady=(0, 10))

        tech_grid = ctk.CTkFrame(tech, fg_color="#23233a", corner_radius=6)
        tech_grid.pack(fill="x")

        # File Size
        size_row = ctk.CTkFrame(tech_grid, fg_color="transparent")
        size_row.pack(fill="x", pady=5, padx=10)
        ctk.CTkLabel(
            size_row,
            text="📏 Size:",
            font=ctk.CTkFont(size=10),
            text_color="#88aaff",
            width=70
        ).pack(side="left")
        ctk.CTkLabel(
            size_row,
            text=info['file_size'],
            font=ctk.CTkFont(size=10, family="Consolas"),
            text_color="#aaccff"
        ).pack(side="left")

        # Magic Bytes
        magic_row = ctk.CTkFrame(tech_grid, fg_color="transparent")
        magic_row.pack(fill="x", pady=(0, 5), padx=10)
        ctk.CTkLabel(
            magic_row,
            text="✨ Magic:",
            font=ctk.CTkFont(size=10),
            text_color="#88aaff",
            width=70
        ).pack(side="left")

        magic_display = info['magic_bytes']
        if len(magic_display) > 30:
            magic_display = magic_display[:27] + "..."

        ctk.CTkLabel(
            magic_row,
            text=magic_display,
            font=ctk.CTkFont(size=9, family="Consolas"),
            text_color="#aaccff"
        ).pack(side="left")

        # Action buttons
        action_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        action_frame.pack(fill="x", padx=20, pady=(5, 15))

        # Quarantine button
        quarantine_btn = ctk.CTkButton(
            action_frame,
            text="🔒 Quarantine File",
            command=lambda: self.quarantine_file(info),
            fg_color="#8c2d2d",
            hover_color="#9c3d3d",
            width=140,
            height=32
        )
        quarantine_btn.pack(side="left", padx=(0, 10))

        # Ignore button
        ignore_btn = ctk.CTkButton(
            action_frame,
            text="⏭️ Ignore",
            command=lambda: self.ignore_file(info, win),
            fg_color="#4d4d4d",
            hover_color="#5d5d5d",
            width=100,
            height=32
        )
        ignore_btn.pack(side="left")

        # Close button
        close_btn = ctk.CTkButton(
            action_frame,
            text="✕ Close",
            command=win.destroy,
            fg_color="#333333",
            hover_color="#444444",
            width=80,
            height=32
        )
        close_btn.pack(side="right")

        # Footer with your branding
        footer_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        footer_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Warning text
        footer = ctk.CTkLabel(
            footer_frame,
            text="⚠️ This file may be malicious - DO NOT OPEN if unsure",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#ff8888",
            fg_color="#330000",
            corner_radius=8,
            height=30
        )
        footer.pack(fill="x", pady=(0, 5))

        # Company signature
        ctk.CTkLabel(
            footer_frame,
            text="Grae-X Labs • Security Division",
            font=ctk.CTkFont(size=9),
            text_color="#666666"
        ).pack()

        # Countdown timer
        self.countdown = 10
        self._update_countdown(footer, win)

    def _update_countdown(self, footer, win):
        """Update the countdown on the footer"""
        if self.countdown > 0:
            footer.configure(text=f"⚠️ Auto-closing in {self.countdown}s - DO NOT OPEN if unsure")
            self.countdown -= 1
            win.after(1000, lambda: self._update_countdown(footer, win))

    def quarantine_file(self, info):
        """Placeholder for quarantine functionality"""
        import tkinter.messagebox as mb
        result = mb.askyesno(
            "Quarantine File",
            f"Move '{info['file_name']}' to quarantine?\n\n"
            "The file will be moved to a secure folder and cannot be executed."
        )
        if result:
            mb.showinfo(
                "Quarantine",
                f"File has been quarantined.\n\n"
                f"This is a simulation - in the full version, the file would be moved."
            )

    def ignore_file(self, info, win):
        """Ignore this detection and close popup"""
        import tkinter.messagebox as mb
        mb.showinfo(
            "Ignored",
            f"Alert for '{info['file_name']}' has been ignored.\n"
            f"You will not be notified again for this file."
        )
        win.destroy()