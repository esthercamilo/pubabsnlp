import json
import os
import spacy


def run(root):
    nlp = spacy.load(os.path.join(root, 'model', "pharmacogenetics_ner_model"))
    original_ner = nlp.get_pipe("ner")
    print("Rótulos do modelo original:", original_ner.labels)

    texts = []
    res_folder = os.path.join(root, 'results')
    allfiles = os.listdir(res_folder)
    print(len(allfiles))
    for i in range(len(allfiles)):
        with open(os.path.join(res_folder, allfiles[i]), "r") as f:
            abstract = [x for x in f.readlines() if x][-1]
            texts.append(abstract)

    results = {}

    for text in texts:
        doc = nlp(text)

        for ent in doc.ents:
            if ent.label_ not in results.keys():
                results[ent.label_] = []
            results[ent.label_].append((ent.text, ent.doc.text))

    with open(os.path.join(res_folder, 'output.json'), 'w') as f:
        f.write(json.dumps(results, indent=4))


