import pandas as pd
import numpy as np
from scipy import stats

def calculate_h_index(group):
    return sum(x >= i + 1 for i, x in enumerate(sorted(list(group['cit_all_years']), reverse=True)))

def main(category):
    # Read visibility index data
    visibility = pd.read_csv(f"domains_visibility_index_{category}.csv", sep=";")
    average_visibility = visibility.groupby('domain')['visibility_index'].mean().reset_index()

    # Read DOI and domain data
    dois = pd.read_csv(f"dois_domains_{category}.csv", sep=";")
    filtered_dois = dois[dois['status'] == 1] # filter dois that we found domain for them

    # Merge DOI and domain data with visibility index
    doi_domain_visibility = filtered_dois.merge(average_visibility, on='domain', how='inner')

    # Get the visibility index and number of dataset for each domain
    domains_doi_counts_visibility_index = doi_domain_visibility.groupby('domain').agg({'doi': 'count', 'visibility_index': 'mean'}).reset_index()
    domains_doi_counts_visibility_index.columns = ['domain', 'dois_number', 'mean_visibility_index']
    domains_doi_counts_visibility_index.to_csv(f'domain_visibility_datasetsNumber_{category}.csv', index=False, sep=';')

    # Read DOI metadata
    dois_info = pd.read_csv(f"dois_info_{category}.csv", sep="$") 
    dois_info['cite_norm'] = (dois_info['cit_all_years'] / (2024 - dois_info['pubyear']))
    dois_info['oa_status'] = np.where(dois_info['oa_status'] == 'closed', 0, 1)
    dois_citation = dois_info[['doi', 'cite_norm', 'cit_all_years', 'oa_status', 'pubyear']]

    # Merge DOI, domain, and visibility with other DOI metadata
    dois_all_info = doi_domain_visibility.merge(dois_citation, on='doi', how='inner')

    # Calculate h-index for different thresholds
    thresholds = [-1, 0, 1]
    for threshold in thresholds:
        filtered_dois_all_info = dois_all_info[(dois_all_info['pubyear'] > 2015) & (dois_all_info['pubyear'] < 2022)]
        domain_h_index = filtered_dois_all_info.groupby('domain').apply(calculate_h_index).reset_index()
        domain_h_index.columns = ['domain', 'h_index']

        visibility_hindex = average_visibility.merge(domain_h_index, on='domain', how='inner')
        visibility_hindex = visibility_hindex[visibility_hindex['h_index'] > threshold]

        spearman_corr = stats.spearmanr(visibility_hindex['visibility_index'], visibility_hindex['h_index'])
        print(f"Threshold {threshold} Spearman correlation for {category}:")
        print(spearman_corr)

        pearson_corr = stats.pearsonr(visibility_hindex['visibility_index'], visibility_hindex['h_index'])
        print(f"Threshold {threshold} Pearson correlation for {category}:")
        print(pearson_corr)

        visibility_hindex.to_csv(f'visibility_h-index_{category}_threshold_{threshold}.csv', index=False)
		

if __name__ == "__main__":
    categories = ["social", "economic"]
    for category in categories:
        main(category)
