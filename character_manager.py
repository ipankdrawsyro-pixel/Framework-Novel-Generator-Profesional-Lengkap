# File: character_manager.py
import streamlit as st
from typing import Dict, List
import json

class CharacterManager:
    def __init__(self):
        self.character_templates = self.load_templates()
    
    def load_templates(self) -> Dict:
        """Load character templates"""
        templates = {
            'hero': {
                'name': '',
                'role': 'protagonist',
                'archetype': 'The Hero',
                'description': '',
                'personality': {},
                'appearance': {},
                'background': {},
                'motivations': [],
                'relationships': [],
                'development_arc': ''
            },
            'villain': {
                'name': '',
                'role': 'antagonist',
                'archetype': 'The Villain',
                'description': '',
                'personality': {},
                'appearance': {},
                'background': {},
                'motivations': [],
                'relationships': [],
                'development_arc': ''
            }
            # Add more templates...
        }
        return templates
    
    def render_character_manager(self):
        """Render character management interface"""
        st.header("👥 Character Management")
        
        if not st.session_state.current_file_path:
            st.info("Open a novel to manage characters")
            return
        
        # Tabs for different character views
        tab1, tab2, tab3, tab4 = st.tabs([
            "Character List", 
            "Add Character", 
            "Relationships", 
            "Development"
        ])
        
        with tab1:
            self.render_character_list()
        
        with tab2:
            self.render_add_character()
        
        with tab3:
            self.render_relationships()
        
        with tab4:
            self.render_development_tracking()
    
    def render_character_list(self):
        """Render list of characters"""
        characters = st.session_state.novel_data.get('characters', [])
        
        if not characters:
            st.info("No characters yet. Add your first character!")
            return
        
        # Search and filter
        col_search, col_filter, col_sort = st.columns(3)
        
        with col_search:
            search = st.text_input("Search characters...")
        
        with col_filter:
            filter_role = st.selectbox("Filter by Role", 
                                      ["All", "Protagonist", "Antagonist", "Supporting", "Minor"])
        
        with col_sort:
            sort_by = st.selectbox("Sort by", 
                                  ["Name", "Role", "Importance", "Recently Added"])
        
        # Filter characters
        filtered_chars = characters
        
        if search:
            filtered_chars = [c for c in filtered_chars 
                            if search.lower() in c.get('name', '').lower()]
        
        if filter_role != "All":
            filtered_chars = [c for c in filtered_chars 
                            if c.get('role', '').lower() == filter_role.lower()]
        
        # Sort characters
        if sort_by == "Name":
            filtered_chars.sort(key=lambda x: x.get('name', '').lower())
        elif sort_by == "Role":
            filtered_chars.sort(key=lambda x: x.get('role', ''))
        elif sort_by == "Importance":
            filtered_chars.sort(key=lambda x: x.get('importance', 0), reverse=True)
        elif sort_by == "Recently Added":
            filtered_chars.sort(key=lambda x: x.get('added_date', ''), reverse=True)
        
        # Display characters
        for i, char in enumerate(filtered_chars):
            with st.expander(f"👤 {char.get('name', 'Unnamed')}", expanded=False):
                self.render_character_card(char, i)
    
    def render_character_card(self, character: Dict, index: int):
        """Render individual character card"""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**Role:** {character.get('role', 'Unknown')}")
            st.write(f"**Archetype:** {character.get('archetype', 'Not specified')}")
            
            if 'description' in character:
                st.write(f"**Description:** {character.get('description', '')}")
            
            # Quick stats
            cols_stats = st.columns(4)
            with cols_stats[0]:
                st.metric("Importance", character.get('importance', 0))
            with cols_stats[1]:
                st.metric("Age", character.get('age', 'Unknown'))
            with cols_stats[2]:
                st.metric("Scenes", len(character.get('appearances', [])))
        
        with col2:
            if st.button("Edit", key=f"edit_char_{index}", use_container_width=True):
                st.session_state.editing_character = index
            
            if st.button("Delete", key=f"delete_char_{index}", use_container_width=True):
                st.session_state.novel_data['characters'].pop(index)
                st.session_state.unsaved_changes = True
                st.success("Character deleted!")
                st.rerun()
    
    def render_add_character(self):
        """Render character creation form"""
        st.subheader("Add New Character")
        
        # Template selection
        template = st.selectbox(
            "Start with template",
            ["Custom", "Hero/Protagonist", "Villain/Antagonist", "Love Interest", 
             "Mentor", "Sidekick", "Comic Relief", "Foil Character"]
        )
        
        # Main form
        with st.form("add_character_form"):
            # Basic Info
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Character Name*", placeholder="Enter full name")
                alias = st.text_input("Alias/Nickname", placeholder="Optional")
                role = st.selectbox("Role*", 
                                  ["Protagonist", "Antagonist", "Supporting", "Minor", "Ensemble"])
                archetype = st.selectbox("Archetype", 
                                       ["The Hero", "The Mentor", "The Shadow", "The Trickster",
                                        "The Guardian", "The Herald", "The Shapeshifter", "The Lover"])
            
            with col2:
                age = st.number_input("Age", min_value=0, max_value=150, value=25)
                gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Other", "Not specified"])
                species = st.text_input("Species/Race", placeholder="Human, Elf, etc.")
                occupation = st.text_input("Occupation")
            
            # Appearance
            st.subheader("Appearance")
            col_app1, col_app2 = st.columns(2)
            
            with col_app1:
                height = st.text_input("Height")
                build = st.selectbox("Build", ["Slim", "Average", "Athletic", "Muscular", "Stocky", "Large"])
                hair_color = st.text_input("Hair Color")
                hair_style = st.text_input("Hair Style")
            
            with col_app2:
                eye_color = st.text_input("Eye Color")
                skin_tone = st.text_input("Skin Tone")
                distinguishing_features = st.text_area("Distinguishing Features", height=60)
                clothing_style = st.text_input("Typical Clothing")
            
            # Personality
            st.subheader("Personality")
            
            col_per1, col_per2 = st.columns(2)
            with col_per1:
                mbti = st.selectbox("MBTI Type (Optional)", 
                                  ["", "INTJ", "INTP", "ENTJ", "ENTP",
                                   "INFJ", "INFP", "ENFJ", "ENFP",
                                   "ISTJ", "ISFJ", "ESTJ", "ESFJ",
                                   "ISTP", "ISFP", "ESTP", "ESFP"])
                
                virtues = st.text_area("Virtues/Strengths", placeholder="Brave, loyal, intelligent...")
            
            with col_per2:
                enneagram = st.selectbox("Enneagram (Optional)", 
                                       ["", "Type 1", "Type 2", "Type 3", "Type 4",
                                        "Type 5", "Type 6", "Type 7", "Type 8", "Type 9"])
                
                flaws = st.text_area("Flaws/Weaknesses", placeholder="Prideful, stubborn, impulsive...")
            
            personality_traits = st.text_input("Key Personality Traits", 
                                             placeholder="Comma separated: ambitious, witty, cynical")
            
            # Background
            st.subheader("Background")
            background = st.text_area("Backstory", height=100)
            
            col_bg1, col_bg2 = st.columns(2)
            with col_bg1:
                birthplace = st.text_input("Birthplace/Hometown")
                education = st.text_input("Education/Training")
            with col_bg2:
                family = st.text_input("Family")
                trauma = st.text_input("Significant Trauma/Events")
            
            # Motivations
            st.subheader("Motivations & Goals")
            
            external_goal = st.text_input("External Goal (What they want)")
            internal_need = st.text_input("Internal Need (What they need)")
            fear = st.text_input("Greatest Fear")
            secret = st.text_input("Secret")
            
            # Character Arc
            st.subheader("Character Development")
            
            arc_type = st.selectbox("Character Arc", 
                                  ["Flat", "Growth", "Corruption", "Redemption", "Fall", "Transformation"])
            
            starting_point = st.text_area("Starting Point (Beginning of story)", height=60)
            development = st.text_area("Development (Middle of story)", height=60)
            end_point = st.text_area("End Point (End of story)", height=60)
            
            # Importance
            importance = st.slider("Character Importance", 1, 10, 5,
                                 help="1 = Minor character, 10 = Main character")
            
            # Submit button
            col_sub1, col_sub2 = st.columns(2)
            with col_sub1:
                submit = st.form_submit_button("➕ Add Character", use_container_width=True)
            with col_sub2:
                save_template = st.form_submit_button("💾 Save as Template", use_container_width=True)
            
            if submit:
                if not name:
                    st.error("Character name is required!")
                else:
                    character = {
                        'name': name,
                        'alias': alias,
                        'role': role,
                        'archetype': archetype,
                        'age': age,
                        'gender': gender,
                        'species': species,
                        'occupation': occupation,
                        
                        'appearance': {
                            'height': height,
                            'build': build,
                            'hair_color': hair_color,
                            'hair_style': hair_style,
                            'eye_color': eye_color,
                            'skin_tone': skin_tone,
                            'distinguishing_features': distinguishing_features,
                            'clothing_style': clothing_style
                        },
                        
                        'personality': {
                            'mbti': mbti,
                            'enneagram': enneagram,
                            'virtues': [v.strip() for v in virtues.split(',') if v.strip()],
                            'flaws': [f.strip() for f in flaws.split(',') if f.strip()],
                            'traits': [t.strip() for t in personality_traits.split(',') if t.strip()]
                        },
                        
                        'background': {
                            'backstory': background,
                            'birthplace': birthplace,
                            'education': education,
                            'family': family,
                            'trauma': trauma
                        },
                        
                        'motivations': {
                            'external_goal': external_goal,
                            'internal_need': internal_need,
                            'fear': fear,
                            'secret': secret
                        },
                        
                        'character_arc': {
                            'type': arc_type,
                            'starting_point': starting_point,
                            'development': development,
                            'end_point': end_point
                        },
                        
                        'importance': importance,
                        'added_date': datetime.now().isoformat(),
                        'appearances': [],
                        'relationships': []
                    }
                    
                    # Add to novel data
                    if 'characters' not in st.session_state.novel_data:
                        st.session_state.novel_data['characters'] = []
                    
                    st.session_state.novel_data['characters'].append(character)
                    st.session_state.unsaved_changes = True
                    
                    st.success(f"Character '{name}' added successfully!")
                    st.rerun()
            
            if save_template:
                # Save as custom template
                st.info("Template saving feature coming soon!")
    
    def render_relationships(self):
        """Render character relationship manager"""
        st.subheader("Character Relationships")
        
        characters = st.session_state.novel_data.get('characters', [])
        
        if len(characters) < 2:
            st.info("Add at least 2 characters to manage relationships")
            return
        
        # Relationship matrix
        st.write("**Relationship Matrix**")
        
        # Create relationship editor
        char1 = st.selectbox("Select Character 1", 
                           [c['name'] for c in characters], 
                           key="rel_char1")
        char2 = st.selectbox("Select Character 2", 
                           [c['name'] for c in characters if c['name'] != char1], 
                           key="rel_char2")
        
        # Find existing relationship
        relationship_type = st.selectbox("Relationship Type", 
                                       ["Friends", "Family", "Romantic", "Rivals", 
                                        "Enemies", "Mentor-Student", "Colleagues", "Other"])
        
        strength = st.slider("Relationship Strength", -10, 10, 0,
                           help="-10 = Extreme hatred, 0 = Neutral, 10 = Deep love")
        
        description = st.text_area("Relationship Description", height=100)
        
        col_rel1, col_rel2 = st.columns(2)
        with col_rel1:
            if st.button("💝 Set Relationship", use_container_width=True):
                self.set_relationship(char1, char2, relationship_type, strength, description)
        with col_rel2:
            if st.button("🗑️ Clear Relationship", use_container_width=True):
                self.clear_relationship(char1, char2)
        
        # Visual relationship map
        st.divider()
        st.write("**Relationship Map**")
        
        # Simple visualization
        for char in characters:
            if 'relationships' in char and char['relationships']:
                st.write(f"**{char['name']}**")
                for rel in char['relationships'][:3]:  # Show first 3
                    st.write(f"  - {rel['with']}: {rel['type']} ({rel['strength']})")
    
    def set_relationship(self, char1_name: str, char2_name: str, rel_type: str, strength: int, description: str):
        """Set relationship between two characters"""
        characters = st.session_state.novel_data.get('characters', [])
        
        # Find character indices
        char1_idx = next((i for i, c in enumerate(characters) if c['name'] == char1_name), -1)
        char2_idx = next((i for i, c in enumerate(characters) if c['name'] == char2_name), -1)
        
        if char1_idx == -1 or char2_idx == -1:
            st.error("Character not found!")
            return
        
        # Create relationship data
        rel_data = {
            'with': char2_name,
            'type': rel_type,
            'strength': strength,
            'description': description,
            'updated': datetime.now().isoformat()
        }
        
        # Update character 1's relationships
        if 'relationships' not in characters[char1_idx]:
            characters[char1_idx]['relationships'] = []
        
        # Remove existing relationship if any
        characters[char1_idx]['relationships'] = [
            r for r in characters[char1_idx]['relationships'] 
            if r['with'] != char2_name
        ]
        
        characters[char1_idx]['relationships'].append(rel_data)
        
        # Also update character 2's relationships (bidirectional)
        if 'relationships' not in characters[char2_idx]:
            characters[char2_idx]['relationships'] = []
        
        rel_data_reverse = rel_data.copy()
        rel_data_reverse['with'] = char1_name
        
        characters[char2_idx]['relationships'] = [
            r for r in characters[char2_idx]['relationships'] 
            if r['with'] != char1_name
        ]
        
        characters[char2_idx]['relationships'].append(rel_data_reverse)
        
        st.session_state.unsaved_changes = True
        st.success(f"Relationship set between {char1_name} and {char2_name}!")
    
    def clear_relationship(self, char1_name: str, char2_name: str):
        """Clear relationship between two characters"""
        characters = st.session_state.novel_data.get('characters', [])
        
        for char in characters:
            if char['name'] in [char1_name, char2_name] and 'relationships' in char:
                char['relationships'] = [
                    r for r in char['relationships'] 
                    if r['with'] not in [char1_name, char2_name]
                ]
        
        st.session_state.unsaved_changes = True
        st.success(f"Relationship cleared between {char1_name} and {char2_name}!")
    
    def render_development_tracking(self):
        """Render character development tracking"""
        st.subheader("Character Development Tracking")
        
        characters = st.session_state.novel_data.get('characters', [])
        
        if not characters:
            st.info("No characters to track")
            return
        
        # Select character to track
        selected_char = st.selectbox(
            "Select Character",
            [c['name'] for c in characters],
            key="dev_char_select"
        )
        
        # Find character
        character = next((c for c in characters if c['name'] == selected_char), None)
        
        if not character:
            return
        
        # Development tracking
        st.write(f"**Tracking Development for: {selected_char}**")
        
        # Arc progress
        if 'character_arc' in character:
            arc = character['character_arc']
            
            st.write(f"**Arc Type:** {arc.get('type', 'Not specified')}")
            
            col_arc1, col_arc2, col_arc3 = st.columns(3)
            with col_arc1:
                st.write("**Starting Point**")
                st.info(arc.get('starting_point', 'Not defined'))
            with col_arc2:
                st.write("**Development**")
                st.warning(arc.get('development', 'Not defined'))
            with col_arc3:
                st.write("**End Point**")
                st.success(arc.get('end_point', 'Not defined'))
        
        # Scene appearances tracking
        st.subheader("Scene Appearances")
        
        if 'appearances' not in character:
            character['appearances'] = []
        
        # Add new appearance
        with st.form("add_appearance_form"):
            chapter = st.number_input("Chapter", min_value=1, value=1)
            scene = st.number_input("Scene", min_value=1, value=1)
            description = st.text_input("Scene Description")
            significance = st.select_slider("Significance", ["Minor", "Medium", "Major"])
            development = st.text_area("Character Development in this Scene", height=80)
            
            if st.form_submit_button("➕ Add Appearance"):
                character['appearances'].append({
                    'chapter': chapter,
                    'scene': scene,
                    'description': description,
                    'significance': significance,
                    'development': development,
                    'timestamp': datetime.now().isoformat()
                })
                st.session_state.unsaved_changes = True
                st.success("Appearance added!")
                st.rerun()
        
        # List appearances
        if character['appearances']:
            st.write("**Appearance History**")
            for i, app in enumerate(character['appearances']):
                with st.expander(f"Chapter {app['chapter']}, Scene {app['scene']}: {app['description']}"):
                    st.write(f"**Significance:** {app['significance']}")
                    st.write(f"**Development:** {app['development']}")
                    
                    col_app1, col_app2 = st.columns(2)
                    with col_app1:
                        if st.button("Edit", key=f"edit_app_{i}"):
                            st.session_state.editing_appearance = i
                    with col_app2:
                        if st.button("Delete", key=f"delete_app_{i}"):
                            character['appearances'].pop(i)
                            st.session_state.unsaved_changes = True
                            st.rerun()