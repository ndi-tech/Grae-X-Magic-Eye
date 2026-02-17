from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from detector import FileTypeDetector
from config import Config
import os

class DownloadHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        self.detector = FileTypeDetector()
        print("✅ DownloadHandler initialized")

    def on_created(self, event):
        print(f"📢 EVENT: File created - {event.src_path}")
        if not event.is_directory:
            self._process_file(event.src_path)

    def on_modified(self, event):
        print(f"📢 EVENT: File modified - {event.src_path}")
        if not event.is_directory:
            print("⏱️ Waiting 1 second for file to complete...")
            time.sleep(1)
            self._process_file(event.src_path)

    def _process_file(self, file_path):
        print(f"\n🔍 PROCESSING: {file_path}")
        
        # Check if it's a temp file
        if any(file_path.endswith(ext) for ext in Config.IGNORE_EXTENSIONS):
            print(f"⏭️ Ignoring temp file (extension in ignore list)")
            return
        
        print(f"📁 Analyzing file...")
        file_info = self.detector.analyze(file_path)
        print(f"📊 Analysis result: {file_info}")
        
        if file_info.get('is_suspicious'):
            print(f"⚠️⚠️⚠️ SUSPICIOUS FILE DETECTED: {file_info['file_name']}")
            print(f"   True type: .{file_info['true_extension']}")
            print(f"   Disguised as: .{file_info['current_extension']}")
            print(f"   Description: {file_info['description']}")
            print(f"📢 Calling callback to show popup...")
            if self.callback:
                self.callback(file_info)
                print("✅ Callback executed")
            else:
                print("❌ No callback registered!")
        elif 'error' in file_info:
            print(f"❌ Error analyzing file: {file_info['error']}")
        else:
            print(f"✅ Safe file: {file_info['file_name']}")
        print("-" * 50)

class FileMonitor:
    def __init__(self, callback):
        print("🔧 Initializing FileMonitor...")
        self.observer = Observer()
        self.handler = DownloadHandler(callback)

    def start(self):
        print("🚀 Starting file monitor...")
        for folder in Config.MONITOR_FOLDERS:
            if os.path.exists(folder):
                self.observer.schedule(self.handler, folder, recursive=False)
                print(f"👀 Monitoring: {folder}")
            else:
                print(f"⚠️ Folder not found: {folder}")

        self.observer.start()
        print("✅ File monitor is now running and watching for changes!\n")
        print("=" * 50)
        print("🛡️  Grae-X Magic Eye Shield is ACTIVE")
        print("=" * 50 + "\n")

    def stop(self):
        print("🛑 Stopping file monitor...")
        self.observer.stop()
        self.observer.join()
        print("✅ File monitor stopped")