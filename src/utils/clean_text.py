import re

def clean_text(text):
    """
    Cleans and preprocesses text from any type of document to make it more structured.
    """
    #replacing multiple spaces/newlines with a single space
    text = re.sub(r"\s+", " ", text)  
    text = re.sub(r"\n\s*\n", "\n", text.strip())  
    #Fix broken words (e.g., "i n v o i c e" -> "invoice")
    text = re.sub(r"(?<!\w)\b(\w(?:\s\w)+)\b", lambda m: m.group(0).replace(" ", ""), text)
    #Removal special characters
    text = re.sub(r"[^\w\s.,:/-]", "", text)  # Keep alphanumeric, spaces, and basic punctuation

    return text.strip()