import os
import re
import pandas


def file_quality(data):
    results = {}

    for line in data.strip().split("\n\n"):
        lines = line.split("\n")
        category = lines[0].strip()

        precision = float(re.search(r'Precision:\s*(\d+\.\d+)', line).group(1))
        recall = float(re.search(r'Recall:\s*(\d+\.\d+)', line).group(1))
        f1_score = float(re.search(r'F1-score:\s*(\d+\.\d+)', line).group(1))

        # Armazena os resultados no dicionário
        results[category] = {
            'Precision': precision,
            'Recall': recall,
            'F1-score': f1_score
        }
    return results


def run(root):
    qfolder = os.path.join(root, 'model', 'qualities')
    files = os.listdir(qfolder)
    final_results = {}
    for fname in files:
        if 'quality_metrics' not in fname:
            continue
        with open(os.path.join(qfolder, fname)) as f:
            data = f.read()
        partial_result = file_quality(data)
        for k, v in partial_result.items():
            if k not in final_results.keys():
                final_results[k] = {'Precision': 0, 'Recall': 0, 'F1-score': 0}
            final_results[k]['Precision'] += partial_result[k]['Precision']
            final_results[k]['Recall'] += partial_result[k]['Recall']
            final_results[k]['F1-score'] += partial_result[k]['F1-score']

    df = pandas.DataFrame(data=final_results)
    df = df[['TECHNIQUE', 'ANALYTICAL_METHOD', 'DATABASE', 'CHALLENGE']].T.apply(lambda k: k/10).round(4)
    df.to_csv(os.path.join(root, 'model', 'qualities', 'final_qualities.txt'))

