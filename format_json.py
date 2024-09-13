import json
import os
import shutil

root = os.getcwd()

def seek_word(word, number_examples=100):
    # Select abstracts with known terms, for example, ngs, microarray or machine learning
    files = os.listdir('./data/review_removed')
    foldername = word.strip()
    os.makedirs(f'data/json_annotate/{foldername}', exist_ok=True)
    os.makedirs(f'data/json_test/{foldername}', exist_ok=True)
    i = 0
    for f in files:
        path = os.path.join(root, 'results', f)
        with open(path, 'r') as t:
            count = 0
            lines = t.read().split('\n')
            abst = lines[2]
            phrases = [x for x in abst.split('.') if x]
            for phr in phrases:
                if word.lower() in phr.lower():
                    newname = f.replace('.txt', f'_{count}.json')
                    count += 1
                    i += 1
                    data = json.dumps({"data": {"text": phr}}, indent=4)
                    # Dividir entre conjunto de treino e teste 75/25
                    if i % 4 != 0:
                        with open(f'data/json_annotate/{foldername}/{newname}', 'w') as fj:
                            fj.write(data)
                    else:
                        with open(f'data/json_test/{foldername}/{newname}', 'w') as fj:
                            fj.write(data)
        if i > number_examples:
            break

seed_terms = ['next generation sequencing', 'microarray', 'pcr', 'nanopore sequencing', 'long-read sequencing',
              'machine learning', 'logistic regression', 'molecular dynamics', 'Hierarchical clustering',
              '1000 Genomes Project', 'PharmGKB', 'TCGA', 'Gnomad', 'dbSNP',
              'cost', 'delivery', 'confidentiality', 'rare variation', 'challenge']
for t in seed_terms:
    seek_word(t)

def exclude_review():
    files = os.listdir('./results')
    for f in files:
        path = os.path.join(root, 'results', f)
        with open(path, 'r') as t:
            text = t.read()
            if 'review' in text.lower():
                continue
            else:
                shutil.copy(path, path.replace('results', 'data/review_removed'))

# exclude_review()
