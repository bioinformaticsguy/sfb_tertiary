## How to run: snakemake -s workflow/plot_analysis.smk --use-conda --cores 1
## With DOcker: snakemake -s workflow/plot_analysis.smk --use-singularity --cores 1

rule all:
    input:
        "output/plots/r_plots/third_trio_156.png"

rule plot_coverage:
    input:
        yaml_config="src/data_to_plot.yaml",
    output:
        "output/plots/r_plots/third_trio_156.png"
    conda:
        "envs/r_environment.yaml"
    container:
        "docker://bioinformaticsguy/r-plotting:latest"
    shell:
        """
        mkdir -p output/plots/r_plots
        Rscript src/plot_coverage_per_chr.R src/data_to_plot.yaml
        """


# Rscript plot_coverage_per_chr.R data_to_plot.yaml