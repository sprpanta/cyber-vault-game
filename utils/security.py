"""Security utilities for the application"""

import hashlib
import hmac
import streamlit as st
from typing import Optional
import os

class SecurityManager:
    """Handles security aspects of the game"""
    
    @staticmethod
    def validate_session() -> bool:
        """Validate the current session"""
        if 'session_id' not in st.session_state:
            return False
        
        # Check session age (expire after 24 hours)
        from datetime import datetime, timedelta
        if 'game_start_time' in st.session_state:
            start_time = datetime.fromisoformat(st.session_state.game_start_time)
            if datetime.now() - start_time > timedelta(hours=24):
                return False
        
        return True
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input"""
        import re
        # Remove any HTML tags
        text = re.sub(r'<[^>]*>', '', text)
        # Remove any script injections
        text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
        # Limit length
        return text[:500]
    
    @staticmethod
    def hash_data(data: str) -> str:
        """Create a hash of data for integrity checking"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def verify_data_integrity(original: str, stored_hash: str) -> bool:
        """Verify data hasn't been tampered with"""
        return SecurityManager.hash_data(original) == stored_hash
    
    @staticmethod
    def get_security_headers() -> dict:
        """Get security headers for the application"""
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';",
        }