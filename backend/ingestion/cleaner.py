import re
import unicodedata

class TextCleaner:
    """
    Cleans and normalizes extracted text before chunking.
    """
    
    @staticmethod
    def clean(text: str) -> str:
        if not text:
            return ""
            
        # 1. Normalize unicode characters
        text = unicodedata.normalize('NFKC', text)
        
        # 2. Replace null bytes and non-printable control characters (except newlines/tabs)
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # 3. Replace multiple spaces/tabs with single space (preserve newlines)
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            # Collapse multiple inline spaces
            cleaned_line = re.sub(r'[ \t]+', ' ', line).strip()
            cleaned_lines.append(cleaned_line)
            
        # 4. Collapse 3+ consecutive newlines into double newlines
        cleaned_text = "\n".join(cleaned_lines)
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
        
        return cleaned_text.strip()
