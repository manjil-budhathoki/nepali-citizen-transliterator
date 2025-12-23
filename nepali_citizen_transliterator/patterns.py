#!/usr/bin/env python3
"""
Pattern definitions and validation for Nepali citizen data.
"""

import re

class NepaliPatterns:
    """Pattern matchers and validators for Nepali data."""
    
    # Regex patterns
    PATTERNS = {
        'nepali_name': r'^[A-Za-z\s\.\-]+$',
        'citizenship_number': r'^\d{1,2}-\d{1,5}-\d{1,10}(-\d{1,2})?$',
        'phone_nepal': r'^(\+?977)?[98]\d{9}$',
        'ward_number': r'^(ward|वडा)[\s]*(no\.?|नं\.?)?[\s]*(\d{1,3}|[१-९०]{1,3})$',
        'date_english': r'^\d{4}[-/]\d{1,2}[-/]\d{1,2}$',
        'date_nepali': r'^\d{4}[\./]\d{1,2}[\./]\d{1,2}$',
        'house_number': r'^(house|घर)[\s]*(no\.?|नं\.?)?[\s]*(\d+|[१-९०]+[A-Za-z]?)$',
    }
    
    # Nepali districts with codes (for citizenship number validation)
    DISTRICTS = {
        '01': 'ताप्लेजुङ', '02': 'पाँचथर', '03': 'इलाम', '04': 'झापा',
        '05': 'मोरङ', '06': 'सुनसरी', '07': 'धनकुटा', '08': 'तेह्रथुम',
        '09': 'संखुवासभा', '10': 'भोजपुर', '11': 'खोटाङ', '12': 'ओखलढुङ्गा',
        '13': 'उदयपुर', '14': 'सोलुखुम्बू', '15': 'रामेछाप', '16': 'दोलखा',
        '17': 'सिन्धुली', '18': 'काठमाडौं', '19': 'भक्तपुर', '20': 'ललितपुर',
        '21': 'काभ्रेपलाञ्चोक', '22': 'सिन्धुपाल्चोक', '23': 'रसुवा',
        '24': 'धादिङ', '25': 'नुवाकोट', '26': 'मकवानपुर', '27': 'चितवन',
        '28': 'गोरखा', '29': 'लमजुङ', '30': 'तनहुँ', '31': 'स्याङ्जा',
        '32': 'कास्की', '33': 'मनाङ', '34': 'मुस्ताङ', '35': 'पर्वत',
        '36': 'बागलुङ', '37': 'गुल्मी', '38': 'अर्घाखाँची', '39': 'प्युठान',
        '40': 'रोल्पा', '41': 'रुकुम', '42': 'सल्यान', '43': 'दाङ',
        '44': 'बाँके', '45': 'बर्दिया', '46': 'सुर्खेत', '47': 'दैलेख',
        '48': 'जाजरकोट', '49': 'डोल्पा', '50': 'जुम्ला', '51': 'कालिकोट',
        '52': 'मुगु', '53': 'हुम्ला', '54': 'बझाङ', '55': 'बाजुरा',
        '56': 'अछाम', '57': 'डोटी', '58': 'कैलाली', '59': 'कञ्चनपुर',
        '60': 'डडेल्धुरा', '61': 'बैतडी', '62': 'दार्चुला', '63': 'महाकाली',
        '64': 'कपिलवस्तु', '65': 'रुपन्देही', '66': 'नवलपरासी', '67': 'पाल्पा',
        '68': 'अर्घाखाँची', '69': 'गुल्मी', '70': 'रुकुम पूर्व', '71': 'रुकुम पश्चिम',
        '72': 'सल्यान', '73': 'दाङ', '74': 'बाँके', '75': 'बर्दिया',
    }
    
    # Common Nepali name components
    NAME_COMPONENTS = {
        'prefixes': ['श्री', 'श्रीमती', 'सुश्री', 'डा.', 'डाक्टर', 
                    'प्रो.', 'प्राध्यापक', 'मिस्टर', 'मिसेज', 'मिस'],
        'suffixes': ['ज्यू', 'दाई', 'बहिनी', 'काका', 'आमा', 'बुवा', 
                    'दिदी', 'दाई', 'बुढा', 'बुढी'],
        'titles': ['कुमार', 'कुमारी', 'बहादुर', 'प्रसाद', 'देवी', 
                  'लाल', 'श्रेष्ठ', 'मान', 'दास', 'नाथ'],
    }
    
    @staticmethod
    def validate_name(name: str) -> tuple[bool, str]:
        """Validate Nepali name and return (is_valid, message)."""
        if not name or not isinstance(name, str):
            return False, "Name cannot be empty"
        
        if len(name.strip()) < 2:
            return False, "Name too short"
        
        if len(name.strip()) > 100:
            return False, "Name too long"
        
        # Check for invalid characters
        invalid_chars = re.findall(r'[^\w\s\.\-]', name)
        if invalid_chars:
            return False, f"Invalid characters: {set(invalid_chars)}"
        
        return True, "Valid name"
    
    @staticmethod
    def validate_citizenship_number(number: str) -> tuple[bool, str]:
        """Validate Nepali citizenship number."""
        if not number:
            return False, "Citizenship number cannot be empty"
        
        # Check pattern
        pattern = r'^(\d{1,2})-(\d{1,5})-(\d{1,10})(-\d{1,2})?$'
        match = re.match(pattern, number)
        
        if not match:
            return False, "Invalid format. Use: DD-XXXXX-XXXXX"
        
        # Extract parts
        district_code = match.group(1)
        reg_series = match.group(2)
        reg_number = match.group(3)
        
        # Validate district code
        if district_code not in NepaliPatterns.DISTRICTS:
            return False, f"Invalid district code: {district_code}"
        
        # Check if all numbers are valid
        try:
            int(district_code)
            int(reg_series)
            int(reg_number)
        except ValueError:
            return False, "Must contain only numbers"
        
        return True, f"Valid citizenship number (District: {NepaliPatterns.DISTRICTS.get(district_code, 'Unknown')})"
    
    @staticmethod
    def extract_district_from_citizenship(citizenship_no: str) -> str:
        """Extract district name from citizenship number."""
        if not citizenship_no:
            return ""
        
        match = re.match(r'^(\d{1,2})', citizenship_no)
        if match:
            district_code = match.group(1)
            return NepaliPatterns.DISTRICTS.get(district_code, "")
        
        return ""
    
    @staticmethod
    def normalize_ward_number(ward_text: str) -> str:
        """Normalize ward number to standard format."""
        if not ward_text:
            return ""
        
        # Extract numbers
        numbers = re.findall(r'\d+', ward_text)
        nepali_numbers = re.findall(r'[१-९०]+', ward_text)
        
        if nepali_numbers:
            return f"वडा {nepali_numbers[0]}"
        elif numbers:
            return f"वडा {numbers[0]}"
        
        return ward_text
    
    @staticmethod
    def is_valid_nepali_date(date_str: str) -> bool:
        """Check if date is in valid Nepali format (YYYY.MM.DD)."""
        if not date_str:
            return False
        
        pattern = r'^\d{4}[\./]\d{1,2}[\./]\d{1,2}$'
        if not re.match(pattern, date_str):
            return False
        
        try:
            year, month, day = map(int, re.split(r'[\./]', date_str))
            
            # Basic validation
            if year < 1970 or year > 2100:
                return False
            if month < 1 or month > 12:
                return False
            if day < 1 or day > 32:
                return False
            
            return True
        except (ValueError, IndexError):
            return False
    
    @staticmethod
    def generate_citizenship_template(district_code: str = "01") -> str:
        """Generate a citizenship number template for given district."""
        if district_code in NepaliPatterns.DISTRICTS:
            district_name = NepaliPatterns.DISTRICTS[district_code]
            return f"{district_code}-12345-67890  # {district_name}"
        return "DD-XXXXX-XXXXX"
    
    @staticmethod
    def get_all_districts() -> dict:
        """Get all districts with codes and names."""
        return NepaliPatterns.DISTRICTS.copy()