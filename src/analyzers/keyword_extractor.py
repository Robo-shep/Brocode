import spacy

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
    
    return keywords

# Example usage
if __name__ == "__main__":
    text = "Apple is a technology company."
    keywords = extract_keywords(text)
    print(keywords)
