import pandas as pd
import sys
import os

# Usage: python generate_genes_with_source.py file1.txt file2.txt ...

if len(sys.argv) < 2:
    print("Usage: python generate_genes_with_source.py file1.txt file2.txt ...")
    sys.exit(1)

all_genes = []
for file in sys.argv[1:]:
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