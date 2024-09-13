import json
import os

root = '/home/esther/GitProjects/pubabsnlp'
json_annotate_folder = os.path.join(root, 'data', 'json_annotate')
allfolders = os.listdir(json_annotate_folder)

dict_entities = {
    'long-read sequencing':                     'TECHNIQUE',
    'pcr':                                      'TECHNIQUE',
    'microarray':                               'TECHNIQUE',
    'nanopore sequencing':                      'TECHNIQUE',
    'PharmGKB':                                 'DATABASE',
    'Gnomad':                                   'DATABASE',
    'dbSNP':                                    'DATABASE',
    'TCGA':                                     'DATABASE',
    '1000 Genomes Project':                     'DATABASE',
    'logistic regression':                      'ANALYTICAL_METHOD',
    'next generation sequencing':               'ANALYTICAL_METHOD',
    'machine learning':                         'ANALYTICAL_METHOD',
    'Hierarchical clustering':                  'ANALYTICAL_METHOD',
    'molecular dynamics':                       'ANALYTICAL_METHOD',
    'confidentiality':                          'CHALLENGE',
    'delivery':                                 'CHALLENGE',
    'rare variation':                           'CHALLENGE',
    'cost':                                     'CHALLENGE',
    'challenge':                                'CHALLENGE',
}

result = []

count = 0

for f in allfolders:
    print(f)
    ent = dict_entities[f]
    with open(os.path.join(json_annotate_folder, f, f+'.json'), 'r') as f:
        j = json.loads(f.read())
        for i in j:
            entities = []
            if 'label' not in i.keys():
                print(i['text'])
                continue
            for k, k1 in enumerate(i['label']):
                entities.append([[i['label'][k]['start'], i['label'][k]['end'], i['label'][k]['labels'][0]]][0])
            count += 1
            result.append(
                (
                    i['text'],
                    {'entities': entities}
                 )
            )
with open('results_annot_extra.txt', 'w') as f:
    f.write('\n'.join([
        "".join(json.dumps(x)[1:-1]) for x in result]
    ))

