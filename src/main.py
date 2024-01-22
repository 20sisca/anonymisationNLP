import spacy
from bs4 import BeautifulSoup
import markdown2

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    return markdown_content

def extract_text_from_markdown(markdown_content):
    html_content = markdown2.markdown(markdown_content)
    
    # If you have more complex Markdown content, you may need to extract text differently
    # This is a simple example that removes HTML tags
    text_content = ''.join(BeautifulSoup(html_content, 'html.parser').findAll(text=True))
    
    return text_content

markdown_file_path = 'data/021018_1682318_1_CC.md'
markdown_content = read_markdown_file(markdown_file_path)
text_content = extract_text_from_markdown(markdown_content)
def merge_compound_names(entities):
    # Merge consecutive entities with the same label
    merged_entities = []
    current_entity = None

    for entity, label in entities:
        if current_entity is None:
            current_entity = (entity, label)
        elif label == current_entity[1]:
            current_entity = (f"{current_entity[0]} {entity}", label)
        else:
            merged_entities.append(current_entity)
            current_entity = (entity, label)

    if current_entity is not None:
        merged_entities.append(current_entity)

    return merged_entities

def recognize_entities_and_pronouns(text):
    # Load SpaCy French model
    nlp = spacy.load("fr_core_news_sm")

    # Process the text using SpaCy
    doc = nlp(text)

    # Extract named entities, their labels, and pronouns
    entities_and_pronouns = []
    for token in doc:
        if token.ent_type_:
            entities_and_pronouns.append((token.text, token.ent_type_))
        elif token.pos_ == "PRON":
            entities_and_pronouns.append((token.text, "PRON"))

    # Merge consecutive entities with the same label
    entities_and_pronouns = merge_compound_names(entities_and_pronouns)

    return entities_and_pronouns

def anonymize_entities_and_pronouns(text, entities_and_pronouns):
    # Dictionary to store mappings from names to letters
    name_to_letter = {}

    # Replace recognized entities with letters and handle pronouns
    anonymized_text = text
    for entity, label in entities_and_pronouns:
        if label == "PER" and entity not in name_to_letter:
            # Generate a new letter for the person
            letter = chr(ord('A') + len(name_to_letter))
            name_to_letter[entity] = letter

        if label == "PER":
            # Replace with the assigned letter
            anonymized_text = anonymized_text.replace(entity, name_to_letter[entity])
        elif label == "PRON":
            # Replace with neutral pronouns
            anonymized_text = anonymized_text.replace(entity, "they")

    return anonymized_text

# Example text (in French)
law_article = """
Dans une affaire majeure, M. Michel Denemar a été accusé de fraude financière.
La demanderesse, Mme Sophie Fonsec, a intenté un procès contre la société XYZ.
M. Jean-Pierre Rognon, époux de Foix, est également impliqué dans l'affaire.
"""

# Recognize entities and pronouns in the example text
entities_and_pronouns = recognize_entities_and_pronouns(text_content)
print(entities_and_pronouns)
# Anonymize entities and pronouns in the text
anonymized_text = anonymize_entities_and_pronouns(text_content, entities_and_pronouns)

# Display the anonymized text
print(anonymized_text)

