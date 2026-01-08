import re
import unicodedata

class TextPreprocessor:
    def clean_text(text: str) -> str:
        """
        Preserves numbers, structure, and stopwords.
        """
    
        # Normalize Unicode 
        text = unicodedata.normalize("NFKC", text)
    
        # Lowercase (transformers are usually case-insensitive)
        text = text.lower()
    
        # Remove URLs (causes noise)
        text = re.sub(r"https?://\S+|www\.\S+", "", text)
    
        # Handle Hyphens 
        text = text.replace("-", " ")
        # We remove punctuation
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        # remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text