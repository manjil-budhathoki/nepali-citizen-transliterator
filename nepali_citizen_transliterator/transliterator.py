#!/usr/bin/env python3
"""
Nepali Citizen Transliterator - Improved Version
Handles Nepali names and addresses with proper Devanagari conversion.
"""

import re

class CitizenTransliterator:
    """Robust transliterator for Nepali citizen data."""
    
    # Vowel mappings (standalone and vowel signs)
    VOWELS = {
        'a': 'अ',    # Standalone
        'aa': 'आ',
        'i': 'इ',
        'ee': 'ई',
        'u': 'उ',
        'oo': 'ऊ',
        'e': 'ए',
        'ai': 'ऐ',
        'o': 'ओ',
        'au': 'औ',
    }
    
    # Vowel signs (when following a consonant)
    VOWEL_SIGNS = {
        'a': '',      # No sign for inherent 'a'
        'aa': 'ा',
        'i': 'ि',
        'ee': 'ी',
        'u': 'ु',
        'oo': 'ू',
        'e': 'े',
        'ai': 'ै',
        'o': 'ो',
        'au': 'ौ',
    }
    
    # Consonant mappings
    CONSONANTS = {
        'k': 'क', 'kh': 'ख', 'g': 'ग', 'gh': 'घ', 'ng': 'ङ',
        'ch': 'च', 'chh': 'छ', 'j': 'ज', 'jh': 'झ', 'ny': 'ञ',
        't': 'ट', 'th': 'ठ', 'd': 'ड', 'dh': 'ढ', 'n': 'ण',
        't': 'त', 'th': 'थ', 'd': 'द', 'dh': 'ध', 'n': 'न',
        'p': 'प', 'ph': 'फ', 'b': 'ब', 'bh': 'भ', 'm': 'म',
        'y': 'य', 'r': 'र', 'l': 'ल', 'w': 'व', 'v': 'व',
        'sh': 'श', 's': 'स', 'h': 'ह', 'ksh': 'क्ष', 'tr': 'त्र',
        'gy': 'ज्ञ', 'dr': 'द्र', 'pr': 'प्र', 'br': 'ब्र', 'gr': 'ग्र',
        'kr': 'क्र', 'tr': 'त्र', 'str': 'स्त्र', 'shr': 'श्र',
    }
    
    # Special character combinations
    SPECIAL = {
        'ri': 'ृ',    # ऋ sound
        'rr': 'ॄ',    # ॠ sound
        'lri': 'ॢ',   # ऌ sound
        'llri': 'ॣ',  # ॡ sound
        'om': 'ॐ',    # Om symbol
        ':': 'ः',     # Visarga
        '.': '।',     # Full stop
        '..': '॥',    # Double danda
    }
    
    # Comprehensive dictionary of common Nepali names
    COMMON_NAMES = {
        # Last names
        'sharma': 'शर्मा', 'poudel': 'पौडेल', 'bhattarai': 'भट्टराई',
        'kc': 'केसी', 'karki': 'कार्की', 'rai': 'राई', 'limbu': 'लिम्बू',
        'maharjan': 'महर्जन', 'tamang': 'तामाङ', 'thapa': 'थापा',
        'magar': 'मगर', 'gurung': 'गुरुङ', 'chhetri': 'क्षेत्री',
        'basnet': 'बस्नेत', 'shrestha': 'श्रेष्ठ', 'ghimire': 'घिमिरे',
        'adhikari': 'अधिकारी', 'khadka': 'खड्का', 'rana': 'राणा',
        'bhandari': 'भण्डारी', 'dahal': 'दाहाल', 'ojha': 'ओझा',
        'pandey': 'पाण्डे', 'bohora': 'बोहोरा', 'hamal': 'हमाल',
        'budhathoki': 'बुढाथोकी', 'basnyat': 'बस्न्यात', 'malla': 'मल्ल',
        'singh': 'सिंह', 'yadav': 'यादव', 'mandal': 'मण्डल',
        
        # First names
        'ram': 'राम', 'shyam': 'श्याम', 'hari': 'हरि', 'krishna': 'कृष्ण',
        'gopal': 'गोपाल', 'mohan': 'मोहन', 'sita': 'सीता', 'gita': 'गीता',
        'radha': 'राधा', 'laxmi': 'लक्ष्मी', 'saraswati': 'सरस्वती',
        'manjil': 'मञ्जिल', 'sujan': 'सुजन', 'sagar': 'सागर',
        'bikash': 'विकास', 'niraj': 'निरज', 'anil': 'अनिल', 'raj': 'राज',
        'arjun': 'अर्जुन', 'bhim': 'भीम', 'dipak': 'दीपक', 'gaurav': 'गौरव',
        'hari': 'हरि', 'ishwor': 'ईश्वर', 'janak': 'जनक', 'kiran': 'किरण',
        'lal': 'लाल', 'madan': 'मदन', 'narendra': 'नरेन्द्र', 'om': 'ओम्',
        'prakash': 'प्रकाश', 'ravi': 'रवि', 'santosh': 'सन्तोष', 'umesh': 'उमेश',
        
        # Titles and suffixes
        'kumar': 'कुमार', 'kumari': 'कुमारी', 'bahadur': 'बहादुर',
        'prasad': 'प्रसाद', 'devi': 'देवी', 'lal': 'लाल', 'jung': 'जुङ्ग',
        'man': 'मान', 'das': 'दास', 'nath': 'नाथ',
    }
    
    # Common place names
    COMMON_PLACES = {
        'kathmandu': 'काठमाडौं', 'pokhara': 'पोखरा', 'bhaktapur': 'भक्तपुर',
        'lalitpur': 'ललितपुर', 'biratnagar': 'विराटनगर', 'birgunj': 'बीरगञ्ज',
        'nepalgunj': 'नेपालगञ्ज', 'dharan': 'धरान', 'butwal': 'बुटवल',
        'hetauda': 'हेटौंडा', 'dhangadhi': 'धनगढी', 'tikapur': 'टीकापुर',
        'ilam': 'इलाम', 'jhapa': 'झापा', 'morang': 'मोरङ', 'sunsari': 'सुनसरी',
        'chitwan': 'चितवन', 'kaski': 'कास्की', 'kavre': 'काभ्रे', 'dhading': 'धादिङ',
        'nuwakot': 'नुवाकोट', 'tanahun': 'तनहुँ', 'syangja': 'स्याङ्ग्जा',
        'gorkha': 'गोरखा', 'lamjung': 'लमजुङ', 'manang': 'मनाङ', 'mustang': 'मुस्ताङ',
        'parbat': 'पर्वत', 'baglung': 'बागलुङ', 'myagdi': 'म्याग्दी',
        
        # Address terms
        'municipality': 'नगरपालिका', 'rural': 'गाउँपालिका', 'ward': 'वडा',
        'tole': 'टोल', 'sadak': 'सडक', 'ghar': 'घर', 'basti': 'बस्ती',
        'nagar': 'नगर', 'gaun': 'गाउँ', 'bazar': 'बजार', 'chowk': 'चोक',
        'toles': 'टोल्स', 'marga': 'मार्ग', 'path': 'पथ', 'line': 'लाइन',
    }
    
    def __init__(self):
        """Initialize the transliterator."""
        # Combine all dictionaries
        self.dictionary = {}
        self.dictionary.update(self.COMMON_NAMES)
        self.dictionary.update(self.COMMON_PLACES)
        
        # All possible mappings for transliteration
        self.all_mappings = {}
        self.all_mappings.update(self.VOWELS)
        self.all_mappings.update(self.CONSONANTS)
        self.all_mappings.update(self.SPECIAL)
        self.all_mappings.update(self.VOWEL_SIGNS)
    
    def transliterate_name(self, name: str) -> str:
        """
        Transliterate a Nepali name from Roman to Devanagari.
        
        Args:
            name: Romanized Nepali name
            
        Returns:
            Name in Devanagari script
        """
        if not name or not isinstance(name, str):
            return ""
        
        # Preserve original capitalization for initials
        name_parts = name.split()
        transliterated_parts = []
        
        for part in name_parts:
            part_lower = part.lower()
            
            # Check if entire part is in dictionary
            if part_lower in self.dictionary:
                nepali_part = self.dictionary[part_lower]
            else:
                # Apply intelligent transliteration
                nepali_part = self._transliterate_word_smart(part)
            
            transliterated_parts.append(nepali_part)
        
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
        
        # Handle common address patterns first
        address_lower = address.lower()
        
        # Special replacements for address components
        replacements = [
            ('ward no.', 'वडा नं.'),
            ('ward no', 'वडा नं'),
            ('ward', 'वडा'),
            ('house no.', 'घर नं.'),
            ('house no', 'घर नं'),
            ('house', 'घर'),
            ('municipality', 'नगरपालिका'),
            ('rural municipality', 'गाउँपालिका'),
            ('sub-metropolitan', 'उप-महानगरपालिका'),
            ('metropolitan', 'महानगरपालिका'),
            ('district', 'जिल्ला'),
            ('province', 'प्रदेश'),
            ('nepal', 'नेपाल'),
            ('road', 'मार्ग'),
            ('street', 'सडक'),
            ('avenue', 'एभेन्यु'),
            ('lane', 'गल्ली'),
            ('area', 'क्षेत्र'),
            ('zone', 'क्षेत्र'),
            ('block', 'ब्लक'),
            ('sector', 'सेक्टर'),
        ]
        
        for eng, nep in replacements:
            if eng in address_lower:
                address = address.replace(eng, nep)
                address_lower = address_lower.replace(eng, nep)
        
        # Now transliterate remaining parts
        words = address.split()
        transliterated_words = []
        
        for word in words:
            word_lower = word.lower()
            
            # Check if word is already in Nepali (from replacements)
            if any(nep_char in word for nep_char in ['व', 'न', 'ग', 'प', 'ज', 'ल', 'ा', 'ि', 'ी', 'ु', 'ू']):
                transliterated_words.append(word)
            elif word_lower in self.dictionary:
                transliterated_words.append(self.dictionary[word_lower])
            else:
                # Try to transliterate, but keep numbers and punctuation
                if word.replace('.', '').replace(',', '').isdigit():
                    # Convert numbers to Nepali
                    nepali_num = self._convert_numbers(word)
                    transliterated_words.append(nepali_num)
                elif self._looks_like_english_word(word):
                    transliterated_words.append(self._transliterate_word_smart(word))
                else:
                    transliterated_words.append(word)
        
        return " ".join(transliterated_words)
    
    def transliterate_number(self, text: str) -> str:
        """
        Convert English numbers in text to Nepali Devanagari numbers.
        
        Args:
            text: Text containing numbers
            
        Returns:
            Text with numbers converted to Devanagari
        """
        if not text:
            return ""
        
        # Convert all digits to Nepali
        number_map = {
            '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
            '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
        }
        
        result = []
        for char in text:
            if char in number_map:
                result.append(number_map[char])
            else:
                result.append(char)
        
        return ''.join(result)
    
    def transliterate_citizen_data(self, data_dict: dict) -> dict:
        """
        Transliterate a dictionary of citizen data.
        
        Args:
            data_dict: Dictionary containing citizen data
            
        Returns:
            Dictionary with transliterated values
        """
        result = {}
        
        for key, value in data_dict.items():
            if not value or not isinstance(value, str):
                result[key] = value
                continue
            
            # Apply appropriate transliteration based on field type
            if key in ['name', 'first_name', 'last_name', 'father_name', 
                      'mother_name', 'spouse_name', 'grandfather_name']:
                result[key] = self.transliterate_name(value)
            elif key in ['address', 'permanent_address', 'temporary_address',
                        'birth_place', 'office_address']:
                result[key] = self.transliterate_address(value)
            elif key in ['district', 'municipality', 'ward', 'province',
                        'vdc', 'tole', 'area', 'zone']:
                result[key] = self.transliterate_name(value)  # Place names
            elif any(num_term in key.lower() for num_term in ['number', 'no', 'id', 
                                                             'num', 'code']):
                result[key] = self.transliterate_number(value)
            else:
                # Default transliteration
                result[key] = self.transliterate_name(value)
        
        return result
    
    def _transliterate_word_smart(self, word: str) -> str:
        """Smart transliteration that handles Nepali phonetics better."""
        if not word:
            return ""
        
        word_lower = word.lower()
        result = []
        i = 0
        length = len(word_lower)
        
        while i < length:
            found = False
            
            # Try longest matches first (up to 4 chars)
            for match_len in range(4, 0, -1):
                if i + match_len <= length:
                    chunk = word_lower[i:i+match_len]
                    
                    # Check special combinations first
                    if chunk in self.SPECIAL:
                        result.append(self.SPECIAL[chunk])
                        i += match_len
                        found = True
                        break
                    
                    # Check consonant+vowel combinations
                    if match_len >= 2:
                        consonant = chunk[:-1]
                        vowel = chunk[-1]
                        
                        if consonant in self.CONSONANTS and vowel in self.VOWEL_SIGNS:
                            # Consonant with vowel sign
                            nepali_consonant = self.CONSONANTS[consonant]
                            nepali_vowel_sign = self.VOWEL_SIGNS[vowel]
                            result.append(nepali_consonant + nepali_vowel_sign)
                            i += match_len
                            found = True
                            break
                    
                    # Check standalone vowel
                    if chunk in self.VOWELS:
                        result.append(self.VOWELS[chunk])
                        i += match_len
                        found = True
                        break
                    
                    # Check standalone consonant
                    if chunk in self.CONSONANTS:
                        # Consonant with inherent 'a'
                        nepali_consonant = self.CONSONANTS[chunk]
                        result.append(nepali_consonant)
                        i += match_len
                        found = True
                        break
            
            # If no match found, keep the character as-is
            if not found:
                result.append(word[i] if i < len(word) else '')
                i += 1
        
        # Join and post-process
        nepali_word = ''.join(result)
        
        # Handle common patterns
        nepali_word = self._post_process(nepali_word)
        
        return nepali_word
    
    def _post_process(self, word: str) -> str:
        """Post-processing to fix common issues."""
        if not word:
            return word
        
        # Fix common transliteration errors
        corrections = [
            ('अा', 'आ'),    # Double vowel fix
            ('अि', 'इ'),
            ('अी', 'ई'),
            ('अु', 'उ'),
            ('अू', 'ऊ'),
            ('अे', 'ए'),
            ('अै', 'ऐ'),
            ('अो', 'ओ'),
            ('अौ', 'औ'),
            ('कअ', 'का'),   # Common consonant fixes
            ('खअ', 'खा'),
            ('गअ', 'गा'),
            ('घअ', 'घा'),
            ('चअ', 'चा'),
        ]
        
        for wrong, right in corrections:
            word = word.replace(wrong, right)
        
        return word
    
    def _convert_numbers(self, text: str) -> str:
        """Convert English numbers to Nepali numbers."""
        number_map = {
            '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
            '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
        }
        
        result = []
        for char in text:
            if char in number_map:
                result.append(number_map[char])
            else:
                result.append(char)
        
        return ''.join(result)
    
    def _looks_like_english_word(self, word: str) -> bool:
        """Check if word looks like an English word (not Nepali already)."""
        if not word:
            return False
        
        # Remove punctuation
        clean_word = re.sub(r'[^\w]', '', word)
        
        # If it's already in Devanagari, don't transliterate
        devanagari_range = '\u0900-\u097F'
        if re.search(f'[{devanagari_range}]', clean_word):
            return False
        
        # If it's mostly letters, it's probably English
        if re.match(r'^[A-Za-z]+$', clean_word):
            return True
        
        return False
    
    def add_custom_mapping(self, roman: str, nepali: str):
        """Add custom transliteration mapping."""
        if roman and nepali:
            self.dictionary[roman.lower()] = nepali
    
    def add_custom_mappings(self, mappings: dict):
        """Add multiple custom mappings."""
        for roman, nepali in mappings.items():
            self.add_custom_mapping(roman, nepali)