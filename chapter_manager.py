# File: chapter_manager.py
import streamlit as st
from typing import Dict, List
import json

class ChapterManager:
    def __init__(self):
        pass
    
    def render_chapter_manager(self):
        """Render chapter management interface"""
        st.header("📖 Chapter Management")
        
        if not st.session_state.current_file_path:
            st.info("Open a novel to manage chapters")
            return
        
        # Tabs for different chapter views
        tab1, tab2, tab3, tab4 = st.tabs([
            "Chapter List", 
            "Write Chapter", 
            "Outline", 
            "Scene Manager"
        ])
        
        with tab1:
            self.render_chapter_list()
        
        with tab2:
            self.render_chapter_writer()
        
        with tab3:
            self.render_outline()
        
        with tab4:
            self.render_scene_manager()
    
    def render_chapter_list(self):
        """Render list of chapters"""
        chapters = st.session_state.novel_data.get('chapters', [])
        
        if not chapters:
            st.info("No chapters yet. Start writing!")
            return
        
        # Search and filter
        col_search, col_filter = st.columns(2)
        
        with col_search:
            search = st.text_input("Search chapters...")
        
        with col_filter:
            filter_status = st.selectbox("Filter by Status", 
                                        ["All", "Outline", "Draft", "Revised", "Final"])
        
        # Filter chapters
        filtered_chapters = chapters
        
        if search:
            filtered_chapters = [c for c in filtered_chapters 
                               if search.lower() in c.get('title', '').lower() or 
                                  search.lower() in c.get('content', '').lower()]
        
        if filter_status != "All":
            filtered_chapters = [c for c in filtered_chapters 
                               if c.get('status', '').lower() == filter_status.lower()]
        
        # Sort by chapter number
        filtered_chapters.sort(key=lambda x: x.get('number', 0))
        
        # Display chapters
        for chapter in filtered_chapters:
            with st.expander(f"📝 Chapter {chapter.get('number', 0)}: {chapter.get('title', 'Untitled')}", 
                           expanded=False):
                self.render_chapter_preview(chapter)
    
    def render_chapter_preview(self, chapter: Dict):
        """Render chapter preview"""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**Status:** {chapter.get('status', 'draft').title()}")
            st.write(f"**Word Count:** {len(chapter.get('content', '').split())}")
            st.write(f"**Last Modified:** {chapter.get('modified', 'Unknown')}")
            
            if 'summary' in chapter:
                st.write(f"**Summary:** {chapter['summary']}")
        
        with col2:
            if st.button("Edit", key=f"edit_chapter_{chapter.get('number')}", use_container_width=True):
                st.session_state.editing_chapter = chapter.get('number')
            
            if st.button("Delete", key=f"delete_chapter_{chapter.get('number')}", use_container_width=True):
                st.session_state.chapter_to_delete = chapter.get('number')
                st.session_state.show_delete_chapter_confirm = True
        
        # Show first 200 characters of content
        content_preview = chapter.get('content', '')[:200]
        if content_preview:
            st.caption(f"Preview: {content_preview}...")
    
    def render_chapter_writer(self):
        """Render chapter writing interface"""
        st.subheader("Write Chapter")
        
        # Chapter selection
        chapters = st.session_state.novel_data.get('chapters', [])
        
        if chapters:
            chapter_nums = [c['number'] for c in chapters]
            next_chapter = max(chapter_nums) + 1 if chapter_nums else 1
        else:
            next_chapter = 1
        
        col_new, col_existing = st.columns(2)
        
        with col_new:
            if st.button("➕ New Chapter", use_container_width=True):
                st.session_state.writing_new_chapter = True
                st.session_state.current_chapter_number = next_chapter
        
        with col_existing:
            if chapters:
                selected_chapter = st.selectbox(
                    "Edit Existing Chapter",
                    [f"Chapter {c['number']}: {c['title']}" for c in chapters],
                    key="select_existing_chapter"
                )
                
                if selected_chapter:
                    chapter_num = int(selected_chapter.split(":")[0].replace("Chapter ", ""))
                    if st.button("Edit Selected", use_container_width=True):
                        st.session_state.editing_chapter = chapter_num
        
        # Chapter editor
        if 'writing_new_chapter' in st.session_state or 'editing_chapter' in st.session_state:
            self.render_chapter_editor()
    
    def render_chapter_editor(self):
        """Render chapter editor"""
        # Determine chapter number
        if 'editing_chapter' in st.session_state:
            chapter_num = st.session_state.editing_chapter
            chapters = st.session_state.novel_data.get('chapters', [])
            chapter_data = next((c for c in chapters if c['number'] == chapter_num), None)
            
            if not chapter_data:
                st.error("Chapter not found!")
                return
        else:
            chapter_num = st.session_state.current_chapter_number
            chapter_data = {
                'number': chapter_num,
                'title': '',
                'content': '',
                'status': 'draft',
                'pov_character': '',
                'setting': '',
                'time_of_day': '',
                'summary': '',
                'word_count_goal': 2000,
                'characters': [],
                'locations': [],
                'conflicts': []
            }
        
        st.subheader(f"Chapter {chapter_num} Editor")
        
        # Basic info
        col_info1, col_info2, col_info3 = st.columns(3)
        
        with col_info1:
            title = st.text_input("Chapter Title", value=chapter_data.get('title', ''))
            status = st.selectbox("Status", 
                                ["outline", "draft", "revised", "final"],
                                index=["outline", "draft", "revised", "final"].index(
                                    chapter_data.get('status', 'draft')
                                ))
        
        with col_info2:
            pov_character = st.text_input("POV Character", value=chapter_data.get('pov_character', ''))
            setting = st.text_input("Setting", value=chapter_data.get('setting', ''))
        
        with col_info3:
            time_of_day = st.selectbox("Time of Day", 
                                     ["Morning", "Afternoon", "Evening", "Night", "Multiple"],
                                     index=["Morning", "Afternoon", "Evening", "Night", "Multiple"].index(
                                         chapter_data.get('time_of_day', 'Morning') 
                                         if chapter_data.get('time_of_day') in ["Morning", "Afternoon", "Evening", "Night", "Multiple"]
                                         else 0
                                     ))
            word_goal = st.number_input("Word Goal", min_value=100, 
                                       value=chapter_data.get('word_count_goal', 2000))
        
        # Summary
        summary = st.text_area("Chapter Summary", 
                             value=chapter_data.get('summary', ''),
                             height=80,
                             placeholder="Brief summary of what happens in this chapter...")
        
        # Characters in this chapter
        st.write("**Characters in this Chapter**")
        
        all_characters = st.session_state.novel_data.get('characters', [])
        if all_characters:
            char_names = [c['name'] for c in all_characters]
            selected_chars = st.multiselect(
                "Select characters appearing in this chapter",
                char_names,
                default=chapter_data.get('characters', [])
            )
        else:
            selected_chars = []
            st.info("No characters created yet")
        
        # Chapter content
        st.write("**Chapter Content**")
        
        content = st.text_area(
            "Write your chapter here...",
            value=chapter_data.get('content', ''),
            height=400,
            placeholder="Start writing your chapter...",
            key=f"chapter_content_{chapter_num}"
        )
        
        # Word count
        word_count = len(content.split())
        st.caption(f"Word Count: {word_count} / {word_goal} ({word_count/word_goal*100:.1f}%)")
        
        # Writing tools
        with st.expander("✏️ Writing Tools", expanded=False):
            col_tools1, col_tools2 = st.columns(2)
            
            with col_tools1:
                if st.button("📝 AI Suggestions"):
                    st.info("AI suggestions feature coming soon!")
            
            with col_tools2:
                if st.button("🔍 Spell Check"):
                    st.info("Spell check feature coming soon!")
            
            # Quick formatting
            st.write("**Quick Formatting**")
            col_format1, col_format2, col_format3 = st.columns(3)
            
            with col_format1:
                if st.button("Bold Selection"):
                    st.info("Formatting feature coming soon!")
            
            with col_format2:
                if st.button("Italic Selection"):
                    st.info("Formatting feature coming soon!")
            
            with col_format3:
                if st.button("Add Dialogue"):
                    st.info("Dialogue helper coming soon!")
        
        # Save buttons
        col_save1, col_save2, col_save3 = st.columns(3)
        
        with col_save1:
            if st.button("💾 Save Chapter", use_container_width=True, type="primary"):
                self.save_chapter(
                    chapter_num,
                    title,
                    content,
                    status,
                    summary,
                    pov_character,
                    setting,
                    time_of_day,
                    word_goal,
                    selected_chars
                )
                
                if 'writing_new_chapter' in st.session_state:
                    del st.session_state.writing_new_chapter
                if 'editing_chapter' in st.session_state:
                    del st.session_state.editing_chapter
                
                st.success("Chapter saved!")
                st.rerun()
        
        with col_save2:
            if st.button("💾 Save & Continue", use_container_width=True):
                self.save_chapter(
                    chapter_num,
                    title,
                    content,
                    status,
                    summary,
                    pov_character,
                    setting,
                    time_of_day,
                    word_goal,
                    selected_chars
                )
                
                if 'writing_new_chapter' in st.session_state:
                    st.session_state.current_chapter_number += 1
                    del st.session_state.writing_new_chapter
                if 'editing_chapter' in st.session_state:
                    del st.session_state.editing_chapter
                
                st.success("Chapter saved! Ready for next chapter.")
                st.rerun()
        
        with col_save3:
            if st.button("❌ Cancel", use_container_width=True):
                if 'writing_new_chapter' in st.session_state:
                    del st.session_state.writing_new_chapter
                if 'editing_chapter' in st.session_state:
                    del st.session_state.editing_chapter
                st.rerun()
    
    def save_chapter(self, chapter_num: int, title: str, content: str, status: str,
                    summary: str, pov_character: str, setting: str, time_of_day: str,
                    word_goal: int, characters: List[str]):
        """Save chapter data"""
        if 'chapters' not in st.session_state.novel_data:
            st.session_state.novel_data['chapters'] = []
        
        chapters = st.session_state.novel_data['chapters']
        
        # Check if chapter exists
        chapter_index = next((i for i, c in enumerate(chapters) if c['number'] == chapter_num), -1)
        
        chapter_data = {
            'number': chapter_num,
            'title': title,
            'content': content,
            'status': status,
            'summary': summary,
            'pov_character': pov_character,
            'setting': setting,
            'time_of_day': time_of_day,
            'word_count_goal': word_goal,
            'characters': characters,
            'locations': [],
            'conflicts': [],
            'created': datetime.now().isoformat() if chapter_index == -1 else chapters[chapter_index].get('created'),
            'modified': datetime.now().isoformat()
        }
        
        if chapter_index == -1:
            # New chapter
            chapters.append(chapter_data)
        else:
            # Update existing chapter
            chapters[chapter_index] = chapter_data
        
        # Update word count in metadata
        total_words = sum(len(c.get('content', '').split()) for c in chapters)
        if 'metadata' in st.session_state.novel_data:
            st.session_state.novel_data['metadata']['word_count'] = total_words
        
        st.session_state.unsaved_changes = True
    
    def render_outline(self):
        """Render novel outline"""
        st.subheader("Novel Outline")
        
        chapters = st.session_state.novel_data.get('chapters', [])
        
        if not chapters:
            st.info("No chapters to outline")
            return
        
        # Sort chapters
        chapters.sort(key=lambda x: x.get('number', 0))
        
        # Outline view
        for chapter in chapters:
            with st.expander(f"Chapter {chapter['number']}: {chapter.get('title', 'Untitled')}"):
                col_out1, col_out2 = st.columns([3, 1])
                
                with col_out1:
                    st.write(f"**Status:** {chapter.get('status', 'draft').title()}")
                    
                    if chapter.get('summary'):
                        st.write(f"**Summary:** {chapter['summary']}")
                    
                    if chapter.get('pov_character'):
                        st.write(f"**POV:** {chapter['pov_character']}")
                    
                    if chapter.get('setting'):
                        st.write(f"**Setting:** {chapter['setting']}")
                
                with col_out2:
                    # Progress indicator
                    content = chapter.get('content', '')
                    goal = chapter.get('word_count_goal', 2000)
                    word_count = len(content.split())
                    
                    progress = min(word_count / goal, 1.0)
                    
                    st.progress(progress, 
                               text=f"{word_count}/{goal} words ({progress*100:.1f}%)")
                    
                    # Characters in chapter
                    if chapter.get('characters'):
                        st.caption(f"Characters: {len(chapter['characters'])}")
        
        # Outline statistics
        st.divider()
        
        total_chapters = len(chapters)
        completed = sum(1 for c in chapters if c.get('status') == 'final')
        in_progress = sum(1 for c in chapters if c.get('status') in ['draft', 'revised'])
        outlined = sum(1 for c in chapters if c.get('status') == 'outline')
        
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        with col_stat1:
            st.metric("Total Chapters", total_chapters)
        with col_stat2:
            st.metric("Completed", completed)
        with col_stat3:
            st.metric("In Progress", in_progress)
        with col_stat4:
            st.metric("Outlined", outlined)
    
    def render_scene_manager(self):
        """Render scene management"""
        st.subheader("Scene Manager")
        
        chapters = st.session_state.novel_data.get('chapters', [])
        
        if not chapters:
            st.info("No chapters to manage scenes")
            return
        
        # Select chapter
        selected_chapter = st.selectbox(
            "Select Chapter",
            [f"Chapter {c['number']}: {c['title']}" for c in chapters],
            key="scene_chapter_select"
        )
        
        if not selected_chapter:
            return
        
        chapter_num = int(selected_chapter.split(":")[0].replace("Chapter ", ""))
        chapter = next((c for c in chapters if c['number'] == chapter_num), None)
        
        if not chapter:
            return
        
        st.write(f"**Managing scenes for Chapter {chapter_num}: {chapter.get('title', 'Untitled')}**")
        
        # Scene list
        if 'scenes' not in chapter:
            chapter['scenes'] = []
        
        scenes = chapter['scenes']
        
        # Add new scene
        with st.form("add_scene_form"):
            col_scene1, col_scene2 = st.columns(2)
            
            with col_scene1:
                scene_number = len(scenes) + 1
                scene_title = st.text_input("Scene Title")
                scene_type = st.selectbox("Scene Type", 
                                        ["Action", "Dialogue", "Description", "Reflection", "Transition"])
            
            with col_scene2:
                pov = st.text_input("POV Character", value=chapter.get('pov_character', ''))
                location = st.text_input("Location", value=chapter.get('setting', ''))
            
            purpose = st.text_area("Scene Purpose", height=60,
                                 placeholder="What does this scene accomplish?")
            
            if st.form_submit_button("➕ Add Scene"):
                scenes.append({
                    'number': scene_number,
                    'title': scene_title,
                    'type': scene_type,
                    'pov': pov,
                    'location': location,
                    'purpose': purpose,
                    'content': '',
                    'word_count': 0,
                    'characters': [],
                    'conflicts': []
                })
                st.session_state.unsaved_changes = True
                st.success("Scene added!")
                st.rerun()
        
        # Display scenes
        if scenes:
            for i, scene in enumerate(scenes):
                with st.expander(f"Scene {scene['number']}: {scene.get('title', 'Untitled')}"):
                    col_s1, col_s2 = st.columns([3, 1])
                    
                    with col_s1:
                        st.write(f"**Type:** {scene.get('type', 'Unknown')}")
                        st.write(f"**POV:** {scene.get('pov', 'Not specified')}")
                        st.write(f"**Location:** {scene.get('location', 'Not specified')}")
                        st.write(f"**Purpose:** {scene.get('purpose', 'Not specified')}")
                    
                    with col_s2:
                        if st.button("Edit", key=f"edit_scene_{i}"):
                            st.session_state.editing_scene = (chapter_num, i)
                        
                        if st.button("Delete", key=f"delete_scene_{i}"):
                            scenes.pop(i)
                            st.session_state.unsaved_changes = True
                            st.rerun()