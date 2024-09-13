from openai import OpenAI

# Inicialize o cliente OpenAI
k = ''
client = OpenAI(api_key=k)


def gerar_respostas_gpt(texto):
    prompt = (
        "Sobre o texto a seguir, qual a técnica de sequenciamento empregada, "
        "qual a metodologia computacional utilizada, qual o banco de dados utilizado e "
        "quais os desafios enfrentados?\n\n"
        f"{texto}"
    )

    response = client.chat.completions.create(
        model="gpt-4",  # Ou outro modelo disponível
        messages=[
            {"role": "system",
             "content": "Você é um assistente que ajuda a analisar textos científicos e responder a perguntas específicas."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,  # Ajuste conforme necessário para obter respostas mais detalhadas
        temperature=0.7
    )

    # Acessar a resposta corretamente
    return response.choices[0].message.content.strip()


# Texto de exemplo
texto_exemplo = (
    "The availability of high-throughput genotyping and sequencing platforms has largely removed technological barriers "
    "in the mapping the genetic determinants of drug response in human populations, and the set of validated pharmacogenetic "
    "variants is gradually increasing. Like the search for disease-susceptibility variation, however, many of the loci identified "
    "to date represent the relatively low-hanging fruit with large phenotypic effects but relatively low predictive power. Yet to "
    "be discovered is the larger set of variants, each with considerably weaker phenotypic effects, which together can be used to "
    "predict drug response more reliably and identify potential targets for novel drug development. Finding these pharmacogenetic "
    "variants is particularly challenging because sample size is typically far too small (and thus statistically underpowered) to "
    "detect genetic variants with weak effects. Studies of the genetics of gene expression (also described as expression quantitative "
    "locus (eQTL) mapping or genetical genomics) represent a novel approach for identification of functional genetic variants that "
    "influence gene expression. In these studies, individual gene transcript abundance as measured from expression microarrays are "
    "considered as discrete quantitative traits for genetic mapping that are intermediate to clinical outcomes of interest. Early studies "
    "using these methods have demonstrated improved power to detect such regulatory variants and have facilitated mapping of disease-susceptibility "
    "variants. The potential use of this approach in the study of pharmacogenetics and for the identification of potentially modifiable drug targets is reviewed here."
)

# Aplicar a função e imprimir as respostas
respostas = gerar_respostas_gpt(texto_exemplo)
print(respostas)
