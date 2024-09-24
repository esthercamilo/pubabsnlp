"""
Create examples from NCBI results folder based on static_terms.csv list of terms.
Também são gerados exemplos a partir do modelo base.

"""
import re
import os
import spacy


def seek(filename, static_list, root):
    """
    Seek terms in files from ncbi
    """
    folder_result = os.path.join(root, 'results')
    with open(os.path.join(folder_result, filename)) as f:
        fulltext = f.read().split('\n')[-1]
    result = []
    for st in static_list:
        pattern = rf"\b{st[0]}\b"
        complement = st[2].split(';')
        case = bool(int(st[3]))
        fulltexts = fulltext.split('.')
        for text in fulltexts:
            text = text.strip()
            # if text is too short, or too long, skip
            if len(text.split(' ')) < 3 or len(text.split(' ')) > 2000:
                continue
            if any([x.lower() in text.lower() for x in complement]):
                if not case:
                    found = re.search(pattern, text)
                else:
                    found = re.search(pattern, text, re.IGNORECASE)
                if found:
                    start = text.lower().index(st[0].lower())  # ignore case
                    end = start + len(st[0])
                    result.append([text, str(start), str(end), st[1], st[0]])
                    print(st[0], st[1])
    return result


def generate_article_examples(debug, root):
    """
    Generate examples for the four entities: CHALLENGE, TECHNIQUE, ANALYSIS AND DATABASE.
    Save in the file fullsamples.csv
    """
    modelfolder = os.path.join(root, 'model')
    folder_result = os.path.join(root, 'results')
    with open(os.path.join(modelfolder, 'static_terms.csv')) as f:
        f.readline()
        static = [x.rstrip('\n').split(',') for x in f.readlines()]

    count = 0
    with open(os.path.join(modelfolder, 'fullsamples.tsv'), 'w') as f:
        files = os.listdir(folder_result)
        for fls in files:
            partial_result = seek(fls, static, root)
            if len(partial_result) > 0:
                for p in partial_result:
                    f.write('\t'.join(p) + '\n')
                    count += 1
                    f.flush()
            if debug and count > 2:
                break


def generate_examples_from_base_model(debug, root):
    """
    Create examples from model base by applying the model in abstracted downloaded from NCBI
    file: training_bionlp13cg.tsv
    """
    nlp = spacy.load("en_ner_bionlp13cg_md")
    folder_results = os.path.join(root, 'results')
    folder_model = os.path.join(root, 'model')
    allfiles = os.listdir(folder_results)

    count = 0
    with open(os.path.join(folder_model, 'training_bionlp13cg.tsv'), 'w') as fo:
        for filename in allfiles:
            with open(os.path.join(folder_results, filename)) as f:
                text = f.read().split('\n')[-1]
            doc = nlp(text)
            for ent in doc.ents:
                partial_result = [doc.text, str(ent.start_char), str(ent.end_char), ent.label_, ent.text]
                fo.write('\t'.join(partial_result) + '\n')
                count += 1
                fo.flush()
            if debug and count > 2:
                break


def run(debug, root):
    generate_article_examples(debug, root)
    generate_examples_from_base_model(debug, root)


