"""
building model ab-initio
"""

import spacy
from spacy.util import minibatch, compounding
import random
import json
from spacy.training import offsets_to_biluo_tags
import re
from spacy.training import Example

# Inicialize um novo objeto Language para o inglês
nlp = spacy.blank("en")  # Cria um pipeline vazio para o inglês
ner = nlp.add_pipe("ner")


def load_data_from_txt(file_path):
    result = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for li in lines:
        row = li.rstrip("\n").split('||')
        text = row[0]
        word = row[1]
        for m in re.finditer(word, text):
            g, s, e = m.group(), m.start(), m.end()
            result.append((text, {"entities": [[s, e, row[2]]]}))
            break
    return result


TRAIN_DATA = load_data_from_txt('./raw_input.txt')

for _, annotations in TRAIN_DATA:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

optimizer = nlp.begin_training()

for i in range(100):  # Número de iterações
    losses = {}
    batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
    for batch in batches:
        examples = []
        for text, annotations in batch:
            doc = nlp.make_doc(text)
            biluo_tags = offsets_to_biluo_tags(doc, annotations['entities'])
            example = Example.from_dict(doc, annotations)
            examples.append(example)
        nlp.update(examples, drop=0.3, losses=losses)
    print(f"Losses at iteration {i}: {losses}")

# Salve o modelo treinado
nlp.to_disk("pharmacogenetics_ner_model")
