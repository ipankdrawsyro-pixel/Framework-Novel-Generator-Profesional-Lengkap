# File: app.py (Main Application)
import streamlit as st
import os
import json
import shutil
import pandas as pd
from datetime import datetime
from pathlib import Path
import sys
import hashlib

# Initialize session state variables
def init_session_state():
    if 'current_novel' not in st.session_state:
        st.session_state.current_novel = None
    if 'unsaved_changes' not in st.session_state:
        st.session_state.unsaved_changes = False
    if 'novel_data' not in st.session_state:
        st.session_state.novel_data = {}
    if 'file_list' not in st.session_state:
        st.session_state.file_list = []
    if 'current_file_path' not in st.session_state:
        st.session_state.current_file_path = None

init_session_state()