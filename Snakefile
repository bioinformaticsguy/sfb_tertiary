rule all:
    input:
        "output/filtered_genes/filtered_variants.csv"

rule generate_genes_with_source:
    input:
        expand("data/genes_list_data/{file}", file=[
            "flugent_200.txt",
            "agas_paper.txt"
            # add other gene list files here
        ])
    output:
        "output/gene_list/all_genes_with_source.csv"
    shell:
        "python src/generate_genes_with_source.py {input}"

rule find_overlap:
    input:
        tsv="data/test_files/SecondTrio.joint.GRCh38.small_variants.phased.norm.slivar.tsv",
        genes="output/gene_list/all_genes_with_source.csv"
    output:
        "output/filtered_genes/filtered_variants.csv"
    script:
        "src/find_overlap.py"