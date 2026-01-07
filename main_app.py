# File: main_app.py
import streamlit as st
import time
from file_manager import FileManager
from ui_file_operations import FileOperationsUI
from character_manager import CharacterManager
from chapter_manager import ChapterManager
from settings_manager import SettingsManager

# Page configuration
st.set_page_config(
    page_title="NovelCraft Pro",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4A5568;
        margin-bottom: 1rem;
    }
    .novel-card {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4299E1;
        background-color: #f8fafc;
        margin-bottom: 1rem;
    }
    .unsaved-warning {
        background-color: #FEF3C7;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 5px solid #F59E0B;
    }
</style>
""", unsafe_allow_html=True)

class NovelCraftApp:
    def __init__(self):
        self.file_ops = FileOperationsUI()
        self.char_manager = CharacterManager()
        self.chapter_manager = ChapterManager()
        self.settings_manager = SettingsManager()
        
        # Initialize app state
        self.init_app_state()
    
    def init_app_state(self):
        """Initialize application state"""
        if 'app_initialized' not in st.session_state:
            st.session_state.app_initialized = True
            
            # Create folder structure
            create_folder_structure()
            
            # Load user settings
            self.settings_manager.load_settings()
    
    def render_header(self):
        """Render application header"""
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown('<h1 class="main-header">📚 NovelCraft Pro</h1>', unsafe_allow_html=True)
        
        with col2:
            if st.session_state.current_file_path:
                status = st.session_state.novel_data.get('status', 'draft')
                st.selectbox(
                    "Status",
                    ["draft", "outline", "writing", "editing", "completed"],
                    index=["draft", "outline", "writing", "editing", "completed"].index(status),
                    key="novel_status",
                    on_change=self.update_novel_status
                )
        
        with col3:
            if st.session_state.current_file_path:
                # Auto-save indicator
                auto_save = st.toggle("Auto-save", value=True, key="auto_save_toggle")
                if auto_save:
                    st.caption("🟢 Auto-save enabled")
                else:
                    st.caption("🔴 Auto-save disabled")
        
        # Show unsaved changes warning
        if st.session_state.unsaved_changes:
            st.markdown("""
            <div class="unsaved-warning">
                ⚠️ <strong>Unsaved Changes</strong> - Remember to save your work!
            </div>
            """, unsafe_allow_html=True)
    
    def update_novel_status(self):
        """Update novel status"""
        if st.session_state.current_file_path:
            st.session_state.novel_data['status'] = st.session_state.novel_status
            st.session_state.unsaved_changes = True
    
    def render_main_content(self):
        """Render main content based on current view"""
        current_view = st.session_state.get('current_view', 'dashboard')
        
        # Navigation tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Dashboard", 
            "👥 Characters", 
            "📖 Chapters", 
            "🌍 World", 
            "📈 Analytics",
            "⚙️ Settings"
        ])
        
        with tab1:
            self.render_dashboard()
        with tab2:
            self.char_manager.render_character_manager()
        with tab3:
            self.chapter_manager.render_chapter_manager()
        with tab4:
            self.render_world_building()
        with tab5:
            self.render_analytics()
        with tab6:
            self.settings_manager.render_settings()
    
    def render_dashboard(self):
        """Render dashboard view"""
        if not st.session_state.current_file_path:
            self.render_welcome_screen()
            return
        
        # Novel overview
        novel_data = st.session_state.novel_data
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Chapters", len(novel_data.get('chapters', [])))
        with col2:
            st.metric("Characters", len(novel_data.get('characters', [])))
        with col3:
            word_count = sum(len(ch.get('content', '').split()) for ch in novel_data.get('chapters', []))
            st.metric("Words", word_count)
        with col4:
            st.metric("Status", novel_data.get('status', 'draft').title())
        
        st.divider()
        
        # Quick actions
        st.subheader("Quick Actions")
        
        col_act1, col_act2, col_act3, col_act4 = st.columns(4)
        
        with col_act1:
            if st.button("➕ Add Chapter", use_container_width=True):
                st.session_state.show_add_chapter = True
        
        with col_act2:
            if st.button("👤 Add Character", use_container_width=True):
                st.session_state.show_add_character = True
        
        with col_act3:
            if st.button("📝 Quick Note", use_container_width=True):
                st.session_state.show_quick_note = True
        
        with col_act4:
            if st.button("🎯 Set Goals", use_container_width=True):
                st.session_state.show_set_goals = True
        
        st.divider()
        
        # Recent activity
        st.subheader("Recent Activity")
        self.render_recent_activity()
    
    def render_welcome_screen(self):
        """Render welcome screen when no file is open"""
        st.markdown("""
        <div style='text-align: center; padding: 5rem;'>
            <h1 style='font-size: 3rem;'>📚</h1>
            <h2>Welcome to NovelCraft Pro</h2>
            <p style='color: #718096; margin-bottom: 2rem;'>
                Your professional novel writing assistant
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.info("💡 **Get Started**")
            
            option = st.radio(
                "Choose an option:",
                ["Create New Novel", "Open Existing Novel", "Import from File", "Try Template"]
            )
            
            if option == "Create New Novel":
                if st.button("🚀 Start New Project", use_container_width=True):
                    st.session_state.show_new_file_dialog = True
            
            elif option == "Open Existing Novel":
                if st.button("📂 Browse Files", use_container_width=True):
                    st.session_state.show_open_file_dialog = True
            
            elif option == "Import from File":
                uploaded_file = st.file_uploader("Choose a file", type=['json', 'txt', 'docx'])
                if uploaded_file:
                    # Handle file import
                    pass
            
            elif option == "Try Template":
                template = st.selectbox("Select Template", ["Fantasy Epic", "Romance Novel", "Mystery Thriller", "Science Fiction"])
                if st.button("Use Template", use_container_width=True):
                    # Load template
                    pass
    
    def render_recent_activity(self):
        """Render recent activity log"""
        if 'metadata' in st.session_state.novel_data:
            meta = st.session_state.novel_data['metadata']
            
            activities = []
            
            if 'created' in meta:
                activities.append(f"📅 Created: {self.format_date(meta['created'])}")
            if 'modified' in meta:
                activities.append(f"✏️ Last Modified: {self.format_date(meta['modified'])}")
            if 'last_opened' in meta:
                activities.append(f"📖 Last Opened: {self.format_date(meta['last_opened'])}")
            
            for activity in activities:
                st.write(activity)
    
    def format_date(self, date_string: str) -> str:
        """Format date string"""
        try:
            dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M")
        except:
            return date_string
    
    def render_world_building(self):
        """Render world building section"""
        st.header("🌍 World Building")
        
        if not st.session_state.current_file_path:
            st.info("Open a novel to access world building features")
            return
        
        tabs = st.tabs(["Locations", "Culture", "Magic/Technology", "History", "Maps"])
        
        with tabs[0]:
            self.render_locations()
        
        with tabs[1]:
            self.render_culture()
        
        with tabs[2]:
            self.render_magic_tech()
        
        with tabs[3]:
            self.render_history()
        
        with tabs[4]:
            self.render_maps()
    
    def render_locations(self):
        """Render locations manager"""
        st.subheader("Locations")
        
        if 'world_building' not in st.session_state.novel_data:
            st.session_state.novel_data['world_building'] = {}
        
        world = st.session_state.novel_data['world_building']
        world.setdefault('locations', [])
        
        # Add new location
        with st.expander("➕ Add New Location", expanded=False):
            with st.form("new_location_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Location Name")
                    type_loc = st.selectbox("Type", ["City", "Town", "Village", "Castle", "Forest", 
                                                    "Mountain", "Temple", "Dungeon", "Other"])
                
                with col2:
                    climate = st.selectbox("Climate", ["Temperate", "Tropical", "Desert", "Arctic", "Mountainous"])
                    importance = st.slider("Importance", 1, 10, 5)
                
                description = st.text_area("Description", height=100)
                
                if st.form_submit_button("Add Location"):
                    if name:
                        world['locations'].append({
                            'name': name,
                            'type': type_loc,
                            'climate': climate,
                            'importance': importance,
                            'description': description,
                            'characters': [],
                            'events': []
                        })
                        st.session_state.unsaved_changes = True
                        st.success(f"Location '{name}' added!")
                        st.rerun()
        
        # Display existing locations
        if world['locations']:
            st.subheader("Existing Locations")
            
            for i, loc in enumerate(world['locations']):
                with st.expander(f"📍 {loc['name']} ({loc['type']})", expanded=False):
                    col_loc1, col_loc2 = st.columns([2, 1])
                    
                    with col_loc1:
                        st.write(f"**Climate:** {loc['climate']}")
                        st.write(f"**Importance:** {loc['importance']}/10")
                        st.write(f"**Description:** {loc['description']}")
                    
                    with col_loc2:
                        if st.button("✏️ Edit", key=f"edit_loc_{i}"):
                            st.session_state.editing_location = i
                        
                        if st.button("🗑️ Delete", key=f"delete_loc_{i}"):
                            world['locations'].pop(i)
                            st.session_state.unsaved_changes = True
                            st.rerun()
        
        # Edit location dialog
        if 'editing_location' in st.session_state:
            self.render_edit_location()
    
    def render_edit_location(self):
        """Render location editor"""
        idx = st.session_state.editing_location
        world = st.session_state.novel_data['world_building']
        loc = world['locations'][idx]
        
        st.subheader(f"Edit Location: {loc['name']}")
        
        with st.form(f"edit_location_form_{idx}"):
            name = st.text_input("Name", value=loc['name'])
            type_loc = st.selectbox("Type", ["City", "Town", "Village", "Castle", "Forest", 
                                            "Mountain", "Temple", "Dungeon", "Other"],
                                   index=["City", "Town", "Village", "Castle", "Forest", 
                                         "Mountain", "Temple", "Dungeon", "Other"].index(loc['type']))
            climate = st.selectbox("Climate", ["Temperate", "Tropical", "Desert", "Arctic", "Mountainous"],
                                  index=["Temperate", "Tropical", "Desert", "Arctic", "Mountainous"].index(loc['climate']))
            importance = st.slider("Importance", 1, 10, loc['importance'])
            description = st.text_area("Description", value=loc['description'], height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                save = st.form_submit_button("💾 Save Changes")
            with col2:
                cancel = st.form_submit_button("❌ Cancel")
            
            if save:
                world['locations'][idx] = {
                    'name': name,
                    'type': type_loc,
                    'climate': climate,
                    'importance': importance,
                    'description': description,
                    'characters': loc.get('characters', []),
                    'events': loc.get('events', [])
                }
                st.session_state.unsaved_changes = True
                del st.session_state.editing_location
                st.success("Location updated!")
                st.rerun()
            
            if cancel:
                del st.session_state.editing_location
                st.rerun()
    
    def render_culture(self):
        """Render culture section"""
        st.subheader("Culture & Society")
        
        if 'world_building' not in st.session_state.novel_data:
            st.session_state.novel_data['world_building'] = {}
        
        world = st.session_state.novel_data['world_building']
        world.setdefault('cultures', [])
        
        # Culture form
        with st.expander("➕ Add Culture", expanded=False):
            with st.form("new_culture_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Culture Name")
                    government = st.selectbox("Government Type", 
                                            ["Monarchy", "Democracy", "Republic", "Theocracy", 
                                             "Tribal", "Anarchy", "Oligarchy", "Other"])
                
                with col2:
                    tech_level = st.selectbox("Technology Level", 
                                             ["Stone Age", "Bronze Age", "Iron Age", "Medieval",
                                              "Renaissance", "Industrial", "Modern", "Futuristic"])
                    morality = st.select_slider("Moral Alignment", 
                                               options=["Lawful Good", "Neutral Good", "Chaotic Good",
                                                       "Lawful Neutral", "True Neutral", "Chaotic Neutral",
                                                       "Lawful Evil", "Neutral Evil", "Chaotic Evil"])
                
                # Custom fields
                traditions = st.text_area("Traditions & Customs", height=80)
                religion = st.text_area("Religion & Beliefs", height=80)
                values = st.text_input("Core Values (comma separated)")
                
                if st.form_submit_button("Add Culture"):
                    if name:
                        world['cultures'].append({
                            'name': name,
                            'government': government,
                            'tech_level': tech_level,
                            'morality': morality,
                            'traditions': traditions,
                            'religion': religion,
                            'values': [v.strip() for v in values.split(',') if v.strip()]
                        })
                        st.session_state.unsaved_changes = True
                        st.success(f"Culture '{name}' added!")
                        st.rerun()
        
        # Display cultures
        if world['cultures']:
            for i, culture in enumerate(world['cultures']):
                with st.expander(f"🌐 {culture['name']}", expanded=False):
                    cols = st.columns(3)
                    with cols[0]:
                        st.write(f"**Government:** {culture['government']}")
                        st.write(f"**Tech Level:** {culture['tech_level']}")
                    with cols[1]:
                        st.write(f"**Morality:** {culture['morality']}")
                        st.write(f"**Values:** {', '.join(culture['values'])}")
                    with cols[2]:
                        if st.button("Edit", key=f"edit_culture_{i}"):
                            st.session_state.editing_culture = i
                        if st.button("Delete", key=f"delete_culture_{i}"):
                            world['cultures'].pop(i)
                            st.session_state.unsaved_changes = True
                            st.rerun()
                    
                    st.write(f"**Traditions:** {culture['traditions']}")
                    st.write(f"**Religion:** {culture['religion']}")
    
    def render_magic_tech(self):
        """Render magic/technology system"""
        st.subheader("Magic & Technology Systems")
        
        if 'world_building' not in st.session_state.novel_data:
            st.session_state.novel_data['world_building'] = {}
        
        world = st.session_state.novel_data['world_building']
        world.setdefault('systems', [])
        
        # System type selection
        system_type = st.radio("System Type", ["Magic", "Technology", "Psionics", "Other"], horizontal=True)
        
        with st.expander(f"➕ Add {system_type} System", expanded=False):
            with st.form(f"new_{system_type.lower()}_form"):
                name = st.text_input("System Name")
                source = st.text_input("Power Source")
                
                col1, col2 = st.columns(2)
                with col1:
                    rules = st.text_area("Rules & Limitations", height=100)
                with col2:
                    cost = st.text_area("Cost/Consequences", height=100)
                
                levels = st.slider("Power Levels", 1, 10, 5)
                accessibility = st.select_slider("Accessibility", 
                                               ["Very Rare", "Rare", "Uncommon", "Common", "Universal"])
                
                if st.form_submit_button(f"Add {system_type} System"):
                    if name:
                        world['systems'].append({
                            'name': name,
                            'type': system_type,
                            'source': source,
                            'rules': rules,
                            'cost': cost,
                            'levels': levels,
                            'accessibility': accessibility
                        })
                        st.session_state.unsaved_changes = True
                        st.success(f"{system_type} system '{name}' added!")
                        st.rerun()
        
        # Display systems
        if world['systems']:
            for i, system in enumerate(world['systems']):
                with st.expander(f"🔮 {system['name']} ({system['type']})", expanded=False):
                    cols = st.columns(2)
                    with cols[0]:
                        st.write(f"**Source:** {system['source']}")
                        st.write(f"**Levels:** {system['levels']}/10")
                        st.write(f"**Accessibility:** {system['accessibility']}")
                    with cols[1]:
                        if st.button("Edit", key=f"edit_system_{i}"):
                            st.session_state.editing_system = i
                        if st.button("Delete", key=f"delete_system_{i}"):
                            world['systems'].pop(i)
                            st.session_state.unsaved_changes = True
                            st.rerun()
                    
                    st.write(f"**Rules:** {system['rules']}")
                    st.write(f"**Cost:** {system['cost']}")
    
    def render_history(self):
        """Render historical timeline"""
        st.subheader("Historical Timeline")
        
        if 'world_building' not in st.session_state.novel_data:
            st.session_state.novel_data['world_building'] = {}
        
        world = st.session_state.novel_data['world_building']
        world.setdefault('timeline', [])
        
        # Add timeline event
        with st.expander("➕ Add Timeline Event", expanded=False):
            with st.form("new_timeline_event"):
                col1, col2 = st.columns(2)
                
                with col1:
                    year = st.text_input("Year/Date")
                    event_type = st.selectbox("Event Type", 
                                            ["Creation", "War", "Peace", "Discovery", 
                                             "Cataclysm", "Coronation", "Revolution", "Other"])
                
                with col2:
                    importance = st.select_slider("Importance", ["Minor", "Significant", "Major", "World-changing"])
                    duration = st.text_input("Duration")
                
                title = st.text_input("Event Title")
                description = st.text_area("Description", height=100)
                consequences = st.text_area("Consequences", height=80)
                
                if st.form_submit_button("Add Event"):
                    if title and year:
                        world['timeline'].append({
                            'year': year,
                            'type': event_type,
                            'importance': importance,
                            'duration': duration,
                            'title': title,
                            'description': description,
                            'consequences': consequences
                        })
                        st.session_state.unsaved_changes = True
                        st.success(f"Event '{title}' added!")
                        st.rerun()
        
        # Display timeline
        if world['timeline']:
            # Sort by year
            timeline_sorted = sorted(world['timeline'], key=lambda x: x['year'])
            
            for i, event in enumerate(timeline_sorted):
                # Color code by importance
                colors = {
                    "Minor": "#CBD5E0",
                    "Significant": "#4299E1",
                    "Major": "#ED8936",
                    "World-changing": "#F56565"
                }
                
                st.markdown(f"""
                <div style='border-left: 4px solid {colors.get(event['importance'], "#CBD5E0")}; 
                            padding: 1rem; margin: 0.5rem 0; background-color: #f8fafc;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <h4 style='margin: 0;'>{event['title']}</h4>
                        <span style='color: #718096;'>{event['year']}</span>
                    </div>
                    <div style='color: #4A5568; margin-top: 0.5rem;'>
                        {event['description']}
                    </div>
                    <div style='margin-top: 0.5rem;'>
                        <small><strong>Type:</strong> {event['type']} • 
                        <strong>Importance:</strong> {event['importance']} • 
                        <strong>Duration:</strong> {event['duration']}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Edit/Delete buttons
                col1, col2 = st.columns([6, 1])
                with col2:
                    if st.button("Edit", key=f"edit_event_{i}"):
                        st.session_state.editing_event = i
                    if st.button("Delete", key=f"delete_event_{i}"):
                        world['timeline'].pop(i)
                        st.session_state.unsaved_changes = True
                        st.rerun()
    
    def render_maps(self):
        """Render maps section"""
        st.subheader("Maps & Geography")
        
        st.info("🗺️ Map feature coming soon!")
        st.write("Upload or create maps for your world")
        
        # Placeholder for map upload/creation
        uploaded_map = st.file_uploader("Upload Map Image", type=['png', 'jpg', 'jpeg', 'svg'])
        
        if uploaded_map:
            st.image(uploaded_map, caption="Uploaded Map", use_column_width=True)
            
            # Map annotations
            st.subheader("Map Annotations")
            annotation = st.text_area("Add annotation to map")
            
            if st.button("Add Annotation"):
                if 'maps' not in st.session_state.novel_data['world_building']:
                    st.session_state.novel_data['world_building']['maps'] = []
                
                st.session_state.novel_data['world_building']['maps'].append({
                    'filename': uploaded_map.name,
                    'annotation': annotation,
                    'added': datetime.now().isoformat()
                })
                st.session_state.unsaved_changes = True
                st.success("Annotation added!")
    
    def render_analytics(self):
        """Render analytics dashboard"""
        st.header("📈 Analytics & Insights")
        
        if not st.session_state.current_file_path:
            st.info("Open a novel to view analytics")
            return
        
        novel_data = st.session_state.novel_data
        
        # Word count over time
        st.subheader("Writing Progress")
        
        # Calculate statistics
        chapters = novel_data.get('chapters', [])
        characters = novel_data.get('characters', [])
        
        total_words = sum(len(ch.get('content', '').split()) for ch in chapters)
        total_chars = sum(len(ch.get('content', '')) for ch in chapters)
        avg_words_per_chapter = total_words / len(chapters) if chapters else 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Words", f"{total_words:,}")
        with col2:
            st.metric("Total Chapters", len(chapters))
        with col3:
            st.metric("Avg Words/Chapter", f"{avg_words_per_chapter:,.0f}")
        with col4:
            st.metric("Total Characters", len(characters))
        
        st.divider()
        
        # Character analytics
        st.subheader("Character Analytics")
        
        if characters:
            # Character by role
            roles = {}
            for char in characters:
                role = char.get('role', 'secondary')
                roles[role] = roles.get(role, 0) + 1
            
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.write("**Characters by Role**")
                for role, count in roles.items():
                    st.progress(count / len(characters), text=f"{role.title()}: {count}")
            
            with col_chart2:
                st.write("**Character Development**")
                developed = sum(1 for char in characters if char.get('character_arc', '') != '')
                st.progress(developed / len(characters), text=f"Arcs Defined: {developed}/{len(characters)}")
        
        st.divider()
        
        # Writing goals
        st.subheader("Writing Goals")
        
        goal_words = st.number_input("Target Word Count", min_value=1000, value=50000, step=1000)
        
        progress = min(total_words / goal_words, 1.0)
        st.progress(progress, text=f"Progress: {total_words:,}/{goal_words:,} words ({progress*100:.1f}%)")
        
        # Estimated completion
        if total_words > 0 and chapters:
            avg_daily = st.number_input("Average words per day", min_value=100, value=1000, step=100)
            days_remaining = max(0, (goal_words - total_words) / avg_daily)
            
            st.write(f"**Estimated completion:** {days_remaining:.0f} days at {avg_daily:,} words/day")
    
    def run(self):
        """Main application loop"""
        # Render header
        self.render_header()
        
        # Render file operations sidebar
        self.file_ops.show_file_operations_sidebar()
        
        # Check for unsaved changes
        if st.session_state.unsaved_changes:
            self.file_ops.check_unsaved_changes()
        
        # Show dialogs if requested
        if st.session_state.get('show_new_file_dialog'):
            self.file_ops.show_new_file_dialog()
        
        if st.session_state.get('show_open_file_dialog'):
            self.file_ops.show_open_file_dialog()
        
        if st.session_state.get('show_save_as_dialog'):
            self.file_ops.show_save_as_dialog()
        
        # Render main content
        self.render_main_content()
        
        # Auto-save timer
        if st.session_state.get('auto_save_toggle', True) and st.session_state.current_file_path:
            # Auto-save every 30 seconds if there are unsaved changes
            if st.session_state.unsaved_changes:
                if 'last_auto_save' not in st.session_state:
                    st.session_state.last_auto_save = time.time()
                
                current_time = time.time()
                if current_time - st.session_state.last_auto_save > 30:  # 30 seconds
                    self.file_ops.save_current_file()
                    st.session_state.last_auto_save = current_time
                    
                    # Show auto-save notification
                    st.toast("Auto-saved!", icon="💾")

# Run the application
if __name__ == "__main__":
    app = NovelCraftApp()
    app.run()