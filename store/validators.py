from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_size_kb=500

    if file.size > max_size_kb * 1024:
        raise ValidationError(f'file can not be longe{max_size_kb}KB!')
    
