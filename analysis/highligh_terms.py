import os
import json


def run(root):

    with open(os.path.join(root, 'model', 'static_terms.csv'), 'r') as r:
        static = [x.lower().split(',')[0] for x in r.readlines()]

    with open(os.path.join(root, 'analysis', 'output.json'), 'r') as r:
        data = json.loads(r.read())

    new_terms = {}
    entities = ['TECHNIQUE', 'ANALYTICAL_METHOD', 'DATABASE', 'CHALLENGE']
    for e in entities:
        terms = data.get(e)
        normalized_terms = [[item.lower() for item in sublist] for sublist in terms]
        if e not in new_terms.keys():
            new_terms[e] = set()
        for n in normalized_terms:
            if n[0] not in static:
                new_terms[e].add(n[0])
    for k, v in new_terms.items():
        with open(os.path.join(root, 'analysis', f'new_terms_{k}.csv'), 'w') as f:
            f.write('\n'.join(v))


run('/home/esther/GitProjects/pubabsnlp')

