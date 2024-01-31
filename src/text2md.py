import os

import markdown
from bs4 import BeautifulSoup


def convert_markdown_to_text_and_save(file_path):
    try:
        # Generate the output text file path
        output_file_path = os.path.splitext(file_path)[0] + "_converted.txt"

        with open(file_path, "r", encoding="utf-8") as file:
            # Read the Markdown content from the file
            markdown_content = file.read()

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


# Example usage:
markdown_file_path = "./ccass/021018_1682318_1_CC.md"
output_file_path = convert_markdown_to_text_and_save(markdown_file_path)

if output_file_path is not None:
    print(f"Conversion successful. Converted text saved to: {output_file_path}")
