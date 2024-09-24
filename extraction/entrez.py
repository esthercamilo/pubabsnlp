import os
from Bio import Entrez

root = os.path.abspath('.')


def search_and_fetch(query, max_results=5):
    Entrez.email = '<your email>'
    print(Entrez.email)

    # Paginate to retrieve all results. As we are interested in new technologies, we search results from 2000
    handle = Entrez.esearch(db='pubmed', term=query, retmax=max_results)
    record = Entrez.read(handle)
    ids = record['IdList']
    saved_ids = [x.split('.')[0] for x in os.listdir('results')]

    for pub_id in ids:
        if pub_id in saved_ids:
            print(f"id já salvo {pub_id}")
            continue
        print(pub_id)
        article = Entrez.efetch(db='pubmed', id=pub_id, retmode='xml')
        article_info = Entrez.read(article)
        try:
            title_ = article_info['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleTitle']
            d = str(article_info['PubmedArticle'][0]['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate'])
            abstract = article_info['PubmedArticle'][0]['MedlineCitation']['Article']['Abstract']['AbstractText'][0]
            title = ''.join([x for x in title_])
            path = os.path.join(root, 'results', f"{pub_id}.txt")
            with open(path, 'w') as f:
                f.write(f"{d}\n{title}\n")
                f.write(abstract)
                print(f"Salvo: {pub_id}")
        except Exception as e:
            # Skip articles without abstracts
            print(e)
            with open('ids_abstract_not_found.csv', 'a') as f:
                f.write(f"{pub_id}\n")
                f.flush()
            continue


def run():

    # Create 'results' folder if not exists
    os.makedirs('results', exist_ok=True)

    # Type the words in the file data/query_words.txt
    start_year = 2008
    end_year = 2024
    for year in range(start_year, end_year + 1):
        query = f'(Pharmacogenomics[Title/Abstract] OR Pharmacogenetics[Title/Abstract]) AND ("{year}"[Date - Publication] : "{year+1}"[Date - Publication])'
        print(f"Searching for year: {year}")
        max_results = 100000
        search_and_fetch(query, max_results=max_results)


if __name__ == '__main__':
    run()

