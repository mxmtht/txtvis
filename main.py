import glob
import spacy
import networkx as nx
from pyvis.network import Network

nlp = spacy.load("nl_core_news_md")

pyvis_mode = True

# networkX things
G = nx.MultiDiGraph()

# coloring (only for pyvis)
color_mapping = {
    "NORP": "red",
    "LANGUAGE": "blue",
    "LOC": "green",
    "GPE": "pink",
    "ORG": "purple",
    "PERSON": "yellow",
    "EVENT": "brown",
    "FAC": "orange",
    "BOOKAUTHOR": "gray",
}

# entity label as category
categories = {}

# input texts
path = 'in/*.txt'

# Entity exclusion settings
excluded_labels = ['DATE', 'PERCENT', 'CARDINAL', 'ORDINAL', 'TIME', 'QUANTITY', 'WORK_OF_ART']
excluded_pos = ['ADJ', 'ADV', 'VERB']
excluded_lemmas = []


def author_to_entity_network(author, doc):
    author_lastname = "".join(author.split(" ")[-1:])
    print(f"### {author_lastname} ###")
    categories[author_lastname] = "BOOKAUTHOR"
    for entity in doc.ents:
        if entity.label_ not in excluded_labels \
                and doc[entity.start].pos_ not in excluded_pos \
                and entity.text not in excluded_lemmas \
                and len(entity.text) > 2 \
                and not entity.text.__contains__(']') \
                and not entity.text.__contains__('*') \
                and not entity.text.__contains__('\\'):
            print(entity.text, entity.label_, entity.ent_id, doc[entity.start].pos_)
            if entity.label_ == "PERSON":  # persons are identified by their last names
                ent_lastname = " ".join(entity.text.split(" ")[-1:])
                if ent_lastname != author_lastname:
                    G.add_edge(author_lastname, ent_lastname)
                    categories[entity.text] = entity.label_
            else:
                G.add_edge(author_lastname, entity.text)
                categories[entity.text] = entity.label_

def pyvis_network():
    # calculate node sizes (based on in_degrees)
    note_degrees = dict(G.degree)
    nx.set_node_attributes(G, note_degrees, 'size')

    # set category based on entity type
    nx.set_node_attributes(G, categories, 'category')

    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    net.force_atlas_2based(gravity=-300, spring_length=100, spring_strength=0.12, central_gravity=0.05, overlap=0.25)
    net.from_nx(G)
    for node in net.nodes:
        try:
            category = node['category']
        except:
            category = 'default'
        color = color_mapping.get(category, "gray")  # Default to gray if the category is not in the mapping
        node["color"] = color
    net.show("out/network.html", notebook=False)

if __name__ == "__main__":
    docs = {}
    for file in glob.glob(path):
        with open(file, encoding='utf-8', errors='ignore') as file_in:
            text = file_in.read()
            doc = nlp(text)
            author_to_entity_network(file[6:-4], doc)
    if pyvis_mode:
        pyvis_network()
    nx.write_gexf(G, "out/network.gexf")
