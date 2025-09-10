## How to run: snakemake --use-conda --cores 1

rule all:
    input:
        "output/filtered_genes/filtered_variants.csv",
        "quarto_rep/report_gen.html"

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

rule render_report:
    input:
        csv="output/filtered_genes/filtered_variants.csv",
        qmd="quarto_rep/report_gen.qmd"
    output:
        html="quarto_rep/report_gen.html"
    conda:
        "workflow/envs/quarto.yaml"
    container:
        "docker://bioinformaticsguy/my-quarto-image:latest"
    shell:
        """
        pwd
        cd quarto_rep
        echo "Rendering report..."
        # Ensure quarto is installed and available in the environment
        if ! command -v quarto &> /dev/null; then
            echo "Quarto is not installed. Please install it in the conda environment."
            exit 1
        fi
        # Render the report using quarto
        echo "Rendering report from {input.qmd} to {output.html}..."
        quarto render report_gen.qmd --to html
        """