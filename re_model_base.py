"""
AMINO_ACID, Amino_acid_monomer
ANATOMICAL_SYSTEM,Body_region
CANCER,cancer
CELL,Cell_natural
CELLULAR_COMPONENT,Cell_component
DEVELOPING_ANATOMICAL_STRUCTURE
GENE_OR_GENE_PRODUCT,Protein_molecule
GENE_OR_GENE_PRODUCT,DNA_domain_or_region
GENE_OR_GENE_PRODUCT,DNA_family_or_group
GENE_OR_GENE_PRODUCT,DNA_molecule
GENE_OR_GENE_PRODUCT,DNA_substructure
GENE_OR_GENE_PRODUCT,Protein_complex
GENE_OR_GENE_PRODUCT,Protein_molecule
GENE_OR_GENE_PRODUCT,RNA_molecule
IMMATERIAL_ANATOMICAL_ENTITY
MULTI_TISSUE_STRUCTURE
ORGAN,Body_region
ORGANISM,Multicellular_organism_natural
ORGANISM,Unicellular_organism
ORGANISM,Virus
ORGANISM_SUBDIVISION
ORGANISM_SUBSTANCE
PATHOLOGICAL_FORMATION
SIMPLE_CHEMICAL,Element
SIMPLE_CHEMICAL,Inorganic_compound
SIMPLE_CHEMICAL,Organic_compound_other
"""
import os
import xml.etree.ElementTree as ET


def get_dict():
    return {
        'Amino_acid_monomer': 'AMINO_ACID',
        'cancer': 'CANCER',
        'Cell_natural': 'CELL',
        'Cell_component': 'CELLULAR_COMPONENT',
        'DEVELOPING_ANATOMICAL_STRUCTURE': 'DEVELOPING_ANATOMICAL_STRUCTURE',
        'Protein_molecule': 'GENE_OR_GENE_PRODUCT',
        'DNA_domain_or_region': 'GENE_OR_GENE_PRODUCT',
        'DNA_family_or_group': 'GENE_OR_GENE_PRODUCT',
        'DNA_molecule': 'GENE_OR_GENE_PRODUCT',
        'DNA_substructure': 'GENE_OR_GENE_PRODUCT',
        'Protein_complex': 'GENE_OR_GENE_PRODUCT',
        'RNA_molecule': 'GENE_OR_GENE_PRODUCT',
        'Body_region': 'ORGAN',
        'Multicellular_organism_natural': 'ORGANISM',
        'Unicellular_organism': 'ORGANISM',
        'Virus': 'ORGANISM',
        'Element': 'SIMPLE_CHEMICAL',
        'Inorganic_compound': 'SIMPLE_CHEMICAL',
        'Organic_compound_other': 'SIMPLE_CHEMICAL'}


def process_bioc_file(file_path, storefile=None):
    # Parse o arquivo XML
    tree = ET.parse(file_path)
    root = tree.getroot()
    abstract_root = root.findall(".//AbstractText")[0]

    sentences = []
    convert = get_dict()
    for sentence in abstract_root.findall(".//sentence"):
        t = ''.join(sentence.itertext()).strip()
        sentence_text = ' '.join(t.replace('\n', ' ').split())
        # Processar termos
        for term in sentence.findall(".//term"):
            sem = term.get('sem', '')
            lex = term.get('lex', '')
            trecho = lex or sem
            sem = convert.get(sem)
            """
            "Challenges related to rare-variant pharmacogenomics", {'entities': [[22, 34, 'CHALLENGE']]}
            """
            if sem:
                start = sentence_text.index(trecho)
                end = start + len(trecho)
                storefile.write(f'"{sentence_text}", ' + '{"entities": [[' + f" {start}, {end}, '{sem}'" + "]]}\n")
    return sentences


# Caminho para o arquivo BioC
path_root = '/home/esther/GitProjects/pubabsnlp/model/GENIA/Meta-knowledge_GENIA_Corpus/Corpus/'
store = open('retrain_data.csv', 'w')
allfiles = os.listdir(path_root)
number_of_files = 0
for fp in allfiles:
    number_of_files += 1
    print(number_of_files)
    file_path = path_root + fp
    try:
        data = process_bioc_file(file_path, storefile=store)
    except Exception as e:
        print(f"{number_of_files} falhou")

    # if number_of_files > 500:
    #     break

store.close()
