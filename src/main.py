import sys
import os
import threading
import tkinter as tk
from tkinter import messagebox
from config import Config
from monitor import FileMonitor
from popup import PopupManager
from dashboard import Dashboard  # Import the dashboard

class MagicEyeApp:
    def __init__(self):
        self.config = Config
        self.monitor = FileMonitor(self.on_suspicious_file)
        self.running = True
        self.root = None
        self.popup_manager = None
        self.dashboard = None  # Add dashboard reference

    def on_suspicious_file(self, file_info):
        print(f"🎯 Suspicious file detected: {file_info.get('file_name', 'unknown')}")
        if self.root:
            self.root.after(0, lambda: self.popup_manager.show_alert(file_info))
            # Also add to dashboard log
            if self.dashboard:
                self.dashboard.add_detection_log(file_info)
                self.dashboard.add_activity(f"⚠️ Threat detected: {file_info.get('file_name')}")

    def start(self):
        print("🚀 Starting Grae-X Magic Eye Shield...")
        
        # Create hidden root for GUI operations
        self.root = tk.Tk()
        self.root.withdraw()
        self.popup_manager = PopupManager(self.root)
        
        # Create and show dashboard
        self.dashboard = Dashboard(self)
        
        # Start file monitor in background
        monitor_thread = threading.Thread(target=self.monitor.start, daemon=True)
        monitor_thread.start()
        print("✅ File monitor started")
        
        print("\n" + "="*50)
        print("🛡️  Grae-X Magic Eye Shield is RUNNING")
        print("="*50)
        print("📁 Monitoring folders:")
        for folder in self.config.MONITOR_FOLDERS:
            print(f"   • {folder}")
        print("\n📊 Dashboard is visible")
        print("="*50 + "\n")
        
        # Keep the application running
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        print("\n🛑 Shutting down...")
        self.monitor.stop()
        if self.root:
            self.root.quit()
        print("👋 Goodbye! Stay safe.")
        sys.exit(0)

if __name__ == "__main__":
    app = MagicEyeApp()
    app.start()