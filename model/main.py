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
import random
import spacy
import random
from spacy.util import minibatch, compounding
import re
from spacy.training import Example
import ast
import json
from spacy.training import offsets_to_biluo_tags


def run_training(train_data, iterations=50):

    nlp = spacy.load("en_ner_bionlp13cg_md")

    if "ner" not in nlp.pipe_names:
        raise ValueError("O modelo carregado não possui o componente NER.")
    ner = nlp.get_pipe("ner")

    entities = list(set([x[3] for x in train_data]))
    for e in entities:
        ner.add_label(e)

    examples = []
    for t in train_data:
        text = t[0]
        doc = nlp.make_doc(text)
        item = [[int(t[1]), int(t[2]), t[3]]]

        try:
            # Tenta verificar o alinhamento usando offsets_to_biluo_tags
            biluo_tags = offsets_to_biluo_tags(doc, item)
            # Se os offsets estiverem corretos, cria o exemplo
            example = Example.from_dict(doc, {"entities": biluo_tags})
            examples.append(example)
        except Exception as e:
            print(doc)

        example = Example.from_dict(doc, {"entities": item})
        examples.append(example)

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # apenas o 'ner' está habilitado
        optimizer = nlp.resume_training()
        for itn in range(iterations):  # número de iterações
            random.shuffle(examples)
            losses = {}
            batches = minibatch(examples, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                nlp.update(batch, drop=0.5, losses=losses)
            print(f"Iteration {itn}, Losses: {losses}")
    nlp.to_disk("pharmacogenetics_ner_model")


def validation(validation_data):
    nlp = spacy.load("../model/pharmacogenetics_ner_model")

    # binning entities
    bins = {}
    for v in validation_data:
        if v[3] not in bins.keys():
            bins[v[3]] = []
        bins[v[3]].append(v)

    fullresult = ''
    for k, validation_data in bins.items():
        validation_examples= []
        for v in validation_data:
            text = v[0]
            item = [[int(v[1]), int(v[2]), v[3]]]
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, {"entities": item})
            validation_examples.append(example)
        scores = nlp.evaluate(validation_examples)
        result_str = f'{v[3]}\nPrecision: {scores["ents_p"]}\nRecall: {scores["ents_r"]}\nF1-score: {scores["ents_f"]}\n\n'
        fullresult += result_str
    return fullresult


def shuffle(fd):
    by_key = {}
    for item in fd:
        entity = item[3]
        if entity not in by_key.keys():
            by_key[entity] = []
        by_key[entity].append(item)
    test = []
    train = []
    for k, v in by_key.items():
        cut = int(0.2 * len(v))
        test.extend(v[:cut])
        train.extend(v[cut:])
    return test, train


if __name__ == '__main__':
    with open('./raw_input_v4.csv', 'r') as f:
        fulldata = [x.rstrip('\n').split('\t') for x in f.readlines()]

    with open('quality_metrics', 'w') as f:

        for i in range(1):
            # while shuffling take care if the instances are balanced
            test_data, train_data = shuffle(fulldata)

            run_training(train_data, iterations=30)
            select = ['TECHNIQUE', 'ANALYTICAL_METHOD', 'DATABASE', 'CHALLENGE']
            filter_seleted = [x for x in test_data if x[3] in select]

            f.write(validation(filter_seleted))
            f.flush()
