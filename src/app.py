import spacy
from flask import Flask, jsonify, request
from flask_cors import CORS  # Import the CORS module

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in the app

# Define an endpoint that takes heavy text as an argument using POST


@app.route("/process_text", methods=["POST"])
def process_text():
    text = request.get_data(as_text=True)
    # print(text)
    nlp = spacy.load("./src/model")

    # Process the new text with the loaded model
    doc = nlp(text)
    ents = set()
    for ent in doc.ents:
        ents.add(ent.text)
        print(f"Entity: {ent.text}, Label: {ent.label_}")
    return jsonify(result=list(ents))


@app.route("/")
def hello_world():
    return jsonify(message="Hello, World!")


if __name__ == "__main__":
    app.run(debug=True)
