## Included by the main Snakefile — do not run directly.
## To trigger this rule, pass a configfile:
##   snakemake --configfile config/plot_config.yaml --use-conda --cores 4

import os

def _plot_files(cfg):
    """Derive the three output HTML paths from out_dir and plot_name."""
    base = os.path.join(
        cfg.get("out_dir", "output/plots/r_plots"),
        os.path.splitext(cfg.get("plot_name", "coverage_plot.html"))[0]
    )
    return {
        "aligned": base + "_aligned.html",
        "boxplot":  base + "_boxplot.html",
        "per_chr":  base + "_per_chr.html",
    }

rule plot_coverage:
    output:
        aligned = _plot_files(config)["aligned"],
        boxplot  = _plot_files(config)["boxplot"],
        per_chr  = _plot_files(config)["per_chr"],
    params:
        config_file = workflow.configfiles[0]
    conda:
        "envs/r_environment.yaml"
    container:
        "docker://bioinformaticsguy/r-plotting:latest"
    shell:
        """
        mkdir -p {config[out_dir]}
        Rscript src/plot_coverage_per_chr.R {params.config_file}
        """
