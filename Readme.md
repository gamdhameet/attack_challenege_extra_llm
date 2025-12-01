# Install dependencies
pip install -r requirements.txt

# Get free Gemini API key from: https://makersuite.google.com/app/apikey

# Run with 3 variations per block (default)
python malware_generator.py --api-key YOUR_GEMINI_KEY

# Or with more variations for more polymorphism
python malware_generator.py --api-key YOUR_GEMINI_KEY --variations 5