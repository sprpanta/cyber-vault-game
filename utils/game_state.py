"""Game state management with session persistence"""

import streamlit as st
import random
from typing import Dict, List, Optional, Set, Tuple
from datetime import datetime

class GameState:
    """Manages all game state securely"""
    
    def __init__(self):
        self.initialize_state()
    
    def initialize_state(self):
        """Initialize or reset game state"""
        defaults = {
            'game_initialized': True,
            'current_card_index': 0,
            'shuffled_indices': [],
            'total_correct': 0,
            'total_attempts': 0,
            'current_streak': 0,
            'best_streak': 0,
            'vault_restored': 0,
            'selected_term': None,
            'selected_def': None,
            'matches': {},
            'revealed': False,
            'feedback': None,
            'feedback_type': None,
            'collected_fragments': [],
            'incorrect_pairs': [],
            'completed_cards': set(),
            'show_fragment': False,
            'current_fragment': None,
            'achievements': set(),
            'game_start_time': datetime.now().isoformat(),
            'session_id': self._generate_session_id(),
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
        
        # Initialize shuffled_indices if empty
        if not st.session_state.shuffled_indices:
            try:
                from data.questions import QUESTION_BANK
                indices = list(range(len(QUESTION_BANK)))
                random.shuffle(indices)
                st.session_state.shuffled_indices = indices
            except Exception as e:
                st.error(f"Error loading questions: {e}")
                st.session_state.shuffled_indices = []
    
    @staticmethod
    def _generate_session_id() -> str:
        """Generate a unique session ID"""
        import hashlib
        import time
        raw = f"{time.time()}{random.randint(1000, 9999)}"
        return hashlib.md5(raw.encode()).hexdigest()[:12]
    
    def reset_game(self):
        """Full game reset"""
        # Keep only essential keys that shouldn't be reset
        keep_keys = ['selected_domain'] if 'selected_domain' in st.session_state else []
        
        for key in list(st.session_state.keys()):
            if key not in keep_keys and key != 'game_initialized':
                del st.session_state[key]
        self.initialize_state()
    
    def get_progress_stats(self) -> Dict:
        """Get current progress statistics"""
        return {
            'vault_restored': st.session_state.vault_restored,
            'total_attempts': st.session_state.total_attempts,
            'total_correct': st.session_state.total_correct,
            'current_streak': st.session_state.current_streak,
            'best_streak': st.session_state.best_streak,
            'accuracy': self._calculate_accuracy(),
            'clearance_level': self._get_clearance_level(),
        }
    
    def _calculate_accuracy(self) -> float:
        """Calculate accuracy percentage"""
        if st.session_state.total_attempts == 0:
            return 0.0
        return (st.session_state.total_correct / st.session_state.total_attempts) * 100
    
    def _get_clearance_level(self) -> Dict:
        """Get current clearance level"""
        vault = st.session_state.vault_restored
        try:
            from data.questions import QUESTION_BANK
            total = len(QUESTION_BANK)
        except:
            total = 175
        
        levels = [
            (total, "Grandmaster Guardian", "⚫", "rank-grandmaster"),
            (int(total * 0.8), "Sentinel", "🟡", "rank-sentinel"),
            (int(total * 0.6), "Architect", "🟣", "rank-architect"),
            (int(total * 0.4), "Specialist", "🔵", "rank-specialist"),
            (int(total * 0.2), "Analyst", "⚪", "rank-analyst"),
            (0, "Initiate", "🟤", "rank-initiate"),
        ]
        for threshold, name, emoji, css_class in levels:
            if vault >= threshold:
                return {"name": name, "emoji": emoji, "css_class": css_class}
        return levels[-1]