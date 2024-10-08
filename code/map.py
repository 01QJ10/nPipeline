# %%
## Model Benchmarking
# https://www.sbert.net/docs/sentence_transformer/pretrained_models.html
import pandas as pd
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
 # %%
all_associations = pd.read_csv("../data/gwas_catalog_v1.0.2-associations_e112_r2024-09-22.tsv", sep='\t', low_memory=False)
all_studies = pd.read_csv("../data/gwas-catalog-v1.0.3.1-studies-r2024-09-22.tsv", sep='\t', low_memory=False)
formA = pd.read_excel("../data/FormA706_20231010.xlsx", sheet_name="dictionary")

# %%
print(all_associations.columns)
print(all_studies.columns)
print(formA.columns)
# %%
formADesc = formA["Description"].unique()
allAssociations_trait = all_associations["DISEASE/TRAIT"].unique()
print(len(formADesc))
print(len(allAssociations_trait))
# %%
np.savetxt('../results/formA_description.txt', formADesc, fmt='%s')
np.savetxt('../results/all_associations_trait.txt', allAssociations_trait, fmt='%s')
# %%
# all-mpnet-base-v2 (The best performance model from the benchmark)
# paraphrase-albert-small-v2 (Smallest model for testing)
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
# print(embeddings)
# %%
def find_top_k_closest(embeddings_A, embeddings_B, top_k, ls_A, ls_B):
    similarity_matrix = cosine_similarity(embeddings_B, embeddings_A)

    closest_items = {}
    for i, sim_scores in enumerate(similarity_matrix):
        # Get indices of the top K most similar sentences from list_A for each sentence in list_B
        top_indices = np.argsort(sim_scores)[-top_k:][::-1]
        top_elements = [ls_A[x] for x in top_indices]
        closest_items[ls_B[i]] = top_elements
    
    return closest_items

# Example usage
embeddings_B = model.encode(formADesc)  
embeddings_A = model.encode(allAssociations_trait)  

result = find_top_k_closest(embeddings_A, embeddings_B, 50, allAssociations_trait, formADesc)
print(result)
# %%
df = pd.DataFrame.from_dict(result, orient='index')

csv_file_path = '../results/formA_associations_50_matches.csv'
df.to_csv(csv_file_path, index_label='DESCRIPTIONS')

print(f"Results exported to {csv_file_path}")
# %%