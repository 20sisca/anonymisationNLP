import os
import sys

import markdown
import spacy
from bs4 import BeautifulSoup
from IPython.display import HTML, display
from spacy import displacy

# Load the trained model from the saved directory


def convert_markdown_to_text_and_save(file_path):
    try:
        # Generate the output text file path
        output_file_path = os.path.splitext(file_path)[0] + "_converted.txt"

        with open(file_path, "r", encoding="utf-8") as file:
            # Read the Markdown content from the file
            markdown_content = file.read()

            # print(markdown_content, "NNNNNNNNNNNNNN")
            # Convert Markdown to plain text
            html_content = markdown.markdown(markdown_content)
            text_content = "".join(
                BeautifulSoup(html_content, "html.parser").findAll(text=True)
            )

            # Write the converted text to a new text file
            with open(output_file_path, "w", encoding="utf-8") as output_file:
                output_file.write(text_content)

            return text_content

    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    text_path_md = sys.argv[1]
    text = convert_markdown_to_text_and_save(text_path_md)

    # print(text)
    nlp = spacy.load("./src/model")

    # Process the new text with the loaded model
    doc = nlp(text)

    # html = displacy.render(doc, style="dep")
    # # Extract and print named entities from the processed text
    # display(HTML(html))
    #
    # # Write HTML content to a new file
    # html_file_path = "output.html"
    # with open(html_file_path, "w", encoding="utf-8") as html_file:
    #     html_file.write(html)
    #
    # # Open the HTML file using a script (e.g., web browser)
    # import webbrowser
    #
    # webbrowser.open(html_file_path)
    print(text)
    for ent in doc.ents:
        print(f"Entity: {ent.text}, Label: {ent.label_}")
