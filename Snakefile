rule all:
    input:
        "output/filtered_genes/filtered_variants.csv"

rule find_overlap:
    input:
        tsv="data/test_files/SecondTrio.joint.GRCh38.small_variants.phased.norm.slivar.tsv",
        genes="output/gene_list/combined.txt"
    output:
        "output/filtered_genes/filtered_variants.csv"
    script:
        "src/find_overlap.py"