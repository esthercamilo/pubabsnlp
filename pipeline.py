"""
Full pipeline for model creation and modelling usage
"""
import os

from analysis.analysis import run as run_analysis
from model.create_examples import run as run_create_samples
from model.main import run as run_model
from model.subsample import run as run_subsampling
from model.qualities.summary import run as run_quality_summary
from graphics.cluster import run as run_graphics

debug = False
root = os.getcwd()


def clearall():
    paths = [
        os.path.join('qualities'),
        os.path.join('sets'),
        os.path.join(root, 'model', 'fullsamples.tsv'),
        os.path.join(root, 'model', 'fulltraining.tsv'),
        os.path.join(root, 'model', 'training_bionlp13cg.tsv')
    ]

    for path in paths:
        try:
            if os.path.isdir(path):
                os.rmdir(path)
            else:
                os.remove(path)
        except OSError:
            pass  # Ignora erros como "arquivo/diretório não encontrado"


# 0. If not debug, clean up
# if not debug:
#     clearall()

# 1. Create samples for training. In this phase two files are created: fullsamples.tsv and training_bionlp13cg.tsv
# run_create_samples(debug, root)

# 2. Sub-sampling. Result file: fulltrainging.tsv
# run_subsampling(root)

# 3. Modellging and validation
# run_model(root)
# run_quality_summary(root)

# 4. Apply model to all abstracts
# run_analysis(root)

# 5. Plot analysis
run_graphics(root)
