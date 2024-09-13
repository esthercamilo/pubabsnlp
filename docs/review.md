Reviewer: 1

Comments to the Author
The paper presents an important and interesting problem, yet several areas require significant improvements.
The abstract is excessively long and uses acronyms without defining them. 
Abstracts for scientific work should be concise and focused, ideally between 150-250 words, 
ensuring clarity and brevity. 
Authors should refer to established guidelines on abstract writing for scientific papers to enhance its effectiveness.
The entities involved in the authors' work and the annotation process lack clarity. 
A detailed explanation of the entities and a comprehensive description of the annotation process are needed
for understanding the scope and methodology of the research. 
The methods employed are not clearly delineated. 
The current format appears to prioritize discussion over a clear presentation of the methods used. 
It is imp to explicitly outline the methodologies to provide clarity and structure.   
Critical information is relegated to the appendix or after references, is it format of the paper? 
making it difficult for reviewers to identify important details within the main content.
Vital information should be integrated into the main sections of the paper to ensure accessibility.
Related works, such as one has conducted similar research but with different entities. 
The authors need to clearly differentiate their work by explaining how their methods for entity extraction differ
from published work, and how their method is unique, is it the problem solved unique or is it the method? 
Large Language Models (LLMs) for this purpose can be used? if so, should be briefly discussed, 
highlighting both the advantages and limitations. It would be good to include a proper architecture diagram 
or at least a workflow of the research would significantly enhance the paper's comprehensibility 
and demonstrate a clear progression of the work.

Tasks:
1. reduce the abstract and avoid acronyms.
2. clarify ENTITIES used and justify their choice - how they are different from other papers?
3. clarify methodology and prioratize methods over discussion.
4. the supplementar is in a bad format. Try to include the table inside the paper.
5. Discuss why we didn't use LLMs models instead hightlighting advantages and limitations.
6. Include a proper architecture diagram or workflow about the whole methodology.


Reviewer: 2

