import pandas as pd
import sys
import os
from glob import glob

# Usage: python generate_genes_with_source.py directory_path

if len(sys.argv) != 2:
    print("Usage: python generate_genes_with_source.py directory_path")
    sys.exit(1)

directory = sys.argv[1]

all_genes = []
# Get all .txt files in the directory
for file in glob(os.path.join(directory, "*.txt")):
    # Use the filename (without extension) as the source
    source = os.path.splitext(os.path.basename(file))[0]
    with open(file) as f:
        content = f.read().strip()
        # If the file is comma-separated (one line), split by comma
        if ',' in content and '\n' not in content:
            genes = [gene.strip() for gene in content.split(',') if gene.strip()]
        else:
            # Otherwise, assume one gene per line
            genes = [line.strip() for line in content.splitlines() if line.strip()]
        all_genes.extend([(gene, source) for gene in genes])

df = pd.DataFrame(all_genes, columns=["gene", "source"])
df.to_csv("output/gene_list/all_genes_with_source.csv", index=False)