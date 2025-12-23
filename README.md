# Nepali Citizen Transliterator

A Python library for converting Romanized Nepali names and addresses to Devanagari script. Made specifically for processing Nepali citizen data like names, addresses, and document information.

## What This Package Actually Does

This is version 1.0 - a **basic starting point**. It can:

1. **Convert English/Roman Nepali names to Devanagari**  
   Example: "Ram Bahadur Shrestha" → "राम बहादुर श्रेष्ठ"

2. **Convert addresses with common Nepali place names**  
   Example: "Kathmandu Municipality" → "काठमाडौं नगरपालिका"

3. **Convert English numbers to Nepali numbers**  
   Example: "Ward 5" → "वडा ५"

4. **Process complete citizen data dictionaries**  
   Takes data like `{"name": "Hari Sharma", "address": "..."}` and converts all fields

## What's NOT Included (Yet)

- **No reverse conversion** (Nepali to Roman) - only one-way
- **No complex rules** - simple character mapping only
- **No your JSON data** - uses only basic built-in dictionary
- **No advanced features** - kept minimal for first version

## Installation

```bash
pip install nepali-citizen-transliterator
```

## Basic Usage

```python
from nepali_citizen_transliterator import CitizenTransliterator

# Initialize
trans = CitizenTransliterator()

# Convert a name
nepali_name = trans.transliterate_name("Sita Kumari Rai")
print(nepali_name)  # सीता कुमारी राई

# Convert an address
address = trans.transliterate_address("Ward 9, Pokhara")
print(address)  # वडा ९, पोखरा

# Process citizen data
data = {
    "name": "Gopal Sharma",
    "district": "Kathmandu",
    "citizenship_no": "05-12345"
}
result = trans.transliterate_citizen_data(data)
# {'name': 'गोपाल शर्मा', 'district': 'काठमाडौं', 'citizenship_no': '०५-१२३४५'}
```

## What's Really in the Box

This package has:
- **Basic character mappings** (a→अ, k→क, etc.)
- **~50 common Nepali names** (Ram, Shyam, Sita, Gopal, etc.)
- **~30 common place names** (Kathmandu, Pokhara, districts)
- **Address terms** (Ward, Municipality, Tole, etc.)
- **Number conversion** (0-9 to ०-९)

## This is a Starting Point

I'm publishing this as version 1 to:
1. Get the package structure working
2. Test PyPI publishing process
3. Have a base to build upon
4. Get feedback from actual use

## Next Steps (Your Suggestions Needed)

I plan to improve this by:
1. **Adding your JSON data** - to make it actually useful
2. **Improving accuracy** - better rules and patterns
3. **Adding reverse conversion** - Nepali to Roman
4. **More validation** - better data checking

## Help Me Make It Better

Since this is my first package, I'd appreciate:
- What features do you actually need?
- What data should I prioritize adding?
- How should I handle edge cases?
- Any bugs or issues you find?

## Simple Enough?

This package is intentionally minimal. Install it, try it, and tell me what's missing or what should change.

---
*Note: This is version 1.0 - basic functionality to start with. Expect improvements based on real usage.*