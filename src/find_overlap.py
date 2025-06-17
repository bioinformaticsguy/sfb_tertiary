import pandas as pd

# Replace 'your_file.tsv' with the actual filename
file_path = 'data/test_files/your_file.tsv'

# Read the TSV file
df = pd.read_csv(file_path, sep='\t')

# Display the first few rows
print(df.head())