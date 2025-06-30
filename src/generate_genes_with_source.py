import pandas as pd
import sys

# Usage: python generate_genes_with_source.py file1.txt source1 file2.txt source2 ...

args = sys.argv[1:]
if len(args) % 2 != 0 or len(args) == 0:
    print("Usage: python generate_genes_with_source.py file1.txt source1 [file2.txt source2 ...]")
    sys.exit(1)

gene_files = [(args[i], args[i+1]) for i in range(0, len(args), 2)]

all_genes = []
for file, source in gene_files:
    with open(file) as f:
        genes = [line.strip() for line in f if line.strip()]
        all_genes.extend([(gene, source) for gene in genes])

df = pd.DataFrame(all_genes, columns=["gene", "source"])
df.to_csv("output/gene_list/all_genes_with_source.csv", index=False)