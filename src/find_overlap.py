import pandas as pd

# Replace 'your_file.tsv' with the actual filename
file_path = 'data/test_files/SecondTrio.joint.GRCh38.small_variants.phased.norm.slivar.tsv'

# Read the TSV file
df = pd.read_csv(file_path, sep='\t')


# Load the gene list
genes_df = pd.read_csv("output/gene_list/all_genes_with_source.csv")
gene_list = genes_df['gene'].unique()  # Get unique gene names


# Filter rows where the 'gene' column contains any gene from the gene list
filtered_df = df[df['gene'].isin(gene_list)]

filtered_df.to_csv("output/filtered_genes/filtered_variants.csv", index=False)

# Print the filtered rows
print(filtered_df)

# Display the first few rows
# print(df.head())
# print(gene_list)