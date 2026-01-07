# File: folder_structure.py
import os

def create_folder_structure():
    """Create necessary folders for the application"""
    folders = [
        'novels',
        'novels/backups',
        'novels/archives',
        'characters',
        'characters/images',
        'characters/profiles',
        'settings',
        'exports',
        'exports/pdf',
        'exports/epub',
        'templates',
        'templates/characters',
        'templates/worlds',
        'logs',
        'temp'
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    
    # Create default files
    default_files = {
        'settings/app_config.json': '{}',
        'settings/user_preferences.json': '{}',
        'templates/characters/default_template.json': '{}',
        'templates/worlds/fantasy_template.json': '{}'
    }
    
    for file_path, content in default_files.items():
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    return True