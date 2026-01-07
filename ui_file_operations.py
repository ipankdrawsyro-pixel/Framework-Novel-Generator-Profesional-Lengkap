# File: ui_file_operations.py
import streamlit as st
from file_manager import FileManager

class FileOperationsUI:
    def __init__(self):
        self.file_manager = FileManager()
    
    def show_file_operations_sidebar(self):
        """Show file operations in sidebar"""
        with st.sidebar:
            st.header("📁 File Operations")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📄 New", use_container_width=True):
                    st.session_state.show_new_file_dialog = True
            with col2:
                if st.button("📂 Open", use_container_width=True):
                    st.session_state.show_open_file_dialog = True
            
            st.divider()
            
            # Current file info
            if st.session_state.current_file_path:
                st.subheader("Current File")
                st.caption(f"**{st.session_state.novel_data.get('title', 'Untitled')}**")
                
                # Save buttons
                col_save1, col_save2 = st.columns(2)
                with col_save1:
                    if st.button("💾 Save", use_container_width=True):
                        self.save_current_file()
                with col_save2:
                    if st.button("💾 Save As", use_container_width=True):
                        st.session_state.show_save_as_dialog = True
                
                # Export options
                st.divider()
                st.subheader("Export")
                export_format = st.selectbox(
                    "Format",
                    ["JSON", "TXT", "PDF"],
                    key="export_format"
                )
                if st.button("📤 Export", use_container_width=True):
                    self.export_current_file(export_format.lower())
            
            st.divider()
            
            # File list
            st.subheader("Recent Files")
            self.show_recent_files_list()
    
    def show_new_file_dialog(self):
        """Dialog for creating new file"""
        with st.form("new_file_form"):
            st.subheader("Create New Novel")
            
            title = st.text_input("Title*", placeholder="Enter novel title")
            author = st.text_input("Author*", placeholder="Your name")
            
            col1, col2 = st.columns(2)
            with col1:
                genre = st.multiselect(
                    "Genre*",
                    ["Romance", "Fantasy", "Science Fiction", "Mystery", "Thriller", 
                     "Horror", "Historical", "Adventure", "Literary", "Young Adult"]
                )
            with col2:
                language = st.selectbox(
                    "Language*",
                    ["Indonesian", "English", "Other"]
                )
            
            description = st.text_area("Description", height=100)
            
            col_submit1, col_submit2 = st.columns(2)
            with col_submit1:
                submit = st.form_submit_button("Create", use_container_width=True)
            with col_submit2:
                cancel = st.form_submit_button("Cancel", use_container_width=True)
            
            if cancel:
                st.session_state.show_new_file_dialog = False
                st.rerun()
            
            if submit:
                if not title or not author or not genre:
                    st.error("Please fill all required fields (*)")
                else:
                    novel_data = {
                        'title': title,
                        'author': author,
                        'genre': genre,
                        'language': language,
                        'description': description,
                        'status': 'draft',
                        'created_date': datetime.now().isoformat()
                    }
                    
                    success, result = self.file_manager.create_new_novel(novel_data)
                    
                    if success:
                        st.success(f"Novel '{title}' created successfully!")
                        st.session_state.show_new_file_dialog = False
                        
                        # Open the new file
                        self.open_file(result)
                        st.rerun()
                    else:
                        st.error(f"Error: {result}")
    
    def show_open_file_dialog(self):
        """Dialog for opening existing file"""
        st.subheader("Open Existing Novel")
        
        # Search bar
        search = st.text_input("Search files...", key="file_search")
        
        # Get file list
        files = self.file_manager.get_file_list()
        
        if search:
            files = [f for f in files if search.lower() in f['title'].lower()]
        
        if not files:
            st.info("No novel files found. Create a new one!")
            return
        
        # File list
        for file_info in files:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**{file_info['title']}**")
                    st.caption(f"Author: {file_info['author']}")
                    st.caption(f"Genre: {', '.join(file_info['genre'])}")
                
                with col2:
                    if st.button("📖", key=f"open_{file_info['filename']}", help="Open"):
                        self.open_file(file_info['filepath'])
                        st.session_state.show_open_file_dialog = False
                        st.rerun()
                
                with col3:
                    if st.button("🗑️", key=f"delete_{file_info['filename']}", help="Delete"):
                        st.session_state.file_to_delete = file_info['filepath']
                        st.session_state.show_delete_confirm = True
        
        # Delete confirmation dialog
        if st.session_state.get('show_delete_confirm'):
            self.show_delete_confirmation()
    
    def show_delete_confirmation(self):
        """Show delete confirmation dialog"""
        filepath = st.session_state.file_to_delete
        
        with st.expander("⚠️ Confirm Deletion", expanded=True):
            st.warning("Are you sure you want to delete this file?")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Yes, Delete", type="primary"):
                    success, message = self.file_manager.delete_file(filepath)
                    if success:
                        st.success("File deleted")
                        # Refresh file list
                        del st.session_state.file_to_delete
                        st.session_state.show_delete_confirm = False
                        st.rerun()
                    else:
                        st.error(f"Error: {message}")
            with col2:
                if st.button("Archive Instead"):
                    success, message = self.file_manager.delete_file(filepath, move_to_trash=True)
                    if success:
                        st.success("File archived")
                        del st.session_state.file_to_delete
                        st.session_state.show_delete_confirm = False
                        st.rerun()
            with col3:
                if st.button("Cancel"):
                    del st.session_state.file_to_delete
                    st.session_state.show_delete_confirm = False
                    st.rerun()
    
    def show_save_as_dialog(self):
        """Save As dialog"""
        st.subheader("Save As New File")
        
        current_title = st.session_state.novel_data.get('title', '')
        new_title = st.text_input("New Title", value=f"{current_title} - Copy")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save", type="primary"):
                if new_title and new_title != current_title:
                    success, result = self.file_manager.save_as(
                        st.session_state.current_file_path,
                        new_title
                    )
                    if success:
                        st.success("Saved as new file!")
                        self.open_file(result)
                        st.session_state.show_save_as_dialog = False
                        st.rerun()
                    else:
                        st.error(f"Error: {result}")
        
        with col2:
            if st.button("Cancel"):
                st.session_state.show_save_as_dialog = False
                st.rerun()
    
    def save_current_file(self):
        """Save current file"""
        if st.session_state.current_file_path and st.session_state.novel_data:
            success, message = self.file_manager.save_file(
                st.session_state.current_file_path,
                st.session_state.novel_data
            )
            if success:
                st.session_state.unsaved_changes = False
                st.success("File saved!")
            else:
                st.error(f"Save failed: {message}")
    
    def open_file(self, filepath: str):
        """Open a file"""
        success, data, message = self.file_manager.open_novel(filepath)
        
        if success:
            st.session_state.current_file_path = filepath
            st.session_state.novel_data = data
            st.session_state.unsaved_changes = False
            st.success(f"Opened: {data.get('title', 'Untitled')}")
        else:
            st.error(f"Failed to open file: {message}")
    
    def export_current_file(self, format: str):
        """Export current file"""
        if st.session_state.current_file_path:
            success, export_path, message = self.file_manager.export_file(
                st.session_state.current_file_path,
                format
            )
            if success:
                st.success(f"Exported to: {export_path}")
                
                # Offer download
                with open(export_path, 'rb') as f:
                    st.download_button(
                        label=f"Download {format.upper()}",
                        data=f,
                        file_name=f"{st.session_state.novel_data.get('title', 'novel')}.{format}",
                        mime="application/json" if format == "json" else "text/plain"
                    )
            else:
                st.error(f"Export failed: {message}")
    
    def show_recent_files_list(self):
        """Show list of recent files in sidebar"""
        files = self.file_manager.get_file_list(sort_by="modified")
        
        for i, file_info in enumerate(files[:5]):  # Show only 5 most recent
            modified_time = datetime.fromisoformat(file_info['modified'])
            time_ago = self._time_ago(modified_time)
            
            if st.button(
                f"{file_info['title'][:20]}...",
                key=f"recent_{i}",
                help=f"Modified {time_ago}",
                use_container_width=True
            ):
                self.open_file(file_info['filepath'])
                st.rerun()
    
    def _time_ago(self, dt: datetime) -> str:
        """Calculate time ago string"""
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 365:
            return f"{diff.days // 365} years ago"
        elif diff.days > 30:
            return f"{diff.days // 30} months ago"
        elif diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} hours ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} minutes ago"
        else:
            return "just now"
    
    def check_unsaved_changes(self):
        """Check for unsaved changes before closing"""
        if st.session_state.unsaved_changes:
            st.warning("⚠️ You have unsaved changes!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("💾 Save Now"):
                    self.save_current_file()
            with col2:
                if st.button("❌ Discard"):
                    st.session_state.unsaved_changes = False
                    st.rerun()
            with col3:
                if st.button("↩️ Cancel"):
                    pass