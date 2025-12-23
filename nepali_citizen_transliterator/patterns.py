#!/usr/bin/env python3
"""
Pattern definitions for Nepali citizen data transliteration
Contains regex patterns and validation rules for Nepali personal data.
"""

import re

class NepaliPatterns:
    """Pattern matchers for Nepali citizen data."""
    
    # Regex patterns for different data types
    PATTERNS = {
        # Nepali names (common patterns)
        'name': r'^[A-Za-z\s\.\-]+$',
        
        # Citizenship number patterns (05-01-123456-12, 1-1234-56789, etc.)
        'citizenship_number': r'^\d{1,2}-\d{1,5}-\d{1,10}(-\d{1,2})?$',
        
        # Nepali phone numbers
        'phone': r'^(\+?977)?[98]\d{9}$',
        
        # Ward numbers (Ward 1, वडा ५, etc.)
        'ward': r'^(ward|वडा)[\s]*(\d{1,2}|[१-९०]{1,2})$',
        
        # Date patterns (YYYY-MM-DD, YYYY/MM/DD, etc.)
        'date': r'^\d{4}[-/]\d{1,2}[-/]\d{1,2}$',
        
        # House numbers
        'house_number': r'^(house|घर)[\s]*(no\.?|नं\.?)?[\s]*(\d+|[१-९०]+)$',
    }
    
    # Common Nepali name prefixes and suffixes
    NAME_PREFIXES = [
        'श्री', 'श्रीमती', 'सुश्री', 'डा.', 'डाक्टर', 'प्रो.', 'प्राध्यापक',
        'mr.', 'mrs.', 'miss', 'dr.', 'prof.'
    ]
    
    NAME_SUFFIXES = [
        'ज्यू', 'दाई', 'बहिनी', 'काका', 'आमा', 'बुवा', 'दिदी', 'दाई'
    ]
    
    # Common address components
    ADDRESS_COMPONENTS = {
        'north': 'उत्तर',
        'south': 'दक्षिण', 
        'east': 'पूर्व',
        'west': 'पश्चिम',
        'center': 'केन्द्र',
        'tole': 'टोल',
        'sadak': 'सडक',
        'marga': 'मार्ग',
        'chowk': 'चोक',
        'bazar': 'बजार',
        'basti': 'बस्ती',
        'toles': 'टोल्स',
    }
    
    # District codes (for citizenship numbers)
    DISTRICT_CODES = {
        '01': 'ताप्लेजुङ',
        '02': 'पाँचथर',
        '03': 'इलाम',
        '04': 'झापा',
        '05': 'मोरङ',
        '06': 'सुनसरी',
        '07': 'धनकुटा',
    }
    
    @classmethod
    def is_valid_name(cls, name: str) -> bool:
        """Check if string looks like a valid Nepali name."""
        if not name or not isinstance(name, str):
            return False
        
        # Remove common prefixes/suffixes for validation
        name_clean = name.lower()
        for prefix in cls.NAME_PREFIXES:
            if name_clean.startswith(prefix.lower()):
                name_clean = name_clean[len(prefix):].strip()
        
        # Check basic pattern
        return bool(re.match(cls.PATTERNS['name'], name_clean.strip()))
    
    @classmethod
    def is_citizenship_number(cls, text: str) -> bool:
        """Check if text matches Nepali citizenship number pattern."""
        if not text:
            return False
        return bool(re.match(cls.PATTERNS['citizenship_number'], text.strip()))
    
    @classmethod
    def extract_ward_number(cls, text: str) -> str:
        """Extract ward number from text."""
        match = re.search(r'(\d+|[१-९०]+)', str(text))
        return match.group(1) if match else ""
    
    @classmethod
    def normalize_address(cls, address: str) -> str:
        """Normalize address by standardizing common terms."""
        if not address:
            return ""
        
        normalized = address.lower()
        
        # Standardize common address terms
        replacements = {
            'rd.': 'road',
            'st.': 'street',
            'ave.': 'avenue',
            'blvd.': 'boulevard',
            'no.': 'number',
            'apt.': 'apartment',
            'ward no.': 'ward',
            'house no.': 'house',
            'municipality': 'municipality',
            'gaunpalika': 'rural municipality',
            'n.p.': 'nagarpalika',
            'g.p.': 'gaunpalika',
        }
        
        for old, new in replacements.items():
            normalized = normalized.replace(old, new)
        
        return normalized.strip()
    
    @classmethod
    def get_district_name(cls, code: str) -> str:
        """Get Nepali district name from code."""
        return cls.DISTRICT_CODES.get(code.strip(), "")