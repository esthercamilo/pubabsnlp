s = open('training_bionlp13cg_sub.tsv', 'w')

count = {}

with open('training_bionlp13cg.tsv') as f:
    for l in f:
        line = l.split('\t')
        if line[3] not in count.keys():
            count[line[3]] = 0
        count[line[3]] += 1
        if count[line[3]] >= 250:
            continue
        s.write(l)

