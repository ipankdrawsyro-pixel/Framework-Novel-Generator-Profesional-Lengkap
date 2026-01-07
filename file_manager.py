# File: file_manager.py
import json
import os
import shutil
from datetime import datetime
from pathlib import Path
import hashlib
from typing import Dict, List, Optional, Tuple

class FileManager:
    def __init__(self, base_path: str = "novels"):
        self.base_path = base_path
        self.current_file = None
        self.backup_path = os.path.join(base_path, "backups")
        os.makedirs(self.backup_path, exist_ok=True)
        
    def generate_file_id(self, title: str) -> str:
        """Generate unique file ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        hash_input = f"{title}_{timestamp}".encode('utf-8')
        return hashlib.md5(hash_input).hexdigest()[:8]
    
    def create_new_novel(self, novel_data: Dict) -> Tuple[bool, str]:
        """Create new novel file"""
        try:
            # Validate required fields
            required_fields = ['title', 'author', 'genre', 'language']
            for field in required_fields:
                if field not in novel_data:
                    return False, f"Missing required field: {field}"
            
            # Generate filename
            file_id = self.generate_file_id(novel_data['title'])
            safe_title = "".join(c for c in novel_data['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_title}_{file_id}.novel"
            filepath = os.path.join(self.base_path, filename)
            
            # Check if file already exists
            if os.path.exists(filepath):
                return False, "File already exists"
            
            # Add metadata
            novel_data['metadata'] = {
                'created': datetime.now().isoformat(),
                'modified': datetime.now().isoformat(),
                'version': '1.0',
                'file_id': file_id,
                'word_count': 0,
                'character_count': 0,
                'chapter_count': 0
            }
            
            # Add empty structure
            novel_data.setdefault('characters', [])
            novel_data.setdefault('chapters', [])
            novel_data.setdefault('world_building', {})
            novel_data.setdefault('settings', {})
            novel_data.setdefault('outline', [])
            
            # Save file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(novel_data, f, indent=2, ensure_ascii=False)
            
            # Create backup
            self.create_backup(filepath)
            
            return True, filepath
            
        except Exception as e:
            return False, f"Error creating file: {str(e)}"
    
    def open_novel(self, filepath: str) -> Tuple[bool, Dict, str]:
        """Open existing novel file"""
        try:
            if not os.path.exists(filepath):
                return False, {}, "File not found"
            
            with open(filepath, 'r', encoding='utf-8') as f:
                novel_data = json.load(f)
            
            # Update metadata
            if 'metadata' in novel_data:
                novel_data['metadata']['last_opened'] = datetime.now().isoformat()
                self.save_file(filepath, novel_data)
            
            self.current_file = filepath
            return True, novel_data, "File opened successfully"
            
        except json.JSONDecodeError:
            return False, {}, "Invalid file format"
        except Exception as e:
            return False, {}, f"Error opening file: {str(e)}"
    
    def save_file(self, filepath: str, novel_data: Dict, auto_backup: bool = True) -> Tuple[bool, str]:
        """Save novel file"""
        try:
            # Update metadata
            if 'metadata' in novel_data:
                novel_data['metadata']['modified'] = datetime.now().isoformat()
                novel_data['metadata']['version'] = str(float(novel_data['metadata'].get('version', '1.0')) + 0.1)
            
            # Save to temporary file first
            temp_file = filepath + '.tmp'
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(novel_data, f, indent=2, ensure_ascii=False)
            
            # Replace original file
            shutil.move(temp_file, filepath)
            
            # Create backup if needed
            if auto_backup:
                self.create_backup(filepath)
            
            return True, "File saved successfully"
            
        except Exception as e:
            return False, f"Error saving file: {str(e)}"
    
    def save_as(self, old_filepath: str, new_title: str) -> Tuple[bool, str]:
        """Save as new file"""
        try:
            # Load old data
            with open(old_filepath, 'r', encoding='utf-8') as f:
                novel_data = json.load(f)
            
            # Update title
            novel_data['title'] = new_title
            
            # Create new file
            success, new_filepath = self.create_new_novel(novel_data)
            
            if success:
                return True, new_filepath
            else:
                return False, "Failed to create new file"
                
        except Exception as e:
            return False, f"Error in save as: {str(e)}"
    
    def delete_file(self, filepath: str, move_to_trash: bool = True) -> Tuple[bool, str]:
        """Delete novel file"""
        try:
            if not os.path.exists(filepath):
                return False, "File not found"
            
            if move_to_trash:
                # Move to archive instead of permanent delete
                archive_path = os.path.join(self.base_path, "archives")
                os.makedirs(archive_path, exist_ok=True)
                
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                archive_file = os.path.join(archive_path, f"{Path(filepath).stem}_{timestamp}.archived")
                shutil.move(filepath, archive_file)
                
                return True, f"File moved to archive: {archive_file}"
            else:
                # Permanent delete
                os.remove(filepath)
                return True, "File permanently deleted"
                
        except Exception as e:
            return False, f"Error deleting file: {str(e)}"
    
    def create_backup(self, filepath: str) -> str:
        """Create backup of file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(
                self.backup_path, 
                f"{Path(filepath).stem}_backup_{timestamp}.bak"
            )
            shutil.copy2(filepath, backup_file)
            
            # Clean old backups (keep only last 10)
            backups = sorted(
                [f for f in os.listdir(self.backup_path) if f.endswith('.bak')],
                key=lambda x: os.path.getmtime(os.path.join(self.backup_path, x))
            )
            
            if len(backups) > 10:
                for old_backup in backups[:-10]:
                    os.remove(os.path.join(self.backup_path, old_backup))
            
            return backup_file
            
        except Exception as e:
            print(f"Backup failed: {e}")
            return ""
    
    def restore_backup(self, backup_file: str, target_file: str) -> bool:
        """Restore from backup"""
        try:
            shutil.copy2(backup_file, target_file)
            return True
        except:
            return False
    
    def get_file_list(self, sort_by: str = "modified") -> List[Dict]:
        """Get list of all novel files"""
        files = []
        
        try:
            for filename in os.listdir(self.base_path):
                if filename.endswith('.novel'):
                    filepath = os.path.join(self.base_path, filename)
                    stat = os.stat(filepath)
                    
                    # Load metadata without loading entire file
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    files.append({
                        'filename': filename,
                        'filepath': filepath,
                        'title': data.get('title', 'Untitled'),
                        'author': data.get('author', 'Unknown'),
                        'genre': data.get('genre', []),
                        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'size': stat.st_size,
                        'metadata': data.get('metadata', {})
                    })
            
            # Sorting
            if sort_by == "modified":
                files.sort(key=lambda x: x['modified'], reverse=True)
            elif sort_by == "created":
                files.sort(key=lambda x: x['created'], reverse=True)
            elif sort_by == "title":
                files.sort(key=lambda x: x['title'].lower())
                
            return files
            
        except Exception as e:
            print(f"Error getting file list: {e}")
            return []
    
    def export_file(self, filepath: str, format: str = "json") -> Tuple[bool, str, str]:
        """Export file to different formats"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            filename = Path(filepath).stem
            export_dir = "exports"
            os.makedirs(export_dir, exist_ok=True)
            
            if format == "json":
                export_path = os.path.join(export_dir, f"{filename}_export.json")
                with open(export_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    
            elif format == "txt":
                export_path = os.path.join(export_dir, f"{filename}_export.txt")
                self._export_to_txt(data, export_path)
                
            elif format == "pdf":
                export_path = os.path.join(export_dir, "pdf", f"{filename}.pdf")
                self._export_to_pdf(data, export_path)
                
            else:
                return False, "", f"Unsupported format: {format}"
            
            return True, export_path, "Export successful"
            
        except Exception as e:
            return False, "", f"Export failed: {str(e)}"
    
    def _export_to_txt(self, data: Dict, export_path: str):
        """Export to plain text format"""
        with open(export_path, 'w', encoding='utf-8') as f:
            f.write(f"Title: {data.get('title', 'Untitled')}\n")
            f.write(f"Author: {data.get('author', 'Unknown')}\n")
            f.write("=" * 50 + "\n\n")
            
            # Export chapters
            for chapter in data.get('chapters', []):
                f.write(f"\nChapter {chapter.get('number', 1)}: {chapter.get('title', '')}\n")
                f.write("-" * 40 + "\n")
                f.write(chapter.get('content', '') + "\n\n")
    
    def _export_to_pdf(self, data: Dict, export_path: str):
        """Export to PDF format"""
        # This would require additional libraries like ReportLab
        # For now, we'll create a placeholder
        pass
    
    def auto_save(self, novel_data: Dict) -> bool:
        """Auto-save feature"""
        if self.current_file and st.session_state.get('auto_save', True):
            success, message = self.save_file(self.current_file, novel_data)
            if success:
                st.session_state.unsaved_changes = False
            return success
        return False
    
    def validate_file_integrity(self, filepath: str) -> Dict:
        """Validate file structure and integrity"""
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {}
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check required fields
            required = ['title', 'author', 'metadata']
            for field in required:
                if field not in data:
                    validation_result['valid'] = False
                    validation_result['errors'].append(f"Missing required field: {field}")
            
            # Check metadata
            if 'metadata' in data:
                meta = data['metadata']
                required_meta = ['created', 'modified', 'version']
                for field in required_meta:
                    if field not in meta:
                        validation_result['warnings'].append(f"Missing metadata: {field}")
            
            # Check chapters structure
            chapters = data.get('chapters', [])
            for i, chapter in enumerate(chapters):
                if 'title' not in chapter:
                    validation_result['warnings'].append(f"Chapter {i+1} missing title")
                if 'content' not in chapter:
                    validation_result['warnings'].append(f"Chapter {i+1} missing content")
            
            # Calculate statistics
            word_count = sum(len(ch.get('content', '').split()) for ch in chapters)
            char_count = sum(len(ch.get('content', '')) for ch in chapters)
            
            validation_result['statistics'] = {
                'total_chapters': len(chapters),
                'total_characters': len(data.get('characters', [])),
                'total_words': word_count,
                'total_chars': char_count
            }
            
        except json.JSONDecodeError:
            validation_result['valid'] = False
            validation_result['errors'].append("Invalid JSON format")
        except Exception as e:
            validation_result['valid'] = False
            validation_result['errors'].append(f"Validation error: {str(e)}")
        
        return validation_result