Comments to the Author
The manuscript describes a natural language processing approach to extract entities and key concepts from the abstracts of peer-reviewed articles related to pharmacogenomics research from PubMed. While the article was framed as the development of a new pipeline to facilitate pharmacogenomic literature reviews, the focus of the results and discussion were a qualitative analysis of the key terms that were extracted, in which numerous assumptions and conjectures regarding the state of the field of pharmacogenomics are made. Additionally, the manuscript would benefit greatly from a more thorough description of the developed algorithm and pipeline, as well as its performance in extracting these concepts. I have several comments that should be addressed prior to being considered for publication.
1.)     Why and how was the collection limited to 4,000 articles? Was it the most recent, most cited, most “relevant” in PubMed? Further, did these 4,000 articles include only original research articles or did it include systematic reviews, meta-analyses, commentaries, etc.? The findings of the qualitative analysis may suffer from selection bias if only a subset of articles were included, and the frequency of the key terms identified may be inflated if non-original research articles were used. Was the search limited to a certain time frame (e.g., articles published in the last 5 years)?
2.)     It is unclear whether using only the keyword “pharmacogenomics” allows for a comprehensive selection of articles in which an informed qualitative analysis can be made. Does the use of this word capture synonyms or related words (e.g., pharmacogenetics)? How do the authors really know that the articles are related to pharmacogenomics? Was the word pharmacogenomics in the journal name, title, abstract, or keywords?
3.)     Why were four entities—TECHNIQUE, ANALYTICAL_METHOD, DATABASE, and CHALLENGE—used to group terms, and how is using these groups beneficial to the goals of this pipeline? A description of each of these entities should be included in the methods and how the authors arrived at these four groupings.
4.)     More information is needed on how the custom NER model was trained and how the overall pipeline works. What algorithm was used? Was a subset of the 4,000 articles used for this training, or what other data were used for training? How was a gold standard developed to validate the trained model (e.g., manual annotation)?
5.)     Related to my previous comment, there is no measure of accuracy (precision, recall, F1) to validate that the trained model correctly identified terms/sub-groups that correspond with each entity.
6.)     How are duplicate terms being handled regarding the frequency or count of each identified term? For example, in the supplementary, it appears that the same abstract captured “next-generation sequencing” and “NGS.” Similarly, are there instances where the same word/phrase may be counted across entities? For example, “cost analysis” is captured in ANALTYICAL_METHOD and “cost” is captured in CHALLENGE. Finally, are there instances where key words do not fall under any of the four entities and how does the pipeline handle that?
7.)     Were any preprocessing steps (e.g., lowercasing, stemming, lemmatization) considered prior to implementing NER? I wonder if doing so may help to group some of the terms listed in the supplementary (e.g., “PBPK modeling”, “PBPK modelling”, “PBPK models”, and “PBPK model” are all the same).
8.)     I am concerned with many of the interpretations that were made from the extracted words/phrases as they relate to the field of pharmacogenetics. Making interpretations about certain words and the state of the field based solely on the frequency of words, especially when the current pipeline uses a limited collection of articles and there may be certain contextual information that NER may miss, is speculative at best and misleading at worst. For instance, on page 8, it is written that “variability…underscores the genetic diversity complicating uniform treatments”, but there are numerous reasons for the use of “variability” that are not associated with genetic diversity that are not considered (e.g., PGx explaining variability in drug exposure or response). I recommend the authors be more cautious with their interpretations and understanding of the limitations of their analysis. Same for “real-world” this could be a data source, not a challenge. How does what the algorithm find compare with the articles published by PGx experts describing the challenges in implementation or the challenges in genotyping or the challenges for using NGS for PGx?
9.)     The conclusion is lacking a greater discussion on how this approach will benefit literature reviews and knowledge extraction for pharmacogenetics. How should this pipeline be used in comparison to or in association with current pharmacogenetic resources? Why should this NLP-based approach be utilized as compared to using or developing more advanced NLP models that are well-suited for this task (e.g., BERT, GPT)? Relatedly, what are the next steps for the development of this pipeline?
10.)    Only one medication (pantoprazole) was identified based on the supplementary material. Can the authors clarify why only one medication was extracted? This seems like a major limitation of the current pipeline for pharmacogenetics literature reviews if medications are not being identified or associated with papers. Similarly, I am surprised that no gene names were identified.
11.)    A paragraph describing the limitations of the current pipeline and analysis should be added to the discussion.
12.)    The supplementary information is difficult to understand with how it is currently formatted and would benefit by being converted to a table. Further, a figure or table showing the most commonly occurring terms (and least occurring) should be added to the main text.

Tasks:
1. describe better the code and pipeline

2. add performance quality metrics

3. bring all articles instead of 4000. Provide more details about how articles were chosen
Fato é que mesmo 4000 não é tudo que há, pois nossa visão ainda é limitada, pois olhamos somente no abstract, não olhamos no artigo inteiro.

4. the reviewer thinks "pharmacogenomics" was not a good choice. Think about better ones and justify them

5. the reviewe didn't understand why we chose 4 entities. Explicar que eu quis mostrar como um empresário poderia ter conhecimento sobre o estado da arte
6. Explain better the training and quality process of the model (same as reviewer 1)
7. no measure of accuracy
8. how duplicates are handled? Explicar que o objetivo final é qualitativo e a quantidade não é precisa.
9. where are pre-processing such as lower cases?
10. o comentário 8 deixa claro que o revisor não compreende como funcionam as NER. Preciso explicar melhor no artigo.
11. reclamou que a conclusão não deixa claro o objetivo de se fazer isso e como isso pode beneficiar a comunidde.
12. reclama no item 10 que só apareceu um medicamento. Na verdade não era pra aparecer nenhum, foi um erro. Ficou surpreso porque nenhum gene apareceu. E de fato não era pra aparecer. É NER.
13. Reclamou que não consegue entender a informação suplementar.

