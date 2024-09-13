import json
import os
import spacy

nlp = spacy.load("model/pharmacogenetics_ner_model")
original_ner = nlp.get_pipe("ner")
print("Rótulos do modelo original:", original_ner.labels)

texts = []
allfiles = os.listdir('results')
for i in range(len(allfiles)):
    with open(os.path.join('results', allfiles[i]), "r") as f:
        abstract = [x for x in f.readlines() if x][-1]
        texts.append(abstract)


docs = [nlp(text) for text in texts]

results = {}

for text in texts:
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ not in results.keys():
            results[ent.label_] = []
        results[ent.label_].append((ent.text, ent.doc.text))

with open('output.json', 'w') as f:
    f.write(json.dumps(results, indent=4))


