import magic
import os

class FileTypeDetector:
    def __init__(self):
        self.mime = magic.Magic(mime=True)
        self.desc = magic.Magic()

    def analyze(self, file_path):
        try:
            fname = os.path.basename(file_path)
            fsize = os.path.getsize(file_path)
            with open(file_path, 'rb') as f:
                magic_bytes = f.read(16).hex(' ').upper()
            mime_type = self.mime.from_file(file_path)
            description = self.desc.from_file(file_path)
            true_ext = self._mime_to_extension(mime_type)
            current_ext = os.path.splitext(fname)[1].lower().lstrip('.')
            is_suspicious = (current_ext and current_ext.lower() != true_ext.lower() and
                             current_ext not in ['tmp', 'temp', 'part'])
            return {
                'file_path': file_path,
                'file_name': fname,
                'file_size': self._format_size(fsize),
                'magic_bytes': magic_bytes,
                'mime_type': mime_type,
                'description': description,
                'true_extension': true_ext,
                'current_extension': current_ext or '(none)',
                'is_suspicious': is_suspicious
            }
        except Exception as e:
            return {'file_path': file_path, 'error': str(e), 'is_suspicious': False}

    def _mime_to_extension(self, mime):
        mapping = {
            'application/pdf': 'pdf',
            'application/zip': 'zip',
            'application/x-rar-compressed': 'rar',
            'application/x-7z-compressed': '7z',
            'application/x-msdownload': 'exe',
            'application/x-msdos-program': 'exe',
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

    def _format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"