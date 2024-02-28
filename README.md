# txtvis
A simple python script that takes raw text input, extracts entities using spaCy NER and draws a network based on the input content.
This version of the script only works with Dutch input text.

## Setup

After cloning into the repository, first install the required packages into a virtual environment.
```
cd to/this/repo/
mkdir out
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Now go ahead and add some source material to the `in` directory.
The naming convention for the input texts is as follows:
```
John Doe.txt
<First Name> <Last Name>.txt
```
You are ready to generate network data.

## Generate network data

Do not forget to remove the example data from the `in/` directory.
To execute the script run the following command:
```
python3 main.py
```
This will generate a `.gexf` file in the `out` directory, which can be edited with [Gephi](https://gephi.org).
Do not forget to look into the main.py source code file to check for options, like generating a pyvis-html-file for interactive exploration of your network data.

## Handy stuff

Some nice things, that can help you debug and understand what is happening.

### Display the entities in a text
Open a python console with in this venv `source venv/bin/activate` and then `python`.

```
import spacy
from spacy import displacy
nlp = spacy.load("nl_core_news_md")
doc = nlp(open('in/Pietertje Janssen.txt').read())
displacy.serve(doc, style='ent', port=5002, host='127.0.0.1')
```