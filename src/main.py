import spacy

def recognize_entities(text):
    # Load SpaCy English model
    nlp = spacy.load("en_core_web_sm")

    # Process the text using SpaCy
    doc = nlp(text)

    # Extract named entities and their labels
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return entities

def anonymize_entities(text, entities):
    # Replace recognized entities with generic names
    anonymized_text = text
    idx = 0
    for entity, label in entities:
        if label == "PERSON":
            # Replace with a generic name like "Person A"
            anonymized_text = anonymized_text.replace(entity, f"Person {chr(ord('A')+idx)}")
            idx+=1
    
    return anonymized_text

# Example text
law_article = """
In a landmark case, John Doe was accused of financial fraud. 
The plaintiff, Jane Smith, filed a lawsuit against XYZ Corporation.
"""

# Recognize entities in the example text
recognized_entities = recognize_entities(law_article)

# Display the recognized entities and their labels
for entity, label in recognized_entities:
    print(f"Entity: {entity}, Label: {label}")

