import os
from Bio import Entrez

root = os.path.abspath('.')


def search_and_fetch(query, max_results=5):
    Entrez.email = 'esthercamilo@gmail.com'
    print(Entrez.email)
    handle = Entrez.esearch(db='pubmed', term=query, retmax=max_results)
    results = Entrez.read(handle)
    ids = results['IdList']

    for pub_id in ids:
        print(pub_id)
        article = Entrez.efetch(db='pubmed', id=pub_id, retmode='xml')
        article_info = Entrez.read(article)
        try:
            title_ = article_info['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleTitle']
            d = str(article_info['PubmedArticle'][0]['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate'])
            abstract = article_info['PubmedArticle'][0]['MedlineCitation']['Article']['Abstract']['AbstractText'][0]
            title = ''.join([x for x in title_])
            path = os.path.join(root, 'results', f"{title}txt")
            with open(path, 'w') as f:
                f.write(d)
                f.write('\n')
                f.write(abstract)
                print(f"Salvo: {pub_id}")
        except Exception as e:
            # Skip articles without abstracts
            print(e)
            continue


def run():

    # Create 'results' folder if not exists
    os.makedirs('results_full', exist_ok=True)

    # Type the words in the file data/query_words.txt
    with open(os.path.join(root, 'data', 'query_words.txt'), 'r') as f:
        words = [x.rstrip('\n') for x in f.readlines() if x]
    query = ' OR '.join(words)
    max_results = 100000
    search_and_fetch(query, max_results=max_results)


run()

