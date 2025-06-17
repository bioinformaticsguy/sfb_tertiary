import pandas as pd

# Replace 'your_file.tsv' with the actual filename
file_path = 'data/test_files/SecondTrio.joint.GRCh38.small_variants.phased.norm.slivar.tsv'

# Read the TSV file
df = pd.read_csv(file_path, sep='\t')


# Load the gene list
gene_list_path = "output/gene_list/combined.txt"
with open(gene_list_path, 'r') as f:
    gene_list = [line.strip() for line in f if line.strip()]


# Filter rows where the 'gene' column contains any gene from the gene list
filtered_df = df[df['gene'].isin(gene_list)]

# Print the filtered rows
print(filtered_df)

# Display the first few rows
# print(df.head())
# print(gene_list)