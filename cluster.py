import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE
from sentence_transformers import SentenceTransformer
import json


def get_terms(entity):
    with open('output.json', 'r') as r:
        data = json.loads(r.read())
    return [x[0] for x in data.get(entity)]


def run_clustering():
    # Carregue o modelo de embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    entities = ['CHALLENGE']
    for e in entities:
        terms = get_terms(e)

        # Transforme os termos em vetores
        embeddings = model.encode(terms)

        # Crie o modelo DBSCAN
        dbscan = DBSCAN(eps=0.5, min_samples=2, metric='cosine')

        # Ajuste o modelo aos embeddings dos termos
        clusters = dbscan.fit_predict(embeddings)
        print(clusters)

        partial_result = dict(zip(terms, clusters))

        # Reduzir os embeddings para 2D usando t-SNE
        tsne = TSNE(n_components=2, perplexity=5, random_state=42)
        embeddings_2d = tsne.fit_transform(embeddings)

        # Criar a visualização
        plt.figure(figsize=(20, 15))  # Aumenta o tamanho da figura

        # Define cores para os clusters
        unique_labels = set(clusters)
        colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Cor para o ruído (outliers)
                col = [0, 0, 0, 1]

            class_member_mask = (clusters == k)

            xy = embeddings_2d[class_member_mask]
            # plt.scatter(xy[:, 0], xy[:, 1], c=[col], s=100, label=f'Cluster {k}' if k != -1 else 'Noise')
            plt.scatter(xy[:, 0], xy[:, 1], c=[col], s=1, label=f'Cluster {k}' if k != -1 else 'Noise', alpha=0.5)

            # Pegar os termos do cluster
            cluster_terms = np.array(terms)[class_member_mask]

            # Calcular o centro de cada cluster
            if k != -1 and len(cluster_terms) > 0:
                # Encontre o termo mais frequente no cluster
                most_frequent_term = max(set(cluster_terms), key=list(cluster_terms).count)

                cluster_center = np.mean(xy, axis=0)

                # plt.scatter(xy[:, 0], xy[:, 1], s=1, color='blue', edgecolor='none', linewidth=0.1)
                plt.annotate(most_frequent_term, (cluster_center[0], cluster_center[1]), fontsize=15,
                             color='black')

        plt.title("Visualização de Clusterização de Termos com DBSCAN e t-SNE")
        plt.legend()

        # Salvar a imagem em vez de mostrar
        plt.savefig('clusters_visualization_CHALLENGE.png', dpi=300, bbox_inches='tight')
        print()


if __name__ == '__main__':
    run_clustering()
