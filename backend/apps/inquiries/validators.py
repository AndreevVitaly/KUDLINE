from pathlib import Path
from django.core.exceptions import ValidationError

MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".dwg", ".dxf", ".doc", ".docx", ".jpg", ".jpeg", ".png", ".zip", ".rar", ".7z"}

def validate_attachment(file):
    if file.size > MAX_FILE_SIZE:
        raise ValidationError("Максимальный размер файла — 10 МБ.")
    if Path(file.name).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValidationError("Недопустимый тип файла.")

