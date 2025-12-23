from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nepali-citizen-transliterator",
    version="1.0.0",
    author="theFoolishOne",
    author_email="manjilbbudhathoki@gmail.com",
    description="Specialized transliterator for Nepali citizen documents (names, addresses, IDs)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manjil-budhathoki/nepali-citizen-transliterator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Intended Audience :: Government",
        "Intended Audience :: Information Technology",
    ],
    python_requires=">=3.6",
    keywords="nepali, devanagari, transliteration, citizen, document, name, address",
    install_requires=[],
)