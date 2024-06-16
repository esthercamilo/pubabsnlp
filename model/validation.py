import random
from spacy.training import Example
from spacy.util import minibatch, compounding
import spacy

# Carregar o modelo pré-existente
nlp = spacy.load("en_ner_bionlp13cg_md")

# Dados de treinamento
train_data = [
    {
        "text": "BRCA1 gene is associated with breast cancer.",
        "entities": [(0, 5, "GENE"), (27, 39, "DISEASE")]
    },
    {
        "text": "p53 mutation can lead to various cancers.",
        "entities": [(0, 3, "GENE"), (28, 35, "DISEASE")]
    },
    {
        "text": "EGFR inhibitors are used to treat lung cancer.",
        "entities": [(0, 4, "GENE"), (35, 46, "DISEASE")]
    },
    # Adicione mais exemplos conforme necessário
]

# Adicionar novos rótulos ao NER
ner = nlp.get_pipe("ner")
for item in train_data:
    for ent in item['entities']:
        ner.add_label(ent[2])

# Criar exemplos de treinamento
examples = []
for item in train_data:
    doc = nlp.make_doc(item['text'])
    example = Example.from_dict(doc, {"entities": item['entities']})
    examples.append(example)

# Treinamento do modelo
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.resume_training()
    for itn in range(20):  # ajuste o número de iterações conforme necessário
        random.shuffle(examples)
        losses = {}
        batches = minibatch(examples, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            nlp.update(batch, drop=0.5, losses=losses)
        print(f"Iteration {itn}, Losses: {losses}")

# Dados de validação
validation_data = [
    {
        "text": "BRCA1 is a gene associated with breast cancer.",
        "entities": [(0, 5, "GENE"), (31, 43, "DISEASE")]
    },
    {
        "text": "Mutations in the p53 gene can lead to various cancers.",
        "entities": [(16, 19, "GENE"), (39, 46, "DISEASE")]
    },
    {
        "text": "EGFR is a gene that plays a role in many cancers, including lung cancer.",
        "entities": [(0, 4, "GENE"), (55, 66, "DISEASE"), (68, 79, "DISEASE")]
    },
    # Adicione mais exemplos conforme necessário
]

# Criar exemplos de validação
validation_examples = []
for item in validation_data:
    doc = nlp.make_doc(item['text'])
    example = Example.from_dict(doc, {"entities": item['entities']})
    validation_examples.append(example)

# Avaliar o modelo
scores = nlp.evaluate(validation_examples)

# Imprimir as métricas
print("Precision:", scores["ents_p"])
print("Recall:", scores["ents_r"])
print("F1-score:", scores["ents_f"])
