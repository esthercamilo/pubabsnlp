"""
Samples are unbalanced.
'DATABASE': 551,
'TECHNIQUE': 1104,
'ANALYTICAL_METHOD': 1038,
'CHALLENGE': 47,
'GENE_OR_GENE_PRODUCT': 24853,
X 'AMINO_ACID': 415,
X 'SIMPLE_CHEMICAL': 29925,
'IMMATERIAL_ANATOMICAL_ENTITY': 257,
'CELL': 5879,
'ORGANISM': 17207,
'CANCER': 12822,
'CELLULAR_COMPONENT': 2314,
'TISSUE': 1126,
'MULTI_TISSUE_STRUCTURE': 1218,
'ORGAN': 2658,
'ORGANISM_SUBSTANCE': 1674,
'ANATOMICAL_SYSTEM': 783,
'ORGANISM_SUBDIVISION': 654,
'PATHOLOGICAL_FORMATION': 1143,
X 'DEVELOPING_ANATOMICAL_STRUCTURE': 15

"""
import os


def evaluate_quantities(root):
    """
    Verify the amount of instance fo each instance
    """
    fn1 = os.path.join(root, 'model', "fullsamples.tsv")
    fn2 = os.path.join(root, 'model', "training_bionlp13cg.tsv")
    entities = {}
    with open(fn1) as f1:
        for l in f1:
            line = l.split('\t')
            if line[3] not  in entities.keys():
                entities[line[3]] = 0
            entities[line[3]] += 1
    with open(fn2) as f2:
        for l in f2:
            line = l.split('\t')
            if line[3] not  in entities.keys():
                entities[line[3]] = 0
            entities[line[3]] += 1

    return entities


def select(root, n=100):
    """
    Prepare a full sample with about 500 examples of each instance
    """
    fn1 = os.path.join(root, 'model', "fullsamples.tsv")
    fn2 = os.path.join(root, 'model', "training_bionlp13cg.tsv")
    entities = {}
    output = []
    with open(fn1) as f1:
        for l in f1:
            line = l.split('\t')
            if line[3] not in entities.keys():
                entities[line[3]] = 0
            entities[line[3]] += 1
            output.append(l)

    exclude = ['AMINO_ACID', 'SIMPLE_CHEMICAL', 'DEVELOPING_ANATOMICAL_STRUCTURE']
    with open(fn2) as f2:
        for l in f2:
            line = l.split('\t')
            if line[3] in exclude:
                continue
            if line[3] not in entities.keys():
                entities[line[3]] = 0
            if entities[line[3]] <= n:
                entities[line[3]] += 1
                output.append(l)

    output_file = os.path.join(root, 'model', 'fulltraining.tsv')
    with open(output_file, 'w') as f:
        for l in output:
            f.write(l)


def run(root):
    print(evaluate_quantities(root))
    select(root)


