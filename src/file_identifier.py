import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import magic
import datetime

class FileIdentifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grae-X Magic Eye")
        self.root.geometry("650x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#2b2b2b')  # dark background

        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#2b2b2b', foreground='white', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10, 'bold'), foreground='white', background='#404040')
        style.map('TButton', background=[('active', '#505050')])
        style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'), foreground='#00aaff')
        style.configure('Status.TLabel', background='#1e1e1e', foreground='#cccccc', relief=tk.SUNKEN)

        # Header
        header = ttk.Label(root, text="🔍 Grae-X Magic Eye", style='Header.TLabel')
        header.pack(pady=(20, 5))

        # Subtitle
        subtitle = ttk.Label(root, text="Reveal the true identity of any file", font=('Segoe UI', 10, 'italic'))
        subtitle.pack(pady=(0, 15))

        # File selection frame
        frame = ttk.Frame(root)
        frame.pack(pady=10, padx=20, fill='x')

        self.file_path = tk.StringVar()
        entry = ttk.Entry(frame, textvariable=self.file_path, width=50, font=('Segoe UI', 10))
        entry.pack(side=tk.LEFT, padx=(0, 10), expand=True, fill='x')

        btn_browse = ttk.Button(frame, text="📂 Browse", command=self.browse_file, width=12)
        btn_browse.pack(side=tk.LEFT)

        # Identify button
        btn_identify = ttk.Button(root, text="🚀 Identify File", command=self.identify, width=20)
        btn_identify.pack(pady=15)

        # Results area with scrollbar
        result_frame = ttk.Frame(root)
        result_frame.pack(pady=10, padx=20, fill='both', expand=True)

        self.result_text = tk.Text(result_frame, height=12, wrap=tk.WORD, font=('Consolas', 10),
                                    bg='#1e1e1e', fg='#d4d4d4', insertbackground='white',
                                    relief=tk.FLAT, borderwidth=0)
        self.result_text.pack(side=tk.LEFT, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.result_text.config(yscrollcommand=scrollbar.set)

        # Status bar
        self.status = ttk.Label(root, text="Ready", style='Status.TLabel')
        self.status.pack(side=tk.BOTTOM, fill='x')

    def browse_file(self):
        filename = filedialog.askopenfilename(title="Select a file")
        if filename:
            self.file_path.set(filename)
            self.status.config(text=f"Selected: {os.path.basename(filename)}")

    def identify(self):
        path = self.file_path.get()
        if not path or not os.path.isfile(path):
            self.show_result("⚠️ Please select a valid file.", warning=True)
            return

        self.status.config(text="Analyzing...")
        self.root.update_idletasks()

        try:
            # File info
            fname = os.path.basename(path)
            fsize = os.path.getsize(path)
            mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')

            # Magic bytes
            with open(path, 'rb') as f:
                magic_bytes = f.read(16).hex(' ').upper()

            # Detection
            mime = magic.from_file(path, mime=True)
            description = magic.from_file(path)
            true_ext = self.mime_to_extension(mime)
            current_ext = os.path.splitext(fname)[1].lower().lstrip('.')

            # Build result with colour tags
            result = f"📄 File: {fname}\n"
            result += f"📏 Size: {self.format_size(fsize)}\n"
            result += f"🕒 Modified: {mod_time}\n"
            result += f"🔍 Detected type: {description}\n"
            result += f"📋 MIME type: {mime}\n"
            result += f"🔧 True extension: .{true_ext}\n"
            result += f"🏷️ Current extension: .{current_ext if current_ext else '(none)'}\n"
            result += f"✨ Magic bytes: {magic_bytes}\n"

            # Mismatch handling
            if current_ext and current_ext.lower() != true_ext.lower():
                result += "\n❌ WARNING: File extension does NOT match the actual file type!\n"
                result += "    This could indicate a renamed or malicious file."
                self.show_result(result, warning=True)
                messagebox.showwarning("⚠️ Suspicious File Detected",
                                       f"The file '{fname}' appears to be:\n{description}\n\n"
                                       f"But it has a .{current_ext} extension.\n\n"
                                       "This is a classic sign of a disguised malicious file.")
            elif not current_ext:
                result += "\nℹ️ No file extension provided."
                self.show_result(result)
            else:
                result += "\n✅ Extension matches detected type. File appears safe."
                self.show_result(result, safe=True)

            self.status.config(text="Done")

        except Exception as e:
            self.show_result(f"❌ Error analyzing file:\n{str(e)}", warning=True)
            self.status.config(text="Error")

    def show_result(self, text, warning=False, safe=False):
        """Display result in the text widget with optional colour highlighting."""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)

        # Apply colour tags
        if warning:
            self.result_text.tag_add("warning", "1.0", "end")
            self.result_text.tag_config("warning", foreground="#ff6b6b")  # red
        elif safe:
            self.result_text.tag_add("safe", "1.0", "end")
            self.result_text.tag_config("safe", foreground="#6bff6b")  # green
        else:
            self.result_text.tag_add("info", "1.0", "end")
            self.result_text.tag_config("info", foreground="#d4d4d4")  # default

        self.result_text.config(state=tk.DISABLED)

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def mime_to_extension(self, mime):
        mapping = {
            'application/pdf': 'pdf',
            'application/zip': 'zip',
            'application/x-rar-compressed': 'rar',
            'application/x-7z-compressed': '7z',
            'application/x-msdownload': 'exe',
            'application/x-elf': 'elf',
            'image/jpeg': 'jpg',
            'image/png': 'png',
            'image/gif': 'gif',
            'image/bmp': 'bmp',
            'audio/mpeg': 'mp3',
            'audio/mp4': 'm4a',
            'video/mp4': 'mp4',
            'video/x-msvideo': 'avi',
            'text/plain': 'txt',
            'text/html': 'html',
            'application/json': 'json',
            'application/xml': 'xml',
            'application/msword': 'doc',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
        }
        return mapping.get(mime, 'bin')

if __name__ == "__main__":
    root = tk.Tk()
    app = FileIdentifierApp(root)
    root.mainloop()