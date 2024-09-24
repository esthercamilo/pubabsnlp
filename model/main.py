"""
Entities already available in en_ner_bionlp13cg_md:
AMINO_ACID
ANATOMICAL_SYSTEM
CANCER
CELL
CELLULAR_COMPONENT
GENE_OR_GENE_PRODUCT
IMMATERIAL_ANATOMICAL_ENTITY
MULTI_TISSUE_STRUCTURE
ORGAN
ORGANISM
ORGANISM_SUBDIVISION
ORGANISM_SUBSTANCE
PATHOLOGICAL_FORMATION
SIMPLE_CHEMICAL
TECHNIQUE
TISSUE

New entities specific for this study
TECHNIQUE
ANALYTICAL_METHOD
DATABASE
CHALLENGE

"""
import os
import random
import spacy
from spacy.training import Example
from spacy.training import offsets_to_biluo_tags
from spacy.util import minibatch, compounding


def validation(validation_data, root, iteration=0):

    nlp = spacy.load(os.path.join(root, "model", "pharmacogenetics_ner_model"))

    # binning entities
    bins = {}
    for v in validation_data:
        if v[3] not in bins.keys():
            bins[v[3]] = []
        bins[v[3]].append(v)

    fullresult = ''
    misclassified_examples = []
    for k, validation_data in bins.items():
        validation_examples = []
        for v in validation_data:
            text = v[0]
            item = [[int(v[1]), int(v[2]), v[3]]]
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, {"entities": item})
            validation_examples.append(example)

        scores = nlp.evaluate(validation_examples)
        result_str = f'{v[3]}\nPrecision: {scores["ents_p"]}\nRecall: {scores["ents_r"]}\nF1-score: {scores["ents_f"]}\n\n'
        fullresult += result_str

        # Check for misclassified examples
        for example in validation_data:
            d = nlp(example[0])
            target_entity = (example[0][int(example[1]):int(example[2])], example[3])
            possible_entities = [(x.text, x.label_) for x in d.ents]
            if possible_entities and target_entity not in possible_entities and len(possible_entities) <= 1:
                misclassified_examples.append([example[0], target_entity[0], target_entity[1], possible_entities[0][0]])

    os.makedirs(os.path.join(root, 'model', 'qualities'), exist_ok=True)
    with open(os.path.join(root, 'model', 'qualities', f'quality_metrics{iteration}.txt'), 'w') as fq:
        fq.write(fullresult)

    with open(os.path.join(root, 'model', 'qualities', 'missclassified.csv'), 'w') as fo:
        mstr = '\n'.join(['\t'.join(x) for x in misclassified_examples])
        fo.write(mstr)

    return fullresult


def run_training(td, train_data, root, iterations=50, min_char_length=10):

    nlp = spacy.load("en_ner_bionlp13cg_md")

    if "ner" not in nlp.pipe_names:
        raise ValueError("O modelo carregado não possui o componente NER.")
    ner = nlp.get_pipe("ner")

    present_labels = ner.labels
    for e in set([x[3] for x in td]):
        if e not in present_labels:
            ner.add_label(e)

    examples = []
    for t in train_data:
        text = t[0]
        doc = nlp.make_doc(text)
        item = [[int(t[1]), int(t[2]), t[3]]]
        try:
            # Tenta verificar o alinhamento usando offsets_to_biluo_tags
            biluo_tags = offsets_to_biluo_tags(doc, item)
            # Se os offsets estiverem corretos e a entidade tiver o comprimento mínimo, cria o exemplo
            if len(doc[item[0][0]:item[0][1]].text) >= min_char_length:
                example = Example.from_dict(doc, {"entities": biluo_tags})
                examples.append(example)
        except Exception as e:
            print(str(e)[0:1], doc)

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
    nlp.to_disk(os.path.join(root, "model", "pharmacogenetics_ner_model"))


def shuffle(fd, root, force=False):

    os.makedirs(os.path.join(root, 'model', 'sets'), exist_ok=True)

    path_train = os.path.join(root, 'model', 'sets', 'train.data')
    path_test = os.path.join(root, 'model', 'sets', 'test.data')

    istrain = os.path.isfile(path_train) and os.path.getsize(path_train) > 0
    istest = os.path.isfile(path_test) and os.path.getsize(path_test) > 0

    if istrain and istest and not force:
        with open(path_train, 'r') as f2:
            train = [x.rstrip('\n').split('\t') for x in f2.readlines()]
        with open(path_test, 'r') as f3:
            test = [x.rstrip('\n').split('\t') for x in f3.readlines()]
    else:
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

        # Save test and train
        with open(path_test, 'w') as f0:
            f0.write('\n'.join(['\t'.join(x) for x in test]))
        with open(path_train, 'w') as f1:
            f1.write('\n'.join(['\t'.join(x) for x in train]))
    return test, train


def run(root):
    # Read data
    with open(os.path.join(root, 'model', 'fulltraining.tsv'), 'r') as f:
        fulldata = [x.rstrip('\n').split('\t') for x in f.readlines()]

    for i in range(1):
        test_data, train_data = shuffle(fulldata, root, force=True)
        run_training(train_data, test_data, root, iterations=30)
        validation(test_data, root, iteration=i)