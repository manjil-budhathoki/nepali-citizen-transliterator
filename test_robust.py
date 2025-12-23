#!/usr/bin/env python3
"""
Test the robust transliterator
"""

from nepali_citizen_transliterator import CitizenTransliterator

def main():
    print("🧪 Testing Robust Nepali Transliterator")
    print("=" * 50)
    
    trans = CitizenTransliterator()
    
    # Test names that failed before
    test_names = [
        "Ram Sharma",
        "Hari Bahadur Thapa",
        "Manjil Budhathoki",
        "Gopal Prasad KC",
        "Sita Kumari Rai",
        "Shyam Kumar Gurung",
        "Bikash Adhikari",
        "Niraj Bhattarai",
    ]
    
    print("\n🔤 Name Transliteration:")
    print("-" * 30)
    for name in test_names:
        result = trans.transliterate_name(name)
        print(f"{name:25} → {result}")
    
    # Test addresses
    print("\n🏠 Address Transliteration:")
    print("-" * 30)
    addresses = [
        "Ward 5, Pokhara",
        "House No. 123, Kathmandu",
        "Tinkune, Kathmandu Municipality",
        "Biratnagar 12, Morang District",
    ]
    
    for addr in addresses:
        result = trans.transliterate_address(addr)
        print(f"{addr:40} → {result}")
    
    # Test numbers
    print("\n🔢 Number Conversion:")
    print("-" * 30)
    numbers = [
        "12345",
        "Ward 9, Phone: 9841234567",
        "Citizenship: 05-1234-56789",
    ]
    
    for num in numbers:
        result = trans.transliterate_number(num)
        print(f"{num:30} → {result}")
    
    # Test complete data
    print("\n📋 Complete Citizen Data:")
    print("-" * 30)
    citizen = {
        "name": "Hari Bahadur Thapa",
        "father_name": "Ram Bahadur Thapa",
        "address": "Ward 9, Pokhara Municipality, Kaski",
        "district": "Kaski",
        "citizenship_number": "32-12345-67890",
        "ward_number": "9"
    }
    
    result = trans.transliterate_citizen_data(citizen)
    for key, value in result.items():
        print(f"{key:20}: {value}")
    
    print("\n✅ Testing completed!")

if __name__ == "__main__":
    main()