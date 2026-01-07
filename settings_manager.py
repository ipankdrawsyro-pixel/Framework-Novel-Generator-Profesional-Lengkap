# File: settings_manager.py
import streamlit as st
import json
import os

class SettingsManager:
    def __init__(self):
        self.settings_file = "settings/user_preferences.json"
        self.default_settings = {
            'appearance': {
                'theme': 'light',
                'font_size': 14,
                'font_family': 'Arial',
                'density': 'normal'
            },
            'writing': {
                'auto_save': True,
                'auto_save_interval': 30,
                'spell_check': True,
                'grammar_check': False,
                'word_count_goal': 1000,
                'daily_word_goal': 1000
            },
            'export': {
                'default_format': 'pdf',
                'include_metadata': True,
                'page_size': 'A4',
                'font_size_export': 12
            },
            'ai_assistance': {
                'enabled': True,
                'model': 'gpt-3.5-turbo',
                'temperature': 0.7,
                'max_tokens': 500
            },
            'backup': {
                'auto_backup': True,
                'backup_interval': 3600,
                'keep_backups': 10,
                'cloud_backup': False
            }
        }
    
    def load_settings(self) -> Dict:
        """Load user settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.default_settings
        except:
            return self.default_settings
    
    def save_settings(self, settings: Dict):
        """Save user settings to file"""
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2)
            return True
        except Exception as e:
            st.error(f"Error saving settings: {e}")
            return False
    
    def render_settings(self):
        """Render settings interface"""
        st.header("⚙️ Settings")
        
        # Load current settings
        settings = self.load_settings()
        
        # Tabs for different setting categories
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Appearance", "Writing", "Export", "AI Assistance", "Backup"
        ])
        
        with tab1:
            settings = self.render_appearance_settings(settings)
        
        with tab2:
            settings = self.render_writing_settings(settings)
        
        with tab3:
            settings = self.render_export_settings(settings)
        
        with tab4:
            settings = self.render_ai_settings(settings)
        
        with tab5:
            settings = self.render_backup_settings(settings)
        
        # Save button
        st.divider()
        
        col_save1, col_save2 = st.columns(2)
        with col_save1:
            if st.button("💾 Save Settings", use_container_width=True, type="primary"):
                if self.save_settings(settings):
                    st.success("Settings saved successfully!")
                else:
                    st.error("Failed to save settings")
        
        with col_save2:
            if st.button("🔄 Reset to Defaults", use_container_width=True):
                if self.save_settings(self.default_settings):
                    st.success("Settings reset to defaults!")
                    st.rerun()
    
    def render_appearance_settings(self, settings: Dict) -> Dict:
        """Render appearance settings"""
        st.subheader("Appearance Settings")
        
        # Theme
        theme = st.selectbox(
            "Theme",
            ["light", "dark", "system"],
            index=["light", "dark", "system"].index(
                settings.get('appearance', {}).get('theme', 'light')
            )
        )
        
        # Font size
        font_size = st.slider(
            "Font Size",
            min_value=10,
            max_value=24,
            value=settings.get('appearance', {}).get('font_size', 14)
        )
        
        # Font family
        font_family = st.selectbox(
            "Font Family",
            ["Arial", "Helvetica", "Times New Roman", "Courier New", "Georgia", "Verdana"],
            index=["Arial", "Helvetica", "Times New Roman", "Courier New", "Georgia", "Verdana"].index(
                settings.get('appearance', {}).get('font_family', 'Arial')
            )
        )
        
        # Density
        density = st.selectbox(
            "UI Density",
            ["compact", "normal", "comfortable"],
            index=["compact", "normal", "comfortable"].index(
                settings.get('appearance', {}).get('density', 'normal')
            )
        )
        
        # Update settings
        settings['appearance'] = {
            'theme': theme,
            'font_size': font_size,
            'font_family': font_family,
            'density': density
        }
        
        return settings
    
    def render_writing_settings(self, settings: Dict) -> Dict:
        """Render writing settings"""
        st.subheader("Writing Settings")
        
        # Auto-save
        auto_save = st.toggle(
            "Enable Auto-save",
            value=settings.get('writing', {}).get('auto_save', True)
        )
        
        if auto_save:
            auto_save_interval = st.slider(
                "Auto-save Interval (seconds)",
                min_value=10,
                max_value=300,
                value=settings.get('writing', {}).get('auto_save_interval', 30)
            )
        else:
            auto_save_interval = 30
        
        # Spell check
        spell_check = st.toggle(
            "Enable Spell Check",
            value=settings.get('writing', {}).get('spell_check', True)
        )
        
        # Grammar check
        grammar_check = st.toggle(
            "Enable Grammar Check",
            value=settings.get('writing', {}).get('grammar_check', False)
        )
        
        # Writing goals
        st.write("**Writing Goals**")
        col_goal1, col_goal2 = st.columns(2)
        
        with col_goal1:
            word_count_goal = st.number_input(
                "Chapter Word Goal",
                min_value=500,
                max_value=10000,
                value=settings.get('writing', {}).get('word_count_goal', 2000)
            )
        
        with col_goal2:
            daily_word_goal = st.number_input(
                "Daily Word Goal",
                min_value=100,
                max_value=5000,
                value=settings.get('writing', {}).get('daily_word_goal', 1000)
            )
        
        # Update settings
        settings['writing'] = {
            'auto_save': auto_save,
            'auto_save_interval': auto_save_interval,
            'spell_check': spell_check,
            'grammar_check': grammar_check,
            'word_count_goal': word_count_goal,
            'daily_word_goal': daily_word_goal
        }
        
        return settings
    
    def render_export_settings(self, settings: Dict) -> Dict:
        """Render export settings"""
        st.subheader("Export Settings")
        
        # Default format
        default_format = st.selectbox(
            "Default Export Format",
            ["pdf", "epub", "docx", "txt", "json"],
            index=["pdf", "epub", "docx", "txt", "json"].index(
                settings.get('export', {}).get('default_format', 'pdf')
            )
        )
        
        # Include metadata
        include_metadata = st.toggle(
            "Include Metadata",
            value=settings.get('export', {}).get('include_metadata', True)
        )
        
        # Page size
        page_size = st.selectbox(
            "Page Size",
            ["A4", "Letter", "A5", "B5"],
            index=["A4", "Letter", "A5", "B5"].index(
                settings.get('export', {}).get('page_size', 'A4')
            )
        )
        
        # Font size for export
        font_size_export = st.slider(
            "Export Font Size",
            min_value=8,
            max_value=18,
            value=settings.get('export', {}).get('font_size_export', 12)
        )
        
        # Update settings
        settings['export'] = {
            'default_format': default_format,
            'include_metadata': include_metadata,
            'page_size': page_size,
            'font_size_export': font_size_export
        }
        
        return settings
    
    def render_ai_settings(self, settings: Dict) -> Dict:
        """Render AI assistance settings"""
        st.subheader("AI Assistance Settings")
        
        # Enable AI
        enabled = st.toggle(
            "Enable AI Assistance",
            value=settings.get('ai_assistance', {}).get('enabled', True)
        )
        
        if enabled:
            # Model selection
            model = st.selectbox(
                "AI Model",
                ["gpt-3.5-turbo", "gpt-4", "claude-2", "bard", "local"],
                index=["gpt-3.5-turbo", "gpt-4", "claude-2", "bard", "local"].index(
                    settings.get('ai_assistance', {}).get('model', 'gpt-3.5-turbo')
                )
            )
            
            # Temperature
            temperature = st.slider(
                "Creativity (Temperature)",
                min_value=0.0,
                max_value=1.0,
                value=settings.get('ai_assistance', {}).get('temperature', 0.7),
                help="Lower = more focused, Higher = more creative"
            )
            
            # Max tokens
            max_tokens = st.slider(
                "Max Response Length (tokens)",
                min_value=100,
                max_value=2000,
                value=settings.get('ai_assistance', {}).get('max_tokens', 500)
            )
            
            # AI features
            st.write("**AI Features**")
            col_ai1, col_ai2 = st.columns(2)
            
            with col_ai1:
                suggest_plots = st.toggle("Suggest Plots", value=True)
                develop_characters = st.toggle("Develop Characters", value=True)
            
            with col_ai2:
                generate_dialogue = st.toggle("Generate Dialogue", value=True)
                proofread = st.toggle("Proofread Text", value=True)
        else:
            model = settings.get('ai_assistance', {}).get('model', 'gpt-3.5-turbo')
            temperature = settings.get('ai_assistance', {}).get('temperature', 0.7)
            max_tokens = settings.get('ai_assistance', {}).get('max_tokens', 500)
            suggest_plots = False
            develop_characters = False
            generate_dialogue = False
            proofread = False
        
        # Update settings
        settings['ai_assistance'] = {
            'enabled': enabled,
            'model': model,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'features': {
                'suggest_plots': suggest_plots,
                'develop_characters': develop_characters,
                'generate_dialogue': generate_dialogue,
                'proofread': proofread
            }
        }
        
        return settings
    
    def render_backup_settings(self, settings: Dict) -> Dict:
        """Render backup settings"""
        st.subheader("Backup Settings")
        
        # Auto backup
        auto_backup = st.toggle(
            "Enable Auto Backup",
            value=settings.get('backup', {}).get('auto_backup', True)
        )
        
        if auto_backup:
            # Backup interval
            backup_interval = st.slider(
                "Backup Interval (seconds)",
                min_value=300,
                max_value=86400,
                value=settings.get('backup', {}).get('backup_interval', 3600),
                help="How often to create automatic backups"
            )
            
            # Number of backups to keep
            keep_backups = st.slider(
                "Backups to Keep",
                min_value=1,
                max_value=50,
                value=settings.get('backup', {}).get('keep_backups', 10),
                help="Maximum number of backup files to keep"
            )
            
            # Cloud backup
            cloud_backup = st.toggle(
                "Enable Cloud Backup",
                value=settings.get('backup', {}).get('cloud_backup', False),
                help="Backup to cloud storage (requires configuration)"
            )
        else:
            backup_interval = settings.get('backup', {}).get('backup_interval', 3600)
            keep_backups = settings.get('backup', {}).get('keep_backups', 10)
            cloud_backup = False
        
        # Manual backup
        st.write("**Manual Backup**")
        
        col_backup1, col_backup2 = st.columns(2)
        with col_backup1:
            if st.button("Create Backup Now", use_container_width=True):
                # Create manual backup
                st.info("Backup feature coming soon!")
        
        with col_backup2:
            if st.button("Restore from Backup", use_container_width=True):
                # Restore from backup
                st.info("Restore feature coming soon!")
        
        # Update settings
        settings['backup'] = {
            'auto_backup': auto_backup,
            'backup_interval': backup_interval,
            'keep_backups': keep_backups,
            'cloud_backup': cloud_backup
        }
        
        return settings