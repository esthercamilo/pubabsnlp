import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE
from sentence_transformers import SentenceTransformer
import json


def run_clustering(ent, root):
    # Carregue o modelo de embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    entities = [ent]

    with open(os.path.join('analysis', 'output.json'), 'r') as r:
        data = json.loads(r.read())

    for e in entities:

        terms = data.get(e)

        # Normalizar termos
        normalized_terms = [[item.lower() for item in sublist] for sublist in terms]

        # Transforme os termos em vetores
        embeddings = model.encode(terms)

        # Crie o modelo DBSCAN
        dbscan = DBSCAN(eps=0.5, min_samples=2, metric='cosine')

        # Ajuste o modelo aos embeddings dos termos
        clusters = dbscan.fit_predict(embeddings)
        print(clusters)

        # Reduzir os embeddings para 2D usando t-SNE
        tsne = TSNE(n_components=2, perplexity=5, random_state=42)
        embeddings_2d = tsne.fit_transform(embeddings)

        plt.figure(figsize=(40, 30))  # Aumenta o tamanho da figura

        unique_labels = set(clusters)
        colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

        for k, col in zip(unique_labels, colors):
            if k == -1:
                col = [0, 0, 0, 1]

            class_member_mask = (clusters == k)

            xy = embeddings_2d[class_member_mask]
            plt.scatter(xy[:, 0], xy[:, 1], c=[col], s=1, label=f'Cluster {k}' if k != -1 else 'Noise', alpha=0.5)

            cluster_terms = np.array(normalized_terms)[class_member_mask]

            if k != -1 and len(cluster_terms) > 0:
                # Encontrar o centro do cluster
                cluster_center = np.mean(xy, axis=0)

                annotated_terms = set()

                for idx in range(len(cluster_terms)):
                    term = cluster_terms[idx]
                    if term[0] not in annotated_terms:
                        plt.annotate(term[0], (xy[idx, 0], xy[idx, 1]), fontsize=6, color='black')
                        annotated_terms.add(term[0])

        plt.title(f"Clustering visualization {ent})")
        plt.legend()

        # Salvar a imagem em vez de mostrar
        path = os.path.join(root, 'graphics', f'clusters_visualization_{ent}.png')
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()  # Fechar a figura após salvar
        print(f"Cluster visualization saved for entity: {ent}")


def run(root):
    entities = ['TECHNIQUE', 'ANALYTICAL_METHOD', 'DATABASE', 'CHALLENGE']
    for e in entities:
        run_clustering(e, root)
