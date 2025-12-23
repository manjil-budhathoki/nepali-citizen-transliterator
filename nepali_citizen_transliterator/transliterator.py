#!/usr/bin/env python3
"""
Nepali Citizen Transliterator
Specialized transliterator for Nepali citizen documents (names, addresses, IDs)
"""

class CitizenTransliterator:
    """Transliterator optimized for Nepali citizen data."""
    
    # Core transliteration mappings for Nepali names/addresses
    CHAR_MAP = {
        # Vowels
        'a': 'अ', 'aa': 'आ', 'i': 'इ', 'ee': 'ई', 'u': 'उ', 'oo': 'ऊ',
        'e': 'ए', 'ai': 'ऐ', 'o': 'ओ', 'au': 'औ',
        
        # Consonants (common in names)
        'k': 'क', 'kh': 'ख', 'g': 'ग', 'gh': 'घ',
        'ch': 'च', 'chh': 'छ', 'j': 'ज', 'jh': 'झ',
        't': 'ट', 'th': 'ठ', 'd': 'ड', 'dh': 'ढ', 'n': 'ण',
        't': 'त', 'th': 'थ', 'd': 'द', 'dh': 'ध', 'n': 'न',
        'p': 'प', 'ph': 'फ', 'b': 'ब', 'bh': 'भ', 'm': 'म',
        'y': 'य', 'r': 'र', 'l': 'ल', 'w': 'व', 'v': 'व',
        'sh': 'श', 's': 'स', 'h': 'ह',
        
        # Special combinations in names
        'gy': 'ज्ञ', 'tr': 'त्र', 'ksh': 'क्ष',
    }
    
    # Common Nepali names and titles (for better accuracy)
    COMMON_NAMES = {
        # Common first names
        'ram': 'राम', 'shyam': 'श्याम', 'hari': 'हरि', 'krishna': 'कृष्ण',
        'gopal': 'गोपाल', 'mohan': 'मोहन', 'sita': 'सीता', 'gita': 'गीता',
        'radha': 'राधा', 'laxmi': 'लक्ष्मी', 'saraswati': 'सरस्वती',
        
        # Common last names
        'sharma': 'शर्मा', 'poudel': 'पौडेल', 'bhattarai': 'भट्टराई',
        'kc': 'केसी', 'karki': 'कार्की', 'rai': 'राई', 'limbu': 'लिम्बू',
        'maharjan': 'महर्जन', 'tamang': 'तामाङ',
        
        # Titles
        'kumar': 'कुमार', 'kumari': 'कुमारी', 'bahadur': 'बहादुर',
        'prasad': 'प्रसाद', 'devi': 'देवी', 'lal': 'लाल',
    }
    
    # Common place names (districts, cities)
    COMMON_PLACES = {
        'kathmandu': 'काठमाडौं', 'pokhara': 'पोखरा', 'bhaktapur': 'भक्तपुर',
        'lalitpur': 'ललितपुर', 'biratnagar': 'विराटनगर', 'birgunj': 'बीरगञ्ज',
        'nepalgunj': 'नेपालगञ्ज', 'dharan': 'धरान', 'butwal': 'बुटवल',
        'hetauda': 'हेटौंडा', 'dhangadhi': 'धनगढी', 'tikapur': 'टीकापुर',
        
        # Districts
        'kaski': 'कास्की', 'chitwan': 'चितवन', 'jhapa': 'झापा', 'morang': 'मोरङ',
        'sunari': 'सुनसरी', 'banke': 'बाँके', 'bardiya': 'बर्दिया',
        
        # Address terms
        'municipality': 'नगरपालिका', 'rural': 'गाउँपालिका', 'ward': 'वडा',
        'tole': 'टोल', 'sadak': 'सडक', 'ghar': 'घर', 'basti': 'बस्ती',
    }
    
    def __init__(self):
        """Initialize the transliterator."""
        # Combine all dictionaries
        self.dictionary = {}
        self.dictionary.update(self.COMMON_NAMES)
        self.dictionary.update(self.COMMON_PLACES)
    
    def transliterate_name(self, name: str) -> str:
        """
        Transliterate a Nepali name from Roman to Devanagari.
        
        Args:
            name: Romanized Nepali name (e.g., "Ram Bahadur Shrestha")
            
        Returns:
            Name in Devanagari script
        """
        if not name:
            return ""
        
        # Convert to lowercase for lookup
        name_lower = name.lower()
        
        # Check if entire name is in dictionary
        if name_lower in self.dictionary:
            return self.dictionary[name_lower]
        
        # Split and transliterate each part
        parts = name.split()
        transliterated_parts = []
        
        for part in parts:
            part_lower = part.lower()
            
            # Check if part is in dictionary
            if part_lower in self.dictionary:
                transliterated_parts.append(self.dictionary[part_lower])
            else:
                # Apply character-by-character transliteration
                transliterated = self._transliterate_word(part)
                transliterated_parts.append(transliterated)
        
        return " ".join(transliterated_parts)
    
    def transliterate_address(self, address: str) -> str:
        """
        Transliterate a Nepali address from Roman to Devanagari.
        
        Args:
            address: Romanized Nepali address
            
        Returns:
            Address in Devanagari script
        """
        if not address:
            return ""
        
        # Handle common address patterns
        address_lower = address.lower()
        
        # Replace common patterns
        replacements = [
            ('ward no.', 'वडा नं.'),
            ('ward no', 'वडा नं'),
            ('ward', 'वडा'),
            ('municipality', 'नगरपालिका'),
            ('rural municipality', 'गाउँपालिका'),
            ('district', 'जिल्ला'),
            ('province', 'प्रदेश'),
            ('nepal', 'नेपाल'),
            ('road', 'मार्ग'),
            ('street', 'सडक'),
            ('house no.', 'घर नं.'),
            ('house no', 'घर नं'),
        ]
        
        for eng, nep in replacements:
            address_lower = address_lower.replace(eng.lower(), nep)
        
        # Now transliterate the rest
        words = address_lower.split()
        transliterated_words = []
        
        for word in words:
            # Skip if already in Nepali (from replacements)
            if any(nep_char in word for nep_char in ['व', 'न', 'ग', 'प', 'ज']):
                transliterated_words.append(word)
            elif word in self.dictionary:
                transliterated_words.append(self.dictionary[word])
            else:
                transliterated_words.append(self._transliterate_word(word))
        
        return " ".join(transliterated_words)
    
    def transliterate_number(self, number_text: str) -> str:
        """
        Convert English numbers to Nepali Devanagari numbers.
        
        Args:
            number_text: Number as text (e.g., "123", "ward 5")
            
        Returns:
            Number in Devanagari script
        """
        number_map = {
            '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
            '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
        }
        
        result = []
        for char in number_text:
            if char in number_map:
                result.append(number_map[char])
            else:
                result.append(char)
        
        return ''.join(result)
    
    def _transliterate_word(self, word: str) -> str:
        """Transliterate a single word character by character."""
        result = []
        i = 0
        
        while i < len(word):
            found = False
            
            # Try 2-character combinations first (like 'ch', 'th', etc.)
            if i + 2 <= len(word):
                two_chars = word[i:i+2].lower()
                if two_chars in self.CHAR_MAP:
                    result.append(self.CHAR_MAP[two_chars])
                    i += 2
                    found = True
            
            # Try 1-character
            if not found and i < len(word):
                one_char = word[i].lower()
                if one_char in self.CHAR_MAP:
                    result.append(self.CHAR_MAP[one_char])
                else:
                    result.append(word[i])  # Keep as is (punctuation, etc.)
                i += 1
        
        return ''.join(result)
    
    def transliterate_citizen_data(self, data_dict: dict) -> dict:
        """
        Transliterate a dictionary of citizen data.
        
        Args:
            data_dict: Dictionary containing citizen data with keys like:
                      'name', 'address', 'district', 'municipality', etc.
                      
        Returns:
            Dictionary with transliterated values
        """
        result = {}
        
        for key, value in data_dict.items():
            if not value or not isinstance(value, str):
                result[key] = value
                continue
            
            # Apply appropriate transliteration based on field type
            if key in ['name', 'first_name', 'last_name', 'father_name', 'mother_name']:
                result[key] = self.transliterate_name(value)
            elif key in ['address', 'permanent_address', 'temporary_address']:
                result[key] = self.transliterate_address(value)
            elif key in ['district', 'municipality', 'ward', 'province']:
                result[key] = self.transliterate_name(value)  # Place names
            elif any(num_term in key.lower() for num_term in ['number', 'no', 'id']):
                result[key] = self.transliterate_number(value)
            else:
                # Default transliteration
                result[key] = self.transliterate_name(value)
        
        return result