"""
Entities already available in en_ner_bionlp13cg_md:
AMINO_ACID
ANATOMICAL_SYSTEM
CANCER
CELL
CELLULAR_COMPONENT
DEVELOPING_ANATOMICAL_STRUCTURE
GENE_OR_GENE_PRODUCT
IMMATERIAL_ANATOMICAL_ENTITY
MULTI_TISSUE_STRUCTURE
ORGAN
ORGANISM
ORGANISM_SUBDIVISION
ORGANISM_SUBSTANCE
PATHOLOGICAL_FORMATION
SIMPLE_CHEMICAL
TISSUE

New entities specific for this study
TECHNIQUE
ANALYTICAL_METHOD
DATABASE
CHALLENGE


"""

import spacy
import random
from spacy.util import minibatch, compounding
import json
import re
from spacy.training import Example


def load_data_from_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        _train_data = [json.loads(line) for line in lines]
    return _train_data


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
            result.append({"text": text, "entities": [[s, e, row[2]]]})
            break  # only the first
    return result


train_data = load_data_from_txt('./raw_input.txt')

nlp = spacy.load("en_ner_bionlp13cg_md")

if "ner" not in nlp.pipe_names:
    raise ValueError("O modelo carregado não possui o componente NER.")
ner = nlp.get_pipe("ner")

for item in train_data:
    for ent in item['entities']:
        ner.add_label(ent[2])

examples = []
for item in train_data:
    doc = nlp.make_doc(item['text'])
    example = Example.from_dict(doc, {"entities": item['entities']})
    examples.append(example)

other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):  # apenas o 'ner' está habilitado
    optimizer = nlp.resume_training()
    for itn in range(50):  # ajuste o número de iterações conforme necessário
        random.shuffle(examples)
        losses = {}
        batches = minibatch(examples, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            nlp.update(batch, drop=0.5, losses=losses)
        print(f"Iteration {itn}, Losses: {losses}")

# Dados de validação
# validation_data = load_data('./test_data.jsonl')
#
# validation_examples = []
# for item in validation_data:
#     doc = nlp.make_doc(item['text'])
#     example = Example.from_dict(doc, {"entities": item['entities']})
#     validation_examples.append(example)
#
# # Avaliar o modelo
# scores = nlp.evaluate(validation_examples)
#
# # Imprimir as métricas
# print("Precision:", scores["ents_p"])
# print("Recall:", scores["ents_r"])
# print("F1-score:", scores["ents_f"])


nlp.to_disk("pharmacogenetics_ner_model")
