# anonymisationNLP
Academic law project to anonymise names in law texts

pip install -r requirements.txt

python src/main.py

You also need to get the law texts and put them in a new directory 'data' in root.


Model precision: 

 'ents_per_type': {'PROTAGONISTS': {'p': 0.983739837398374,
   'r': 0.9499509322865555,
   'f': 0.9665501747378932}},


Instructions to get all the names to anonymise in a text from the model:

    Retrieve the text to process and put it in root

    python3 src/test_model.py <path_of_text.md>
