import os

import spacy

# nlp = spacy.load("en_ner_bionlp13cg_md")
nlp = spacy.load("/home/esther/GitProjects/pubabsnlp/model/pharmacogenetics_ner_model")

count = 1

texts = []
allfiles = os.listdir('results')
for i in range(len(allfiles)):
    with open(os.path.join('results', allfiles[i]), "r") as f:
        abstract = [x for x in f.readlines() if x][-1]
        if 'pcr' in abstract.lower():
            count += 1
            print(i)
            print(abstract)
            texts.append(abstract)
            if count > 10:
                break
        # texts.append(abstract)

docs = [nlp(text) for text in texts]

for text in texts:
    doc = nlp(text)
    for ent in doc.ents:
        print(ent.text, ent.label_)



# análise mais profunda com topic modeling
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.decomposition import LatentDirichletAllocation
#
# # Vetorização dos textos
# vectorizer = CountVectorizer(stop_words='english')
# X = vectorizer.fit_transform(texts)
#
# # Aplicar LDA
# lda = LatentDirichletAllocation(n_components=10, random_state=42)
# lda.fit(X)
#
# # Mostrar os tópicos descobertos
# terms = vectorizer.get_feature_names_out()
# for idx, topic in enumerate(lda.components_):
#     print(f"Tópico {idx}:")
#     print([terms[i] for i in topic.argsort()[-10:]])

# # análise com visualizaçao
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
#
# # Gerar a nuvem de palavras
# wordcloud = WordCloud().generate(' '.join(texts))
#
# # Mostrar a nuvem de palavras
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')
# plt.show()
