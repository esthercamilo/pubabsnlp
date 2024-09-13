# Unlocking New Insights from PubMed Articles Abstracts: Conceptual Extraction and Clustering Methodology Applied to Pipelines for Pharmacogene Phenotype prediction

## Introduction

Python script to review and extract insights from scientific article abstracts.

The pipeline consists of three main components: 
1. downloading data from PubMed using the e-utilities library; 
2. processing abstracts to extract terms of interest; and 
3. grouping and analyzing the articles.

We make use of the spaCy library with the `en_ner_bionlp13cg_md` model, a named entity recognition (NER) model
specifically designed for biomedical text. It was trained on the BioNLP 2013 corpus and can recognize entities such
as diseases, chemicals, genes, and proteins. This model helps in extracting relevant biomedical entities from 
scientific texts, aiding in tasks like literature mining, information extraction, and knowledge discovery in the
biomedical domain.

## Installation and requirements

1. clone the repository:
    ```git clone https://github.com/esthercamilo/pubabsnlp.git```
2. create a virtual python environment
    https://docs.python.org/3/library/venv.html
3. install the requirements:
    ```cd pubabsnlp```
    ```pip install -r requirements```
4. install the pre-trained model
    ```pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_ner_bionlp13cg_md-0.4.0.tar.gz```
5. In order to have the scripts working properly, you will need at least a dual-core CPU, 
   8 GB of RAM, 128 GB storage, and an operating system such as Windows, macOS, or Linux.

## Usage

1. define single query words for article selection in the file data/query_words.txt
2. execute the script `entrez.py` to download all abstracts related to the chosen query words. 
3. next you can play with the script `analysis.py` to extract metrics from specific query words related to your research:
    ```python analysis.py pcr```
    this will provide you with the abstract id and if it has or not the term. You can also search for 

## Anotation

`label-studio start`
